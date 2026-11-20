import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dates = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Create the output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Format CST column
    out['cst'] = dates.dt.strftime('%a %m/%d/%Y')
    
    # Map value1...value24 to 1:00...24:00
    for h in range(1, 25):
        out[f'{h}:00'] = source[f'value{h}']
        
    return out.reset_index(drop=True)
