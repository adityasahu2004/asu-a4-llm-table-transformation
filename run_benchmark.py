import argparse
from dataclasses import asdict
import importlib
import json
import os
from pathlib import Path
import platform
import re
import sys
import time
import pandas as pd
from openai import OpenAI
from config import CONFIG, DEMO_CASES, ROOT
from execution import execute
from strategies.common import dump
from validation import score

def load_env():
    path = ROOT/'.env'
    if path.exists():
        for line in path.read_text().splitlines():
            if line and not line.startswith('#') and '=' in line:
                k,v = line.split('=',1)
                os.environ.setdefault(k.strip(),v.strip())

def case_key(path):
    return tuple(map(int,re.fullmatch(r'length(\d+)_(\d+)',Path(path).name).groups()))

def parser():
    p=argparse.ArgumentParser()
    p.add_argument('--strategy',choices=['s1','s2','s4','s5'],required=True)
    p.add_argument('--model',required=True)
    p.add_argument('--cases',default='all',help='all or comma-separated names; all includes five demo diagnostics')
    p.add_argument('--benchmark',type=Path,default=ROOT.parent)
    p.add_argument('--output',type=Path,default=ROOT)
    p.add_argument('--max-tokens',type=int,default=6000)
    p.add_argument('--reasoning-effort',default='none')
    p.add_argument('--sample-rows',type=int,default=12)
    p.add_argument('--k',type=int,default=5)
    p.add_argument('--timeout',type=int,default=120)
    p.add_argument('--api-timeout',type=int,default=3600,help='API queue/read timeout, separate from generated-code limit')
    p.add_argument('--rescore',action='store_true',help='Reexecute cached generated programs without API calls')
    p.add_argument('--reselect',action='store_true',help='Replay cached completions and candidate voting without API calls')
    return p

