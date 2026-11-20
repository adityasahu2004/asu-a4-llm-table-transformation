import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map Month: Add 6 months to the source month name
    # Mar->Sep, Apr->Oct, May->Nov, Jun->Dec, Jul->Jan, Aug->Feb
    month_map = {
        'Mar': 'September',
        'Apr': 'October',
        'May': 'November',
        'Jun': 'December',
        'Jul': 'January',
        'Aug': 'February'
    }
    
    # Map Daytype: WD->weekday, WE->weekend
    daytype_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    
    # Create output dataframe
    out = pd.DataFrame()
    
    # Transform month
    out['month'] = source['Month'].map(month_map)
    
    # Transform daytype
    out['day'] = source['Daytype'].map(daytype_map)
    
    # Rename and select hourly columns
    for h in range(1, 25):
        src_col = f"{h}:00"
        tgt_col = f"hr{h}"
        out[tgt_col] = source[src_col]
        
    return out
