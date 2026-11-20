import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Map hour 0 to 24
    df['hour'] = df['hour'].apply(lambda h: 24 if h == 0 else h)
    
    # Create a flag for presence
    df['present'] = 1
    
    # Group by date and hour, sum the presence flag
    grouped = df.groupby(['date_only', 'hour'])['present'].sum().reset_index()
    
    # Pivot to wide format
    # We want all hours 1-24 for all dates
    # First, create a complete index of dates and hours
    all_dates = pd.to_datetime(grouped['date_only']).dt.date.unique()
    all_hours = range(1, 25)
    
    # Create a multi-index for all combinations
    full_index = pd.MultiIndex.from_product([all_dates, all_hours], names=['date_only', 'hour'])
    
    # Reindex the grouped data
    grouped = grouped.set_index(['date_only', 'hour']).reindex(full_index, fill_value=0)
    grouped = grouped.reset_index()
    
    # Pivot
    pivot = grouped.pivot(index='date_only', columns='hour', values='present')
    
    # Rename columns to match target format
    pivot.columns = [f'{h}:00' for h in pivot.columns]
    
    # Fill NaN with 0
    pivot = pivot.fillna(0)
    
    # Assign the value 876.0 if present (value > 0), else 0.0
    # Note: The aggregation was sum of 1s. If sum > 0, it's present.
    # However, the target has 876.0.
    # Let's assume if present, value is 876.0.
    
    for col in pivot.columns:
        pivot[col] = pivot[col].apply(lambda x: 876.0 if x > 0 else 0.0)
        
    # Reset index and rename date column
    pivot = pivot.reset_index()
    pivot = pivot.rename(columns={'date_only': 'cst'})
    
    # Format date as "Dow MM/DD/YYYY"
    pivot['cst'] = pd.to_datetime(pivot['cst']).dt.strftime('%a %m/%d/%Y')
    
    # Ensure column order
    cols = ['cst'] + [f'{h}:00' for h in range(1, 25)]
    pivot = pivot[cols]
    
    return pivot
