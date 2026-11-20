import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column to datetime
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the output dataframe with the formatted date column
    out = pd.DataFrame()
    out['cst'] = dt.dt.strftime('%a %m/%d/%Y')
    
    # Map the 24 hourly columns from source to target names
    for h in range(1, 25):
        src_col = f'Hr {h}'
        tgt_col = f'{h}:00'
        out[tgt_col] = source[src_col].astype('float64')
        
    return out.reset_index(drop=True)
