import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse dates
    source = source.copy()
    source['date'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # 2. Extract month
    source['month'] = source['date'].dt.month
    
    # 3. Melt the value columns (value1...value24) into long format
    # Identify value columns
    value_cols = [c for c in source.columns if c.startswith('value')]
    
    # Create a mapping from column name to hour number
    # value1 -> 1, value2 -> 2, etc.
    hour_map = {f'value{i}': i for i in range(1, 25)}
    
    # Melt
    melted = pd.melt(
        source, 
        id_vars=['month'], 
        value_vars=value_cols, 
        var_name='value_col', 
        value_name='load'
    )
    
    # Map column names to hours
    melted['hour'] = melted['value_col'].map(hour_map)
    
    # Drop rows where load is NaN (though source says 0 nulls, good practice)
    melted = melted.dropna(subset=['load'])
    
    # 4. Aggregate: Mean load per hour per month
    aggregated = melted.groupby(['hour', 'month'])['load'].mean().reset_index()
    
    # 5. Pivot: Hours as index, Months as columns
    pivoted = aggregated.pivot(index='hour', columns='month', values='load')
    
    # 6. Rename month columns to lowercase names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    pivoted = pivoted.rename(columns=month_names)
    
    # Ensure all expected month columns exist, even if empty (NaN)
    for m in range(1, 13):
        if month_names[m] not in pivoted.columns:
            pivoted[month_names[m]] = np.nan
            
    # Select only the month columns in order
    month_cols = [month_names[i] for i in range(1, 13)]
    pivoted = pivoted[month_cols]
    
    # 7. Reset index to make 'hour' a column
    result = pivoted.reset_index()
    
    # Ensure hour is int
    result['hour'] = result['hour'].astype(int)
    
    # Sort by hour for deterministic output
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result
