import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Filter for the specific rate that seems to drive the aggregate profile
    # Based on sample data, R4 has varying hourly profiles, while S/T rates have flat blocks.
    # The target values are large, suggesting summation over days.
    df = source[source['Rate'] == 'R4'].copy()
    
    # Parse dates
    df['dt'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['month'] = df['dt'].dt.month
    
    # Select hourly columns
    hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # Melt the dataframe to long format for easier aggregation
    # Keep 'month' and the hourly values
    long_df = df[['month'] + hour_cols].melt(id_vars=['month'], var_name='hour_label', value_name='value')
    
    # Extract hour number from 'Hr N'
    long_df['hour'] = long_df['hour_label'].str.extract(r'(\d+)').astype(int)
    
    # Aggregate: Sum the values for each hour and each month
    agg_df = long_df.groupby(['month', 'hour'])['value'].sum().reset_index()
    
    # Pivot to wide format: Hours as rows, Months as columns
    pivot_df = agg_df.pivot(index='hour', columns='month', values='value').reset_index()
    
    # Rename columns to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    pivot_df.rename(columns=month_names, index=str, inplace=True)
    
    # Ensure 'hour' column is integer and sorted
    pivot_df['hour'] = pivot_df['hour'].astype(int)
    pivot_df = pivot_df.sort_values('hour').reset_index(drop=True)
    
    # Select only the required columns in order
    final_cols = ['hour'] + [month_names[i] for i in range(1, 13)]
    result = pivot_df[final_cols]
    
    return result
