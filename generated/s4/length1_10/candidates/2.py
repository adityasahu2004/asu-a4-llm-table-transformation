import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    dt = pd.to_datetime(source['date'])
    
    # Extract date for grouping
    date_part = dt.dt.date
    
    # Extract hour and map 0 to 24
    hour = dt.dt.hour
    hour = hour.replace(0, 24)
    
    # Map the cooling setpoint to 876.0 or 0.0
    # 84.0 -> 876.0, else (73.0, null) -> 0.0
    value = np.where(source['zone_016_cooling_sp'] == 84.0, 876.0, 0.0)
    
    # Create a DataFrame for aggregation
    df_agg = pd.DataFrame({
        'date': date_part,
        'hour': hour,
        'value': value
    })
    
    # Group by date and hour, then take the mean
    grouped = df_agg.groupby(['date', 'hour'])['value'].mean().reset_index()
    
    # Pivot to wide format
    pivot = grouped.pivot(index='date', columns='hour', values='value').reset_index()
    
    # Fill NaNs with 0.0
    pivot = pivot.fillna(0.0)
    
    # Rename columns to match target format
    # The index column 'date' should be renamed to 'cst' and formatted
    pivot['cst'] = pd.to_datetime(pivot['date']).dt.strftime('%a %m/%d/%Y')
    
    # Select and rename hour columns
    # Hours are 1 to 24
    hour_cols = [str(h) for h in range(1, 25)]
    
    # Ensure all hour columns exist, filling with 0 if missing
    for h in hour_cols:
        if h not in pivot.columns:
            pivot[h] = 0.0
            
    pivot = pivot[['cst'] + hour_cols]
    
    # Rename columns to "1:00", "2:00", etc.
    pivot.columns = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    
    # Sort by the underlying date
    pivot['date_sort'] = pd.to_datetime(pivot['cst'].str.extract(r'(\d{2}/\d{2}/\d{4})').squeeze())
    pivot = pivot.sort_values('date_sort').drop(columns=['date_sort']).reset_index(drop=True)
    
    return pivot
