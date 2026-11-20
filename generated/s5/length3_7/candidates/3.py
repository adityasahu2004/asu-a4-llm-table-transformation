import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date and format it
    dt = pd.to_datetime(source['Date'])
    
    # Create the output dataframe
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map the numeric hour columns to the target names
    for h in range(1, 25):
        out[f'Hour {h}'] = source[str(h)]
        
    return out.reset_index(drop=True)
