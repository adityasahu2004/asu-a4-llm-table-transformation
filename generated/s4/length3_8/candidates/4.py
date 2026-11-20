import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse CST to datetime. Format is "%a %m/%d/%Y" (e.g., "Sat 12/01/2012")
    # We only need the date part for the output column.
    dates = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    out = pd.DataFrame(index=source.index)
    out['date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Map source hour columns to target hour columns
    # Source: "1:00", "2:00", ..., "23:00", "24:00:00"
    # Target: "Hour 1", "Hour 2", ..., "Hour 23", "Hour 24"
    for h in range(1, 25):
        src_col = f'{h}:00' if h < 24 else '24:00:00'
        tgt_col = f'Hour {h}'
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
