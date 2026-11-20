import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map Month abbreviations to full names shifted by 6 months
    month_map = {
        'Mar': 'September',
        'Apr': 'October',
        'May': 'November',
        'Jun': 'December',
        'Jul': 'January',
        'Aug': 'February'
    }
    
    # Map Daytype
    day_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    
    out = pd.DataFrame()
    out['month'] = source['Month'].map(month_map)
    out['day'] = source['Daytype'].map(day_map)
    
    # Process hourly columns
    for h in range(1, 25):
        src_col = f'{h}:00'
        tgt_col = f'hr{h}'
        # Transformation observed: target = source - 0.1
        out[tgt_col] = source[src_col] - 0.1
        
    return out
