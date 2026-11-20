import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'])
    
    # Extract date and hour
    df['dt_date'] = df['parsed_date'].dt.date
    df['hour'] = df['parsed_date'].dt.hour
    
    # Aggregate: Mean * 60
    # Group by date and hour, calculate mean of zone_016, then multiply by 60
    agg_df = df.groupby(['dt_date', 'hour'])['zone_016'].mean().reset_index()
    agg_df['zone_016'] = agg_df['zone_016'] * 60
    
    # Pivot
    pivot_df = agg_df.pivot(index='dt_date', columns='hour', values='zone_016')
    
    # Fill NaNs with 0
    pivot_df = pivot_df.fillna(0)
    
    # Rename columns to 1:00 ... 24:00
    # Hour 0 -> 1:00, Hour 1 -> 2:00, ..., Hour 23 -> 24:00
    new_cols = []
    for h in range(24):
        new_cols.append(f"{h+1}:00")
    
    # Ensure all hours 0-23 are present in columns, even if empty in data
    pivot_df = pivot_df.reindex(columns=range(24), fill_value=0)
    pivot_df.columns = new_cols
    
    # Format date index
    pivot_df.index = pd.to_datetime(pivot_df.index).strftime('%a %m/%d/%Y')
    pivot_df.index.name = 'cst'
    
    # Reset index to make 'cst' a column
    result = pivot_df.reset_index()
    
    # Ensure column order
    cols = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    result = result[cols]
    
    return result
