import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    out['date'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    for h in range(1,25):
        out[f'Hour {h}'] = source[f'PCT_HOURLY_{h:02d}00']
    return out.reset_index(drop=True)
