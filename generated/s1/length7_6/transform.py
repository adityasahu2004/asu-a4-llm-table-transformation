import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the Date column
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # Extract month name
    df['month'] = df['Date'].dt.strftime('%B')
    
    # Extract day type: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: 0=Mon, ..., 4=Fri, 5=Sat, 6=Sun
    df['daytype'] = df['Date'].dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # Rename columns 1-24 to hr1-hr24
    rename_map = {str(i): f'hr{i}' for i in range(1, 25)}
    df.rename(columns=rename_map, inplace=True)
    
    # Drop the original Date and Class columns
    df.drop(columns=['Date', 'Class'], inplace=True)
    
    # Define the desired column order
    hour_cols = [f'hr{i}' for i in range(1, 25)]
    final_cols = ['month', 'daytype'] + hour_cols
    
    # Select and reorder columns
    df = df[final_cols]
    
    # Sort by month (chronologically) and daytype
    # To sort months chronologically, we can map them to numbers or use a custom sort key
    month_order = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
        'October': 10, 'November': 11, 'December': 12
    }
    
    df['month_num'] = df['month'].map(month_order)
    df.sort_values(by=['month_num', 'daytype'], inplace=True)
    df.drop(columns=['month_num'], inplace=True)
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    
    return df
