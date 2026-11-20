import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Mapping for months from abbreviation to full capitalized name
    month_map = {
        'Jan': 'January',
        'Feb': 'February',
        'Mar': 'March',
        'Apr': 'April',
        'May': 'May',
        'Jun': 'June',
        'Jul': 'July',
        'Aug': 'August',
        'Sep': 'September',
        'Oct': 'October',
        'Nov': 'November',
        'Dec': 'December'
    }
    
    # Mapping for day type
    daytype_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Map month
    out['month'] = source['Month'].map(month_map)
    
    # Map day type
    out['day'] = source['Daytype'].map(daytype_map)
    
    # Rename and copy hour columns
    for h in range(1, 25):
        src_col = f"{h}:00"
        tgt_col = f"hr{h}"
        out[tgt_col] = source[src_col]
        
    return out.reset_index(drop=True)
