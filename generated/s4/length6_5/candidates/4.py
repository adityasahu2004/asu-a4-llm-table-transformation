import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates and format to MM/DD/YYYY
    dates = pd.to_datetime(source['Date'])
    out = pd.DataFrame()
    out['Date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Map source columns '1'...'24' to 'Hr 1'...'Hr 24'
    for h in range(1, 25):
        out[f'Hr {h}'] = source[str(h)]
        
    return out.reset_index(drop=True)
