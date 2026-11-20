import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column to ensure consistent formatting
    # Source format is observed as "1/1/2014" -> Target "01/01/2014"
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create the output DataFrame
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map Hr N -> Hour N
    for h in range(1, 25):
        out[f'Hour {h}'] = source[f'Hr {h}']
        
    return out.reset_index(drop=True)
