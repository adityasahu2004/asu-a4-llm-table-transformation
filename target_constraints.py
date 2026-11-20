"""Generic constraints inferred only from the target's prompt sample.

No case identifiers, evaluation rows, validator scores, or target row counts are
used. Relations are enforced only when the sample identifies one convention.
"""
import re
import warnings
import numpy as np
import pandas as pd

POLICY = {'version':'schema-weekday-v1','pool':'five few-shot SC samples + one greedy few-shot sample',
    'constraints':['exact target schema','uniquely identified date-to-weekday relation'],
    'target_rows':'the same 12-row prompt sample as the baselines',
    'output_rows':'up to 128 evenly spaced training-output rows',
    'selection':'strictly lower lexicographic constraint loss; preserve SC winner on ties',
    'forbidden_inputs':['test_0.csv','validator results','case-specific rules','target row counts']}


def sample_frame(frame, n=128):
    indices=sorted(set(np.linspace(0,max(0,len(frame)-1),min(n,len(frame)),dtype=int)))
    return frame.iloc[indices]


def parsed_dates(series):
    text=series.astype(str)
    if not text.str.contains(r'\b\d{4}\b',regex=True).all():
        return None
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        dates=pd.to_datetime(text,format='mixed',errors='coerce')
    if dates.isna().any() or dates.nunique()<4:
        return None
    return dates


def weekday_values(dates, convention):
    weekday=dates.dt.dayofweek
    return {'monday0':weekday,'monday1':weekday+1,
            'sunday0':(weekday+1)%7,'sunday1':(weekday+1)%7+1}[convention]


def derive_constraints(target_profile):
    sample=pd.DataFrame(target_profile['sample']['data'],columns=target_profile['sample']['columns'])
    relations=[]
    for dow_column in sample:
        canonical=re.sub(r'[^a-z]','',dow_column.lower())
        if canonical not in {'dow','dayofweek','weekday'}:
            continue
        numeric=pd.to_numeric(sample[dow_column],errors='coerce')
        if numeric.isna().any() or numeric.nunique()<4 or not numeric.between(0,7).all():
            continue
        for date_column in sample:
            if date_column==dow_column or not re.search(r'date|cst|dt_',date_column,re.I):
                continue
            dates=parsed_dates(sample[date_column])
            if dates is None:
                continue
            valid=[c for c in ['monday0','monday1','sunday0','sunday1']
                   if (weekday_values(dates,c).to_numpy()==numeric.to_numpy()).all()]
            if len(valid)==1:
                relations.append({'date_column':date_column,'weekday_column':dow_column,
                                  'convention':valid[0],'support_rows':len(sample)})
    return {'columns':sample.columns.tolist(),'relations':relations}


def constraint_loss(output,constraints):
    expected=set(constraints['columns']);actual=set(output.columns)
    schema_errors=len(expected ^ actual)
    sample=sample_frame(output)
    violations=[]
    for relation in constraints['relations']:
        date=relation['date_column'];dow=relation['weekday_column']
        error=1.0
        if date in sample and dow in sample:
            dates=parsed_dates(sample[date])
            numeric=pd.to_numeric(sample[dow],errors='coerce')
            if dates is not None:
                expected_dow=weekday_values(dates,relation['convention'])
                error=float((numeric.isna() | numeric.ne(expected_dow)).mean())
        violations.append({**relation,'violation_fraction':error})
    return (schema_errors,sum(r['violation_fraction'] for r in violations)),violations


def select(records,baseline):
    valid=[r for r in records if r['execution']['status']=='ok']
    if not valid:
        raise RuntimeError('All pooled candidates failed training execution')
    best=min(tuple(r['constraint_loss']) for r in valid)
    baseline_record=next((r for r in valid if r['index']==baseline),None)
    if baseline_record is not None and tuple(baseline_record['constraint_loss'])==best:
        return baseline,'SC winner retained: no strict constraint improvement'
    selected=min(r['index'] for r in valid if tuple(r['constraint_loss'])==best)
    return selected,'Strict target-derived constraint improvement over SC winner'
