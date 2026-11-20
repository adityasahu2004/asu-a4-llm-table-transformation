import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the source date column
    dt = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Format the date for the target column 'date'
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%m/%d/%Y')
    
    # Map source columns "1" through "24" to "Hour 1" through "Hour 24"
    for h in range(1, 25):
        out[f'Hour {h}'] = source[str(h)]
        
    return out.reset_index(drop=True)
