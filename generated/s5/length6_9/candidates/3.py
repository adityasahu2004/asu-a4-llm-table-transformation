import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column into datetime objects
    df['dt'] = pd.to_datetime(df['date'])
    
    # Extract the date as a string in MM/DD/YYYY format
    df['Date'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # Extract the hour from the datetime (0-23)
    df['Hour'] = df['dt'].dt.hour
    
    # Pivot the data: rows are Dates, columns are Hours, values are zone_016
    pivot = df.pivot(index='Date', columns='Hour', values='zone_016')
    
    # Ensure all hours from 0 to 23 are present as columns, filling missing ones with NaN
    all_hours = pd.RangeIndex(0, 24)
    pivot = pivot.reindex(columns=all_hours, fill_value=float('nan'))
    
    # Rename the columns to 'Hr 1' through 'Hr 24'
    pivot.columns = [f'Hr {h+1}' for h in range(24)]
    
    # Reset index to move 'Date' back to a column
    result = pivot.reset_index()
    
    # Preserve the order of dates as they first appeared in the source
    unique_dates = df['Date'].drop_duplicates().tolist()
    result = result.set_index('Date').reindex(unique_dates).reset_index()
    
    return result
