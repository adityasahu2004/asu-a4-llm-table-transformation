import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    source = source.copy()
    source['datetime'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    source['date_only'] = source['datetime'].dt.date
    source['hour'] = source['datetime'].dt.hour
    
    # Pivot the data
    # We want rows to be dates, columns to be hours 1-24
    # Source hour 0 corresponds to Hr 1, hour 1 to Hr 2, etc.
    
    # Create a pivot table
    # Index: date_only, Columns: hour (0-23), Values: zone_016_cooling_sp
    pivot_df = source.pivot_table(index='date_only', columns='hour', values='zone_016_cooling_sp')
    
    # Reindex columns to ensure all 24 hours (0-23) are present, filling missing with NaN
    pivot_df = pivot_df.reindex(columns=range(24), fill_value=np.nan)
    
    # Rename columns to Hr 1 ... Hr 24
    pivot_df.columns = [f'Hr {h+1}' for h in range(24)]
    
    # Reset index to make date_only a column
    result = pivot_df.reset_index()
    
    # Format the date column as MM/dd/yyyy
    result['Date'] = result['date_only'].apply(lambda x: x.strftime('%m/%d/%Y') if pd.notnull(x) else np.nan)
    
    # Select and order columns
    cols = ['Date'] + [f'Hr {h}' for h in range(1, 25)]
    result = result[cols]
    
    return result
