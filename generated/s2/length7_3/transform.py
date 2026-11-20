import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Mapping for months based on the observed shift in the sample data
    month_map = {
        'Mar': 'September',
        'Apr': 'October',
        'May': 'November',
        'Jun': 'December',
        'Jul': 'January',
        'Aug': 'February'
    }
    
    # Mapping for day types
    day_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    
    # Create the output dataframe
    out = pd.DataFrame()
    
    # Map month and day columns
    out['month'] = source['Month'].map(month_map)
    out['day'] = source['Daytype'].map(day_map)
    
    # Rename and select hour columns
    for h in range(1, 25):
        src_col = f'{h}:00'
        tgt_col = f'hr{h}'
        out[tgt_col] = source[src_col]
        
    return out
