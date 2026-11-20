"""Generate empirical evidence for the manually reviewed analysis.json."""
import json
from collections import Counter
from config import ROOT
from summarize import read_results,aggregate

def main():
    data=read_results(ROOT)
    evaluation={s:{r['case']:r for r in rows if not r['is_demo']} for s,rows in data.items()}
    common=set(evaluation.get('s2',{})) & set(evaluation.get('s4',{}))
    help_cases=[]
    hurt_cases=[]
    agree_correct=[]
    agree_wrong=[]
    for case in sorted(common):
        a=evaluation['s2'][case]['autopipeline']['is_correct']
        b=evaluation['s4'][case]['autopipeline']['is_correct']
        (agree_correct if a and b else help_cases if b else hurt_cases if a else agree_wrong).append(case)
    evidence={'paired_s2_s4':{'common':len(common),'s4_helps':help_cases,'s4_hurts':hurt_cases,
              'both_correct':agree_correct,'both_wrong':agree_wrong},'strategies':{}}
    hard_pairs={'common':len(common),'s4_helps':[],'s4_hurts':[],'both_correct':[],'both_wrong':[]}
    for case in sorted(common):
        a=evaluation['s2'][case]['hard_match']['is_correct']
        b=evaluation['s4'][case]['hard_match']['is_correct']
        group='both_correct' if a and b else 's4_helps' if b else 's4_hurts' if a else 'both_wrong'
        hard_pairs[group].append(case)
    evidence['paired_s2_s4_hard_match']=hard_pairs
    if 's5' in evaluation:
        pairs={}
        for metric in ('autopipeline','hard_match'):
            groups={'s5_helps':[],'s5_hurts':[],'both_correct':[],'both_wrong':[]}
            for case in sorted(set(evaluation['s4']) & set(evaluation['s5'])):
                a=evaluation['s4'][case][metric]['is_correct'];b=evaluation['s5'][case][metric]['is_correct']
                key='both_correct' if a and b else 's5_helps' if b else 's5_hurts' if a else 'both_wrong'
                groups[key].append(case)
            pairs[metric]=groups
        evidence['paired_s4_s5']=pairs
    for s,by_case in evaluation.items():
        rows=list(by_case.values())
        failures=[]
        for r in rows:
            if not r['autopipeline']['is_correct'] or not r['hard_match']['is_correct']:
                failures.append({'case':r['case'],'execution':r['execution'],
                    'autopipeline':r['autopipeline'],'hard_match':r['hard_match'],
                    'code_path':f'generated/{s}/{r["case"]}/transform.py'})
        votes=Counter()
        truncated=0
        candidate_statuses=Counter()
        for r in rows:
            clusters=r.get('generation',{}).get('clusters',{})
            if clusters:
                votes[max(len(g) for g in clusters.values())]+=1
            folder=ROOT/'logs'/s/r['case']
            response_path=folder/'response.json'
            if response_path.exists():
                response=json.loads(response_path.read_text())
                completions=([p['response']['completion'] for p in response['pools']]
                    if response.get('kind')=='pooled_raw_api_responses' else [response['completion']])
                truncated+=sum(c.get('finish_reason')=='length' for completion in completions for c in completion['choices'])
            candidates_path=folder/'candidates.json'
            if candidates_path.exists():
                candidates=json.loads(candidates_path.read_text())
                candidate_statuses.update(c['execution']['status'] for c in candidates)
        evidence['strategies'][s]={'metrics':aggregate(rows),
            'official_failure_families':{
                'generation_or_selection_failure':sum(r['execution']['status']=='generation_error' for r in rows),
                'runtime_or_constraint_failure':sum(r['execution']['status'] not in {'ok','generation_error'} for r in rows),
                'executes_but_official_mismatch':sum(r['execution']['status']=='ok' and not r['autopipeline']['is_correct'] for r in rows)},
            'execution_status_counts':dict(Counter(r['execution']['status'] for r in rows)),
            'largest_vote_size_counts':dict(votes),'truncated_completions':truncated,
            'candidate_status_counts':dict(candidate_statuses),
            'auto_only_passes':sum(r['autopipeline']['is_correct'] and not r['hard_match']['is_correct'] for r in rows),
            'hard_only_passes':sum(r['hard_match']['is_correct'] and not r['autopipeline']['is_correct'] for r in rows),
            'schema_mismatch_cases':[r['case'] for r in rows if r['execution']['status']=='ok' and not r.get('exact_schema')],
            'official_pass_with_schema_mismatch':[r['case'] for r in rows if r['autopipeline']['is_correct'] and not r.get('exact_schema')],
            'failures':failures}
    path=ROOT/'results'/'analysis_evidence.json'
    path.write_text(json.dumps(evidence,indent=2))
    print(path)

if __name__=='__main__':
    main()
