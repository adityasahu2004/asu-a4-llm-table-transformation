import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms hourly load data from wide format (value1-value24) 
    to a pivoted format with hours as columns (1:00-24:00) and 
    formatted date strings as the index column 'cst'.
    """
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Melt the dataframe from wide to long format
    # Select only the value columns and the date
    value_cols = [f'value{i}' for i in range(1, 25)]
    melt_cols = ['date'] + value_cols
    
    # Create hour mapping: value1 -> 1, value2 -> 2, ...
    # We melt and then map the variable name to an integer hour
    melted = df.melt(
        id_vars=['date'], 
        value_vars=value_cols, 
        var_name='hour_var', 
        value_name='value'
    )
    
    # Extract integer hour from 'value1', 'value2', etc.
    melted['hour'] = melted['hour_var'].str.extract(r'(\d+)').astype(int)
    
    # 3. Pivot the dataframe
    # Index: date, Columns: hour, Values: value
    pivoted = melted.pivot_table(
        index='date', 
        columns='hour', 
        values='value'
    )
    
    # 4. Format the date index into the 'cst' column
    # Format: "Sat 01/01/2011" -> %a %m/%d/%Y
    pivoted['cst'] = pivoted.index.strftime('%a %m/%d/%Y')
    
    # 5. Rename columns to "1:00", "2:00", ... "24:00"
    pivoted.columns = [f"{h}:00" for h in pivoted.columns]
    # Note: The 'cst' column was added to the index level or as a column? 
    # pivot_table returns a DataFrame with 'date' as index. 
    # The assignment pivoted['cst'] = ... adds it as a column.
    # The columns list now includes 'cst' and the hour strings.
    # We need to ensure 'cst' is the first column.
    
    # Reorder columns: 'cst' first, then hours 1-24
    hour_cols = [f"{h}:00" for h in range(1, 25)]
    final_cols = ['cst'] + hour_cols
    
    # Select and reorder columns
    result = pivoted[final_cols]
    
    # 6. Sort by date (using the index) to ensure chronological order
    result = result.sort_index()
    
    # 7. Reset index to make 'date' (if it was index) disappear, 
    # but we kept 'cst' as a column. The index is currently 'date'.
    # We want 'cst' as a column and no index name.
    result = result.reset_index(drop=True)
    
    # Ensure numeric types for value columns
    for col in hour_cols:
        result[col] = pd.to_numeric(result[col], errors='coerce')
        
    return result
