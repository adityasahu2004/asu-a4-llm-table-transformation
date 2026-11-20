import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Derive grouping and key columns
    # Month name padded to 10 chars with spaces on the right
    df['month'] = df['dt'].dt.strftime('%B').str.ljust(10)
    
    # Day type: weekday vs weekend
    # dayofweek: Monday=0 ... Sunday=6
    df['daytype'] = df['dt'].dt.dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # Hour 1-24 mapping from 0-23
    df['hour_key'] = df['dt'].dt.hour + 1
    
    # Pivot to get mean values for each hour, grouped by month and daytype
    pivot_df = df.pivot_table(
        index=['month', 'daytype'],
        columns='hour_key',
        values='cerc_logger_1',
        aggfunc='mean'
    )
    
    # Rename columns to hr1, hr2, ... hr24
    pivot_df.columns = [f'hr{int(c)}' for c in pivot_df.columns]
    
    # Reset index to bring grouping keys back to columns
    result = pivot_df.reset_index()
    
    # Ensure column order: month, daytype, hr1...hr24
    # The reset_index puts month, daytype first, then the sorted hour columns.
    # Since hour_key was numeric 1-24, they should be sorted correctly.
    
    return result
