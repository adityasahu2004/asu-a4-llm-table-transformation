import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    source = source.copy()
    source['datetime'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month'] = source['datetime'].dt.month
    
    # Select hourly columns
    hour_cols = [f'Hour {h}' for h in range(1, 25)]
    
    # Melt the dataframe to long format for easier grouping
    long_df = source.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_label', 
        value_name='value'
    )
    
    # Extract hour number from 'Hour X'
    long_df['hour'] = long_df['hour_label'].str.extract(r'(\d+)').astype(int)
    
    # Group by month and hour, compute mean
    # Using pivot_table to get a wide format: rows=hour, cols=month, values=mean
    pivot_df = long_df.pivot_table(
        index='hour', 
        columns='month', 
        values='value', 
        aggfunc='mean'
    )
    
    # Define target month names
    month_names = [
        'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Create the result dataframe
    result = pd.DataFrame()
    result['hour'] = pivot_df.index.astype(int)
    
    # Map month numbers to names and assign columns
    # Months 1-7 exist in pivot_df, 8-12 do not (will be NaN)
    for i, name in enumerate(month_names, 1):
        if i in pivot_df.columns:
            result[name] = pivot_df[i]
        else:
            result[name] = np.nan
            
    # Ensure correct dtypes
    result['hour'] = result['hour'].astype(int)
    for col in month_names:
        result[col] = result[col].astype(float)
        
    # Sort by hour to match typical output order (though sample is not sorted, 
    # deterministic output usually implies sorted or index-preserving. 
    # The sample output is not sorted by hour (1, 11, 13...), but it's a sample.
    # Standard practice is to sort by the primary key 'hour' for clean output unless specified otherwise.
    # However, looking at the sample: 1, 11, 13, 15, 17, 19, 20, 22, 24, 4, 6, 9.
    # This looks like a random subset or specific selection. 
    # Since the target has 24 rows and distinct hours 1-24, we should return all 24 rows.
    # I will sort by hour for determinism.
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result
