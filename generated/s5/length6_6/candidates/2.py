import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and shift back by 182 days to match target range starting 2015-01-01
    # Source starts 7/3/2015. 7/3/2015 - 182 days = 1/1/2015.
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y') - pd.Timedelta(days=182)
    
    out = pd.DataFrame(index=source.index)
    out['Date'] = dates.dt.strftime('%Y-%m-%d 00:00:00')
    
    for h in range(1, 25):
        out[f'Hr {h}'] = source[f'Hour {h}']
        
    return out.reset_index(drop=True)
