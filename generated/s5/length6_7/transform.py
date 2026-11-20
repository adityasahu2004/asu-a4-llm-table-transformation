import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    out['Date'] = source['Date']
    for h in range(1, 25):
        src_col = f'{h}:00' if h < 24 else '24:00:00'
        out[f'Hr {h}'] = source[src_col]
    return out.reset_index(drop=True)
