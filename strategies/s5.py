"""Custom strategy: target-constraint reranking of a fixed six-program LLM pool.

The pool reuses identical s2/s4 API requests when available. A cold run issues
those same requests. Selection never reads test data or previous validation.
"""
import hashlib
import json
from pathlib import Path
import re
import time
import pandas as pd
from config import CONFIG
from execution import execute
from prompting import messages,extract_code
from strategies.common import dump,choose_candidate
from target_constraints import POLICY,derive_constraints,constraint_loss,select


def acquire(case_dir,client,model,strategy,logs):
    original=CONFIG.output/'logs'/strategy/case_dir.name
    own_prompt=logs/f'{strategy}_prompt.json';own_response=logs/f'{strategy}_response.json'
    inherited=0.0;marginal=0;interruption=None
    if own_response.exists():
        request=json.loads(own_prompt.read_text());response=json.loads(own_response.read_text())
        inherited=response['latency_seconds']
    elif (original/'response.json').exists():
        request=json.loads((original/'prompt.json').read_text())
        response=json.loads((original/'response.json').read_text())
        inherited=response['latency_seconds']
    else:
        if CONFIG.replay_only:
            raise RuntimeError('No cached pool response; replay never calls the API')
        request={'model':model,'temperature':0.7 if strategy=='s4' else 0,
            'n':5 if strategy=='s4' else 1,'max_tokens':CONFIG.max_tokens,
            'reasoning_effort':CONFIG.reasoning_effort,'messages':messages(case_dir,True)}
        start=time.perf_counter();errors=[]
        for attempt in range(6):
            marginal+=1
            try:
                raw=client.chat.completions.with_raw_response.create(**request,extra_headers={'x-obleth-boons':'off'})
                response={'request_hash':hashlib.sha256(json.dumps({'base_url':CONFIG.base_url,**request},sort_keys=True).encode()).hexdigest(),
                    'base_url':CONFIG.base_url,'completion':raw.parse().model_dump(),
                    'latency_seconds':time.perf_counter()-start,'api_attempts':attempt+1,
                    'reasoning_effort_header':raw.headers.get('x-obleth-reasoning-effort'),
                    'api_timeout_seconds':CONFIG.api_timeout,'retries':errors}
                break
            except Exception as e:
                status=getattr(e,'status_code',None)
                errors.append({'type':type(e).__name__,'status':status})
                dump(logs/f'{strategy}_request_errors.json',errors)
                if attempt==5 or not (status in (429,500,502,503,504) or type(e).__name__ in {'APIConnectionError','APITimeoutError'}):
                    raise
                time.sleep(min(60,2**attempt*2))
    expected={'model':model,'temperature':0.7 if strategy=='s4' else 0,'n':5 if strategy=='s4' else 1,
              'max_tokens':CONFIG.max_tokens,'reasoning_effort':CONFIG.reasoning_effort}
    if any(request.get(k)!=v for k,v in expected.items()):
        raise ValueError('Pool configuration mismatch')
    key=hashlib.sha256(json.dumps({'base_url':CONFIG.base_url,**request},sort_keys=True).encode()).hexdigest()
    if response['request_hash']!=key:
        raise ValueError('Pool request hash mismatch')
    own_interruption=logs/f'{strategy}_interruption.json'
    if own_interruption.exists():interruption=json.loads(own_interruption.read_text())
    elif (original/'interruption.json').exists():interruption=json.loads((original/'interruption.json').read_text())
    if interruption:dump(own_interruption,interruption)
    dump(own_prompt,request);dump(own_response,response)
    return {'strategy':strategy,'request':request,'response':response,
            'inherited_api_seconds':inherited,'marginal_api_attempts':marginal,'interruption':interruption}


def generate(case_dir,client,model):
    case_dir=Path(case_dir);logs=CONFIG.output/'logs'/'s5'/case_dir.name
    generated=CONFIG.output/'generated'/'s5'/case_dir.name
    (generated/'candidates').mkdir(parents=True,exist_ok=True);logs.mkdir(parents=True,exist_ok=True)
    pools=[acquire(case_dir,client,model,s,logs) for s in ['s4','s2']]
    if pools[0]['request']['messages']!=pools[1]['request']['messages']:
        raise ValueError('Pool prompts must be identical')
    profile=json.loads(pools[0]['request']['messages'][-1]['content'].split(':\n',1)[1])['target']
    constraints=derive_constraints(profile)
    dump(logs/'prompt.json',{'model':model,'policy':POLICY,'stages':[p['request'] for p in pools]})
    dump(logs/'response.json',{'kind':'pooled_raw_api_responses','pools':pools})
    training=pd.read_csv(case_dir/'training_0.csv',low_memory=False)
    records=[]
    for pool_index,pool in enumerate(pools):
        for choice in sorted(pool['response']['completion']['choices'],key=lambda c:c['index']):
            index=len(records);content=choice['message'].get('content') or ''
            (logs/f'completion_{index}.txt').write_text(content)
            record={'index':index,'pool_index':pool_index,'provider_index':choice['index'],
                    'finish_reason':choice.get('finish_reason')}
            try:
                code=extract_code(content);path=generated/'candidates'/f'{index}.py';path.write_text(code)
                record['path']=str(path.relative_to(CONFIG.output))
                output,record['execution']=execute(code,training,CONFIG.timeout)
                if output is not None:
                    loss,details=constraint_loss(output,constraints)
                    record.update(constraint_loss=list(loss),constraint_diagnostics=details)
            except Exception as e:
                record['execution']={'status':'extraction_error','error':str(e)}
            records.append(record);dump(logs/'candidates.json',records)
    try:baseline,clusters=choose_candidate(records[:5])
    except RuntimeError:baseline=None;clusters={}
    chosen,reason=select(records,baseline)
    usage={k:sum((p['response']['completion'].get('usage') or {}).get(k,0) or 0 for p in pools)
           for k in ['prompt_tokens','completion_tokens','total_tokens']}
    interrupted=[p['interruption'] for p in pools if p['interruption']]
    meta={'candidate_count':len(records),'selected_index':chosen,'baseline_index':baseline,
          'selection_reason':reason,'constraints':constraints,'policy':POLICY,
          'usage':usage,'api_attempts':sum(p['response']['api_attempts']+(p['interruption'] or {}).get('uncounted_requests',0) for p in pools),
          'marginal_api_attempts':sum(p['marginal_api_attempts'] for p in pools),
          'latency_seconds':sum(p['response']['latency_seconds'] for p in pools),
          'inherited_api_seconds':sum(p['inherited_api_seconds'] for p in pools),
          'clusters':clusters,'cost_basis':'standalone logical pool cost; reused requests have zero marginal API cost'}
    if interrupted:meta['interruption']={'inherited':interrupted,'calendar_wait_seconds':sum(x.get('calendar_wait_seconds',0) for x in interrupted)}
    dump(logs/'generation.json',meta)
    code=(CONFIG.output/records[chosen]['path']).read_text()
    (generated/'transform.py').write_text(code)
    return code
