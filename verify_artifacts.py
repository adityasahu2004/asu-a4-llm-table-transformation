"""Check completeness, prompt fairness, selected-code provenance and secrets."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from config import ROOT, DEMO_CASES
from prompting import extract_code
from summarize import read_results
from target_constraints import derive_constraints,select
from strategies.common import choose_candidate

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--benchmark',type=Path,default=ROOT.parent)
    args=p.parse_args()
    cases={p.name for p in args.benchmark.glob('length*_*') if p.is_dir()}
    assert len(cases)==105,f'Expected 105 benchmark cases, found {len(cases)}'
    results=read_results(ROOT)
    prompts={}
    for s in ('s1','s2','s4','s5'):
        by_case={r['case']:r for r in results.get(s,[])}
        assert set(by_case)==cases,f'{s}: incomplete case set'
        assert sum(not r['is_demo'] for r in by_case.values())==100
        prompts[s]={}
        for case,r in by_case.items():
            assert r['is_demo']==(case in DEMO_CASES)
            assert r['model']=='qwen36-27b'
            folder=ROOT/'logs'/s/case
            request=json.loads((folder/'prompt.json').read_text())
            response=json.loads((folder/'response.json').read_text())
            generation=json.loads((folder/'generation.json').read_text())
            if s=='s5':
                assert response['kind']=='pooled_raw_api_responses'
                assert len(response['pools'])==2
                candidates=json.loads((folder/'candidates.json').read_text())
                assert len(candidates)==6
                pool_choices=[]
                for pool in response['pools']:
                    req=pool['request'];res=pool['response'];is_sc=pool['strategy']=='s4'
                    assert req['model']=='qwen36-27b' and req['max_tokens']==6000 and req['reasoning_effort']=='none'
                    assert req['n']==(5 if is_sc else 1) and req['temperature']==(0.7 if is_sc else 0)
                    key=hashlib.sha256(json.dumps({'base_url':res['base_url'],**req},sort_keys=True).encode()).hexdigest()
                    assert key==res['request_hash']
                    pool_choices.extend(sorted(res['completion']['choices'],key=lambda c:c['index']))
                assert response['pools'][0]['request']['messages']==response['pools'][1]['request']['messages']
                assert response['pools'][0]['request']['messages']==prompts['s2'][case]
                chosen=ROOT/'generated'/s/case/'transform.py'
                assert chosen.read_text()==extract_code(pool_choices[generation['selected_index']]['message']['content'])
                target=json.loads(response['pools'][0]['request']['messages'][-1]['content'].split(':\n',1)[1])['target']
                assert derive_constraints(target)==generation['constraints']
                baseline=choose_candidate(candidates[:5])[0]
                assert select(candidates,baseline)[0]==generation['selected_index']
                continue
            assert request['model']=='qwen36-27b'
            assert request['max_tokens']==6000 and request['reasoning_effort']=='none'
            assert request['temperature']==(0.7 if s=='s4' else 0)
            assert request['n']==(5 if s=='s4' else 1)
            key=hashlib.sha256(json.dumps({'base_url':response['base_url'],**request},sort_keys=True).encode()).hexdigest()
            assert response['request_hash']==key
            assert len(response['completion']['choices'])==request['n']
            prompts[s][case]=request['messages']
            chosen=ROOT/'generated'/s/case/'transform.py'
            if chosen.exists():
                index=generation['selected_index']
                choice=sorted(response['completion']['choices'],key=lambda c:c['index'])[index]
                assert chosen.read_text()==extract_code(choice['message']['content'])
            if r['execution']['status']=='ok':
                assert chosen.exists()
                assert 'PROVISIONAL' not in r.get('hard_match_provenance','')
    for case in cases:
        assert prompts['s2'][case]==prompts['s4'][case],f'Few-shot prompts differ: {case}'
        assert prompts['s1'][case][0]==prompts['s2'][case][0]
        assert prompts['s1'][case][-1]==prompts['s2'][case][-1]
    for directory in ('logs','generated','demos','results'):
        for path in (ROOT/directory).rglob('*'):
            if path.is_file() and path.suffix in {'.py','.json','.jsonl','.txt'}:
                assert not re.search(r'obl_[A-Za-z0-9]{20,}',path.read_text()),f'Credential pattern in {path}'
    frozen=json.loads((ROOT/'results'/'s5_policy.json').read_text())
    for name,digest in frozen['implementation_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'Fourth-strategy policy changed after freeze'
    print('Verified: 420 case records, 400 evaluation cases, fixed baseline prompts/model, pooled-code provenance, frozen s5 policy, no credential patterns.')

if __name__=='__main__':
    main()
