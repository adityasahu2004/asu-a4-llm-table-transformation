import hashlib
import json
from pathlib import Path
import re
import tempfile
import time
import pandas as pd
from config import CONFIG
from execution import execute
from prompting import extract_code, messages

def dump(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w',dir=path.parent,prefix=path.name+'-',delete=False) as stream:
        json.dump(payload,stream,indent=2,default=str)
        temp=Path(stream.name)
    temp.replace(path)

def choose_candidate(records):
    clusters = {}
    for record in records:
        if record['execution']['status'] == 'ok':
            clusters.setdefault(record['execution']['fingerprint'], []).append(record['index'])
    if not clusters:
        raise RuntimeError('All sampled candidates failed execution or constraints')
    # No target-dependent ranking: ties go to earliest valid completion.
    winner = min(clusters.values(), key=lambda group:(-len(group),min(group)))
    return min(winner), clusters

def synthesize(case_dir, client, model, strategy, few_shot, consistency):
    case_dir = Path(case_dir)
    logs = CONFIG.output/'logs'/strategy/case_dir.name
    generated = CONFIG.output/'generated'/strategy/case_dir.name
    generated.mkdir(parents=True, exist_ok=True)
    expected = {'model':model,'temperature':0.7 if consistency else 0,
                'n':CONFIG.k if consistency else 1,'max_tokens':CONFIG.max_tokens,
                'reasoning_effort':CONFIG.reasoning_effort}
    if CONFIG.replay_only:
        request = json.loads((logs/'prompt.json').read_text())
        if any(request.get(k)!=v for k,v in expected.items()):
            raise ValueError('Replay decoding settings differ from the archived request')
    else:
        request = {**expected,'messages':messages(case_dir, few_shot)}
    key = hashlib.sha256(json.dumps({'base_url':CONFIG.base_url, **request},sort_keys=True).encode()).hexdigest()
    dump(logs/'prompt.json', request)
    response_path = logs/'response.json'
    cached = response_path.exists()
    if cached:
        response = json.loads(response_path.read_text())
        if response['request_hash'] != key:
            raise ValueError('Cached response configuration differs. Use a fresh --output directory.')
    else:
        errors_path = logs/'request_errors.json'
        historical_errors = json.loads(errors_path.read_text()) if errors_path.exists() else []
        attempts = []
        start = time.perf_counter()
        for attempt in range(6):
            try:
                raw = client.chat.completions.with_raw_response.create(**request,
                    extra_headers={'x-obleth-boons':'off'})
                completion = raw.parse()
                response = {'request_hash':key,'base_url':CONFIG.base_url,'completion':completion.model_dump(),
                            'reasoning_effort_header':raw.headers.get('x-obleth-reasoning-effort'),
                            'latency_seconds':time.perf_counter()-start,
                            'api_timeout_seconds':CONFIG.api_timeout,
                            'api_attempts':len(historical_errors)+attempt+1,
                            'retries':historical_errors+attempts}
                dump(response_path, response)
                break
            except Exception as e:
                status = getattr(e,'status_code',None)
                attempts.append({'status':status,'type':type(e).__name__})
                dump(logs/'request_errors.json', historical_errors+attempts)
                transient = status in (429,500,502,503,504) or type(e).__name__ in {'APIConnectionError','APITimeoutError'}
                if not transient or attempt == 5:
                    raise
                time.sleep(min(60,2**attempt*2))
    completion = response['completion']
    records = []
    training = pd.read_csv(case_dir/'training_0.csv', low_memory=False) if consistency else None
    choices = sorted(completion['choices'], key=lambda x:x['index'])
    if len(choices) != request['n']:
        raise ValueError(f'Expected {request["n"]} completions, got {len(choices)}')
    for index, choice in enumerate(choices):
        message = choice['message']
        text = message.get('content') or ''
        (logs/f'completion_{index}.txt').write_text(text)
        record = {'index':index,'finish_reason':choice.get('finish_reason')}
        try:
            code = extract_code(text)
            path = generated/'candidates'/f'{index}.py'
            path.parent.mkdir(exist_ok=True)
            path.write_text(code)
            record['path'] = str(path.relative_to(CONFIG.output))
            if consistency:
                _, record['execution'] = execute(code, training, CONFIG.timeout)
            else:
                record['execution'] = {'status':'not_voted'}
        except Exception as e:
            record['execution'] = {'status':'extraction_error','error':str(e)}
            blocks = re.findall(r'```python\s*\n(.*?)```', text, flags=re.S|re.I)
            if blocks:
                invalid = generated/'candidates'/f'{index}_invalid.py'
                invalid.parent.mkdir(exist_ok=True)
                invalid.write_text(blocks[-1].strip()+'\n')
                record['invalid_code_path'] = str(invalid.relative_to(CONFIG.output))
        records.append(record)
        dump(logs/'candidates.json', records)
    meta = {'request_hash':key,'usage':completion.get('usage',{}),'latency_seconds':response['latency_seconds'],
            'api_attempts':response['api_attempts'],'cached':cached,'candidate_count':len(records),
            'api_timeout_seconds':response.get('api_timeout_seconds',600),
            'reasoning_effort_header':response.get('reasoning_effort_header')}
    if (logs/'interruption.json').exists():
        meta['interruption']=json.loads((logs/'interruption.json').read_text())
        meta['api_attempts']+=meta['interruption'].get('uncounted_requests',0)
    dump(logs/'generation.json', meta)
    if consistency:
        selected, clusters = choose_candidate(records)
    else:
        selected, clusters = 0, {}
        if 'path' not in records[0]:
            raise RuntimeError(records[0]['execution'].get('error'))
    meta.update(selected_index=selected,clusters=clusters)
    dump(logs/'generation.json', meta)
    code = (CONFIG.output/records[selected]['path']).read_text()
    (generated/'transform.py').write_text(code)
    return code
