import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # Extract month name
    df['month'] = df['date_parsed'].dt.strftime('%B')
    
    # Extract daytype: weekday or weekend
    # dayofweek: 0=Mon, ..., 5=Sat, 6=Sun
    df['daytype'] = df['date_parsed'].dt.dayofweek.apply(
        lambda x: 'weekend' if x >= 5 else 'weekday'
    )
    
    # Rename hour columns from "Hour N" to "hrN"
    rename_map = {f'Hour {i}': f'hr{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # Sort by the original date to ensure chronological order
    df = df.sort_values(by='date_parsed')
    
    # Select the target columns in the correct order
    # month, daytype, hr1...hr24
    hour_cols = [f'hr{i}' for i in range(1, 25)]
    final_cols = ['month', 'daytype'] + hour_cols
    
    result = df[final_cols].reset_index(drop=True)
    
    return result
