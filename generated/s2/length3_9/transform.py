import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the output dataframe with the formatted date
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map source hourly columns to target hourly columns
    for h in range(1, 25):
        src_col = f'Hr {h}'
        tgt_col = f'Hour {h}'
        out[tgt_col] = source[src_col]
        
    return out
