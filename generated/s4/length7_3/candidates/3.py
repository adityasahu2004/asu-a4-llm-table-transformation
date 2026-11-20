import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Define mapping for months
    month_map = {
        'Mar': 'March',
        'Apr': 'April',
        'May': 'May',
        'Jun': 'June',
        'Jul': 'July',
        'Aug': 'August',
        'Sep': 'September',
        'Oct': 'October',
        'Nov': 'November',
        'Dec': 'December',
        'Jan': 'January',
        'Feb': 'February'
    }
    
    # Define mapping for day types
    day_map = {
        'WD': 'weekday',
        'WE': 'weekend'
    }
    
    # Create the output dataframe
    out = pd.DataFrame()
    
    # Transform Month to full name
    out['month'] = source['Month'].map(month_map)
    
    # Transform Daytype to full name
    out['day'] = source['Daytype'].map(day_map)
    
    # Rename hour columns from "H:00" to "hrH"
    hour_cols = [f'{h}:00' for h in range(1, 25)]
    new_hour_cols = [f'hr{h}' for h in range(1, 25)]
    
    # Select and rename the hour columns
    out[hour_cols] = source[hour_cols]
    out.rename(columns=dict(zip(hour_cols, new_hour_cols)), inplace=True)
    
    # Ensure column order: month, day, hr1...hr24
    final_cols = ['month', 'day'] + new_hour_cols
    out = out[final_cols]
    
    return out
