import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Mapping for months: Source Mar..Aug maps to Target Sep..Feb
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
    
    # Transform 'Month' to 'month'
    out['month'] = source['Month'].map(month_map)
    
    # Transform 'Daytype' to 'day'
    out['day'] = source['Daytype'].map(day_map)
    
    # Transform hourly columns: "1:00" -> "hr1", ..., "24:00" -> "hr24"
    for h in range(1, 25):
        source_col = f"{h}:00"
        target_col = f"hr{h}"
        out[target_col] = source[source_col]
        
    return out
