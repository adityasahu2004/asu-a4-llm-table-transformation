import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date string to datetime
    # Format observed: "1/2/2018 0:11" -> month/day/year hour:minute
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract calendar date and hour
    df['cal_date'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour 0-23 to "Hour 1" - "Hour 24"
    df['hour_label'] = 'Hour ' + (df['hour'] + 1).astype(str)
    
    # Pivot table
    # Index: cal_date, Columns: hour_label, Values: zone_016
    pivot_df = df.pivot_table(
        index='cal_date',
        columns='hour_label',
        values='zone_016',
        aggfunc='first'
    )
    
    # Ensure all 24 columns exist
    expected_cols = [f'Hour {i}' for i in range(1, 25)]
    for col in expected_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # Reorder columns
    pivot_df = pivot_df[expected_cols]
    
    # Convert index to datetime for sorting, then reset to string
    pivot_df.index = pd.to_datetime(pivot_df.index)
    
    # Sort by date descending
    pivot_df = pivot_df.sort_index(ascending=False)
    
    # Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'index': 'date'})
    
    # Format date as MM/DD/YYYY
    pivot_df['date'] = pivot_df['date'].dt.strftime('%m/%d/%Y')
    
    return pivot_df
