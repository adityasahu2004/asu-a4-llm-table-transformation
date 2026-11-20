import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates and shift back by 182 days to match target temporal alignment
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y') - pd.Timedelta(days=182)
    
    # Create output dataframe with cst column
    out = pd.DataFrame(index=source.index)
    out['cst'] = dates.dt.strftime('%a %m/%d/%Y')
    
    # Map Hour N columns to N:00 columns
    for h in range(1, 25):
        out[f'{h}:00'] = source[f'Hour {h}']
        
    return out.reset_index(drop=True)
