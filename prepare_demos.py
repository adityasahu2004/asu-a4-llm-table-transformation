"""Author fixed demonstrations only; these are never scored as evaluation cases."""
import argparse
import json
from pathlib import Path
from config import ROOT, DEMO_CASES
from prompting import case_block

CODES = {
'length1_1': '''import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    out['cst'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y').dt.strftime('%a %m/%d/%Y')
    for h in range(1,25):
        out[f'{h}:00'] = source[f'PCT_HOURLY_{h:02d}00']
    return out.reset_index(drop=True)
''',
'length2_1': '''import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['dt_strata'] = dates.dt.strftime('%m/%d/%Y')
    out['dow'] = dates.dt.dayofweek + 1
    for h in range(1,25):
        name = f'{h}:00' if h < 24 else '24:00:00'
        out[f'pct_hourly_{h:02d}00'] = pd.to_numeric(source[name], errors='coerce')
    out['pct_hourly_2500'] = 0
    return out.reset_index(drop=True)
''',
'length3_1': '''import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    out['date'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    for h in range(1,25):
        out[f'Hour {h}'] = source[f'PCT_HOURLY_{h:02d}00']
    return out.reset_index(drop=True)
'''}
PLANS = {
'length1_1':'Project the 24 hourly measurements; rename them to hour labels; format DT_STRATA as weekday plus MM/DD/YYYY for cst. Preserve rows and measurement values.',
'length2_1':'Parse CST; format dt_strata; derive ISO day of week (Monday=1 through Sunday=7); rename the 24 hour columns to pct_hourly labels and append the structural 25th-hour zero column.',
'length3_1':'Drop identifier, Strata, DOW and the 25th hour; format DT_STRATA as MM/DD/YYYY; project and rename the 24 measurements to Hour 1 through Hour 24.'}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--benchmark',type=Path,default=ROOT.parent)
    args = p.parse_args()
    demos = []
    directory = ROOT/'demos'
    directory.mkdir(exist_ok=True)
    (directory/'split.json').write_text(json.dumps({'held_out':DEMO_CASES,'shown':list(CODES),
        'note':'All five excluded from every headline denominator; three worked examples shown.'},indent=2))
    for case, code in CODES.items():
        (directory/f'{case}.py').write_text(code)
        demos.append({'case':case,'prompt':'Infer the transformation from this schema/sample block:\n'+case_block(args.benchmark/case),
                      'completion':'Operator plan: '+PLANS[case]+'\n\n```python\n'+code+'```'})
    (directory/'demonstrations.json').write_text(json.dumps(demos,indent=2))
    print('Prepared three worked demonstrations; fixed holdout contains five cases.')

if __name__ == '__main__':
    main()
