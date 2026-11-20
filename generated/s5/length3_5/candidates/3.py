import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    out['date'] = pd.to_datetime(source['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    for h in range(1, 25):
        out[f'Hour {h}'] = source[f'value{h}']
    return out.reset_index(drop=True)
