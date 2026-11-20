import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse dates and extract month
    source = source.copy()
    source['date'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month'] = source['date'].dt.month
    
    # 2. Identify hour columns and melt
    hour_cols = [col for col in source.columns if col.startswith('Hour ')]
    
    # Extract hour number from column names
    # Create a mapping or just melt and parse
    melted = source.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # Extract integer hour from 'Hour X'
    melted['hour'] = melted['hour_col'].str.extract(r'(\d+)').astype(int)
    melted = melted.drop(columns=['hour_col'])
    
    # 3. Group by hour and month, aggregate
    # Using 'first' to preserve exact values assuming consistency per group
    # If values vary, 'first' is deterministic. 'mean' would create new values.
    agg_df = melted.groupby(['hour', 'month'])['value'].first().reset_index()
    
    # 4. Pivot to wide format
    # Map month numbers to names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    agg_df['month_name'] = agg_df['month'].map(month_names)
    
    # Pivot
    target_df = agg_df.pivot(index='hour', columns='month_name', values='value')
    
    # Ensure all month columns exist, even if empty
    all_months = [month_names[i] for i in range(1, 13)]
    for m in all_months:
        if m not in target_df.columns:
            target_df[m] = np.nan
            
    # Reorder columns
    target_df = target_df[all_months]
    
    # Reset index to make hour a column
    target_df = target_df.reset_index()
    
    # Ensure hour is int64
    target_df['hour'] = target_df['hour'].astype('int64')
    
    # Sort by hour to ensure deterministic order (optional but good practice)
    target_df = target_df.sort_values('hour').reset_index(drop=True)
    
    return target_df
