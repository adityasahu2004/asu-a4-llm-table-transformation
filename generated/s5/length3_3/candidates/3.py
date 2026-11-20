import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date string: "1/2/2018 0:11" -> datetime
    src = source.copy()
    src['datetime'] = pd.to_datetime(src['date'], format='%m/%d/%Y %H:%M')
    
    # Extract calendar date and hour
    src['cal_date'] = src['datetime'].dt.date
    src['hour'] = src['datetime'].dt.hour
    
    # Map hour to 1-24 index for column naming
    # Hour 0 -> 24, Hour 1 -> 1, ..., Hour 23 -> 23
    src['hour_idx'] = src['hour'].apply(lambda h: 24 if h == 0 else h)
    
    # Pivot table
    # index: cal_date, columns: hour_idx, values: zone_016
    pivot = src.pivot_table(
        index='cal_date', 
        columns='hour_idx', 
        values='zone_016', 
        aggfunc='first'
    )
    
    # Rename columns to "Hour 1", "Hour 2", ..., "Hour 24"
    pivot.columns = [f'Hour {h}' for h in pivot.columns]
    
    # Reset index to make cal_date a column
    pivot = pivot.reset_index()
    
    # Rename cal_date to date and format as MM/DD/YYYY
    pivot = pivot.rename(columns={'cal_date': 'date'})
    pivot['date'] = pd.to_datetime(pivot['date']).dt.strftime('%m/%d/%Y')
    
    # Ensure all 24 hour columns are present, filling missing with NaN
    expected_cols = [f'Hour {h}' for h in range(1, 25)]
    for col in expected_cols:
        if col not in pivot.columns:
            pivot[col] = np.nan
            
    # Select only the required columns in the correct order
    result = pivot[['date'] + expected_cols]
    
    # Sort by date descending to match target sample order (latest date first)
    result['date_dt'] = pd.to_datetime(result['date'])
    result = result.sort_values('date_dt', ascending=False).drop(columns=['date_dt'])
    
    return result.reset_index(drop=True)
