import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month'] = source['dt'].dt.month
    
    # 2. Select value columns and melt
    value_cols = [f'value{i}' for i in range(1, 25)]
    melted = source[['dt', 'month'] + value_cols].melt(
        id_vars=['dt', 'month'], 
        value_vars=value_cols, 
        var_name='hour_str', 
        value_name='val'
    )
    
    # 3. Extract hour integer
    melted['hour'] = melted['hour_str'].str.extract(r'(\d+)').astype(int)
    
    # 4. Aggregate mean by hour and month
    agg_df = melted.groupby(['hour', 'month'])['val'].mean().reset_index()
    
    # 5. Pivot to wide format
    pivoted = agg_df.pivot(index='hour', columns='month', values='val')
    
    # 6. Format columns and index
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    # Rename columns based on month names
    pivoted = pivoted.rename(columns=month_names)
    
    # Ensure all 12 month columns exist, filling with NaN if missing
    for m_name in month_names.values():
        if m_name not in pivoted.columns:
            pivoted[m_name] = np.nan
            
    # Select only the required month columns in order
    ordered_months = [month_names[i] for i in range(1, 13)]
    pivoted = pivoted[ordered_months]
    
    # Reset index to make hour a column
    result = pivoted.reset_index()
    result = result.rename(columns={'hour': 'hour'})
    
    # Ensure hour is int64
    result['hour'] = result['hour'].astype('int64')
    
    # Sort by hour to match typical output expectations (1-24)
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result
