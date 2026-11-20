import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column
    df['date_dt'] = pd.to_datetime(df['date'])
    
    # Derive month name
    df['month'] = df['date_dt'].dt.month_name()
    
    # Derive day type: 'weekday' for Mon-Fri, 'weekend' for Sat-Sun
    # dayofweek: 0=Mon, ..., 4=Fri, 5=Sat, 6=Sun
    df['daytype'] = df['date_dt'].apply(lambda x: 'weekend' if x.dayofweek >= 5 else 'weekday')
    
    # Rename hourly columns from 'Hour X' to 'hrX'
    rename_map = {f'Hour {i}': f'hr{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # Select the required columns in the correct order
    cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    df = df[cols]
    
    # Sort by month to match the target sample grouping
    # The target sample appears sorted by Month name (Jan, Feb, Mar...)
    df = df.sort_values(by=['month']).reset_index(drop=True)
    
    return df
