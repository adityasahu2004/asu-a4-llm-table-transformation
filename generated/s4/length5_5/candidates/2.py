import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying source
    df = source.copy()
    
    # Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # Extract date string in MM/DD/YYYY format
    df['date_only'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # Extract hour (0-23)
    df['hour'] = df['dt'].dt.hour
    
    # Group by date and hour, aggregate the value
    # Using 'first' to handle potential duplicates within an hour
    agg_df = df.groupby(['date_only', 'hour'])['zone_016_cooling_sp'].first().reset_index()
    
    # Pivot the table
    pivot_df = agg_df.pivot(index='date_only', columns='hour', values='zone_016_cooling_sp')
    
    # Rename columns to value1...value24
    # Mapping hour 0 -> value1, hour 1 -> value2, ..., hour 23 -> value24
    pivot_df.columns = [f'value{h+1}' for h in pivot_df.columns]
    
    # Ensure all 24 columns are present, even if empty for some dates
    expected_cols = [f'value{i}' for i in range(1, 25)]
    pivot_df = pivot_df.reindex(columns=expected_cols)
    
    # Reset index to make 'date_only' a column
    pivot_df = pivot_df.reset_index()
    
    # Rename the date column to 'date'
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    return pivot_df
