import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse Date and extract Month
    source = source.copy()
    source['dt'] = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    source['month'] = source['dt'].dt.month
    source['month_name'] = source['dt'].dt.strftime('%B').str.lower()
    
    # 2. Melt the hourly columns (1-24)
    # The columns are named "1" through "24"
    melt_cols = [str(i) for i in range(1, 25)]
    df_long = source.melt(
        id_vars=['month', 'month_name'], 
        value_vars=melt_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # 3. Convert hour string to int
    df_long['hour'] = df_long['hour_str'].astype(int)
    
    # 4. Group by hour and month, calculate mean
    # We group by month_name to ensure we get the string names for columns
    grouped = df_long.groupby(['hour', 'month_name'])['value'].mean()
    
    # 5. Pivot to wide format: rows=hour, cols=month_name, values=value
    df_wide = grouped.unstack('month_name')
    
    # 6. Reset index to make 'hour' a column
    df_wide = df_wide.reset_index()
    
    # 7. Ensure column order: hour, january, february, ...
    month_cols = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Select only the months that exist in the data, plus hour
    # But we need to ensure all month columns are present if they are expected in the schema, 
    # even if NaN. The pivot might drop months with no data.
    # Let's reindex the columns to match the target schema order.
    
    # First, ensure all month columns exist
    for m in month_cols:
        if m not in df_wide.columns:
            df_wide[m] = np.nan
            
    # Sort/Select columns
    final_cols = ['hour'] + month_cols
    df_wide = df_wide[final_cols]
    
    # Sort by hour
    df_wide = df_wide.sort_values('hour').reset_index(drop=True)
    
    # Ensure hour is int
    df_wide['hour'] = df_wide['hour'].astype(int)
    
    return df_wide
