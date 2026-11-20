import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = source.copy()
    # Parse date and shift back by 183 days
    dates = pd.to_datetime(out['date'], format='%m/%d/%Y')
    out['date'] = (dates - pd.Timedelta(days=183)).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Rename Hour columns to value columns
    rename_map = {}
    for h in range(1, 25):
        rename_map[f'Hour {h}'] = f'value{h}'
    
    out = out.rename(columns=rename_map)
    
    # Reorder columns to match target: date, then value1...value24
    cols = ['date'] + [f'value{h}' for h in range(1, 25)]
    out = out[cols]
    
    return out.reset_index(drop=True)