def main():
    args=parser().parse_args()
    load_env()
    CONFIG.output=args.output.resolve()
    for key in ('model','max_tokens','reasoning_effort','k','sample_rows','timeout','api_timeout'):
        setattr(CONFIG,key,getattr(args,key))
    CONFIG.base_url=os.getenv('OPENAI_BASE_URL','https://openai.rc.asu.edu/v1')
    if args.k < 2 or not 1 <= args.sample_rows <= 20:
        raise SystemExit('Require k>=2 and 1<=sample_rows<=20')
    paths=sorted((p for p in args.benchmark.resolve().glob('length*_*')
                  if p.is_dir() and re.fullmatch(r'length\d+_\d+',p.name)),key=case_key)
    if args.cases != 'all':
        names=set(args.cases.replace(' ',',').split(','))
        known={p.name for p in paths}
        if names-known:
            raise SystemExit(f'Unknown cases: {names-known}')
        paths=[p for p in paths if p.name in names]
    results=CONFIG.output/'results'/f'{args.strategy}.jsonl'
    results.parent.mkdir(parents=True,exist_ok=True)
    done={}
    if results.exists():
        for line in results.read_text().splitlines():
            row=json.loads(line)
            if row['model'] != args.model:
                raise SystemExit('Model mismatch; use a fresh output directory')
            previous=done.get(row['case'])
            if previous:
                row['wall_seconds']=max(row.get('wall_seconds',0),previous.get('wall_seconds',0))
            done[row['case']]=row
    client=None
    replay = args.rescore or args.reselect
    CONFIG.replay_only = args.reselect
    if not replay:
        if not os.getenv('OPENAI_API_KEY'):
            raise SystemExit('Missing OPENAI_API_KEY. Run configure_api.py locally.')
        client=OpenAI(base_url=CONFIG.base_url,timeout=CONFIG.api_timeout,max_retries=0)
    generate=importlib.import_module('strategies.'+args.strategy).generate
    config={k:str(v) if isinstance(v,Path) else v for k,v in asdict(CONFIG).items()}
    config.update(strategy=args.strategy,python=sys.version,platform=platform.platform(),
                  pandas=pd.__version__,held_out=list(DEMO_CASES),benchmark=str(args.benchmark.resolve()))
    config_path=CONFIG.output/'results'/f'{args.strategy}_config.json'
    if config_path.exists():
        previous=json.loads(config_path.read_text())
        for key in ('model','max_tokens','reasoning_effort','k','sample_rows','timeout','base_url'):
            if previous.get(key)!=config[key]:
                raise SystemExit(f'Configuration changed: {key}; use a fresh --output directory')
    dump(config_path,config)
    for path in paths:
        if path.name in done and not replay:
            previous=done[path.name]
            transport_failed = str(previous.get('error','')).startswith(('APIConnectionError:','APITimeoutError:'))
            if not transport_failed:
                continue
        if args.reselect and not (CONFIG.output/'logs'/args.strategy/path.name/'response.json').exists():
            raise SystemExit(f'No cached response for {path.name}; --reselect never calls the API')
        start=time.perf_counter()
        log=CONFIG.output/'logs'/args.strategy/path.name
        record={'case':path.name,'length':case_key(path)[0],'strategy':args.strategy,
                'model':args.model,'is_demo':path.name in DEMO_CASES,'parameters':config,
                'prompt_path':str((log/'prompt.json').relative_to(CONFIG.output)),
                'completion_path':str((log/'response.json').relative_to(CONFIG.output))}
        try:
            transform=CONFIG.output/'generated'/args.strategy/path.name/'transform.py'
            code=transform.read_text() if args.rescore and not args.reselect else generate(path,client,args.model)
            output, execution=execute(code,pd.read_csv(path/'test_0.csv'),CONFIG.timeout)
            record['execution']=execution
            if output is not None:
                record.update(score(output,pd.read_csv(path/'target.csv')))
            else:
                record['error']=execution.get('error',execution.get('stderr',execution['status']))
        except Exception as e:
            # Do not log full API exception strings, which may include request details.
            if getattr(e,'status_code',None) is not None or type(e).__name__ in {'APIConnectionError','APITimeoutError'}:
                raise SystemExit(f'API {type(e).__name__}, status {getattr(e,"status_code",None)}; cached progress preserved')
            record['error']=f'{type(e).__name__}: {e}'
            record.setdefault('execution',{'status':'generation_error'})
        meta=log/'generation.json'
        if meta.exists():
            record['generation']=json.loads(meta.read_text())
        for method in ('autopipeline','hard_match'):
            record.setdefault(method,{'accuracy':0.0,'is_correct':False,'similarities':{}})
        record['wall_seconds']=time.perf_counter()-start
        if not replay and path.name not in done and 'inherited_api_seconds' in record.get('generation',{}):
            record['wall_seconds']+=record['generation']['inherited_api_seconds']
        if not replay and path.name not in done and record.get('generation',{}).get('cached'):
            record['cached_generation_seconds']=record['generation'].get('latency_seconds',0)
            record['wall_seconds']+=record['cached_generation_seconds']
        if not replay and path.name in done and str(done[path.name].get('error','')).startswith(('APIConnectionError:','APITimeoutError:')):
            record['transport_recovery_seconds']=done[path.name]['wall_seconds']
            record['wall_seconds']+=done[path.name]['wall_seconds']
        if replay and path.name in done:
            record['replay_wall_seconds']=record['wall_seconds']
            record['wall_seconds']=done[path.name]['wall_seconds']
            if 'transport_recovery_seconds' in done[path.name]:
                record['transport_recovery_seconds']=done[path.name]['transport_recovery_seconds']
        dump(log/'validation.json',record)
        with results.open('a') as stream:
            stream.write(json.dumps(record,default=str)+'\n')
        print(f'{args.strategy} {path.name}: {record["execution"]["status"]}, '
              f'auto={record["autopipeline"]["is_correct"]}, hard={record["hard_match"]["is_correct"]}',flush=True)

if __name__=='__main__':
    main()
