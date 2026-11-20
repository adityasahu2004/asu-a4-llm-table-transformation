import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format to ISO 8601 with time component
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    out = pd.DataFrame(index=source.index)
    out['date'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Rename Hour columns to value columns
    for h in range(1, 25):
        out[f'value{h}'] = source[f'Hour {h}']
        
    return out.reset_index(drop=True)
