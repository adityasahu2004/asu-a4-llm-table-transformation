import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    out['Date'] = pd.to_datetime(source['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d 00:00:00')
    for h in range(1, 25):
        out[f'Hr {h}'] = source[f'value{h}']
    return out.reset_index(drop=True)
