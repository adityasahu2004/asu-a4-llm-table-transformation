import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Filter out T2 rate
    df = source[source['Rate'] != 'T2'].copy()
    
    # 2. Parse Date and extract Month
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['Month'] = df['Date'].dt.month
    
    # 3. Melt the hourly columns
    # Columns are 'Hr 1' to 'Hr 24'
    hour_cols = [f'Hr {i}' for i in range(1, 25)]
    df_melted = df.melt(
        id_vars=['Month'], 
        value_vars=hour_cols, 
        var_name='Hour_Str', 
        value_name='Value'
    )
    
    # 4. Extract Hour number
    df_melted['Hour'] = df_melted['Hour_Str'].str.extract('(\d+)').astype(int)
    
    # 5. Group by Hour and Month, sum the values
    grouped = df_melted.groupby(['Hour', 'Month'])['Value'].sum().reset_index()
    
    # 6. Pivot to get Months as columns
    # Map month numbers to names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    pivoted = grouped.pivot(index='Hour', columns='Month', values='Value')
    
    # 7. Rename columns to month names
    pivoted = pivoted.rename(columns=month_names)
    
    # 8. Ensure all 12 months are present and ordered
    expected_months = [month_names[i] for i in range(1, 13)]
    for col in expected_months:
        if col not in pivoted.columns:
            pivoted[col] = 0.0
            
    pivoted = pivoted[expected_months]
    
    # 9. Reset index and rename
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'Hour': 'hour'})
    
    # 10. Sort by hour
    pivoted = pivoted.sort_values('hour').reset_index(drop=True)
    
    return pivoted
