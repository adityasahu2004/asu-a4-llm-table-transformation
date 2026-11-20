import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month_num'] = source['dt'].dt.month
    source['hour'] = source['dt'].dt.hour + 1  # 1-24

    # Melt the value columns
    value_cols = [f'value{i}' for i in range(1, 25)]
    long_df = source.melt(
        id_vars=['month_num', 'hour'],
        value_vars=value_cols,
        var_name='value_col',
        value_name='val'
    )
    
    # Extract hour from value_col name if needed, but we already have hour from date
    # Actually, the problem implies the values correspond to the hours of the day for that date.
    # The sample target has specific hours (1, 11, 13, etc.) which suggests we are aggregating across days.
    # The target has 24 rows, one for each hour of the day.
    # The columns are months.
    
    # Group by hour and month_num and take the mean
    agg_df = long_df.groupby(['hour', 'month_num'])['val'].mean().reset_index()
    
    # Pivot to get months as columns
    pivot_df = agg_df.pivot_table(index='hour', columns='month_num', values='val', aggfunc='mean')
    
    # Rename columns to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivot_df.rename(columns=month_names, inplace=True)
    
    # Ensure all month columns exist, even if empty (NaN)
    for m_name in month_names.values():
        if m_name not in pivot_df.columns:
            pivot_df[m_name] = np.nan
            
    # Reorder columns
    month_order = [month_names[i] for i in range(1, 13)]
    pivot_df = pivot_df[month_order]
    
    # Reset index to make hour a column
    pivot_df.reset_index(inplace=True)
    
    # Ensure hour is int64
    pivot_df['hour'] = pivot_df['hour'].astype('int64')
    
    # Reorder columns to match target: hour, then months
    final_cols = ['hour'] + month_order
    pivot_df = pivot_df[final_cols]
    
    return pivot_df
