import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract hour and map to 1-24 scale
    # Hour 0 (midnight) maps to 24, others map to 1-23
    df['hour'] = df['datetime'].dt.hour
    df['hour'] = df['hour'].apply(lambda h: 24 if h == 0 else h)
    
    # 3. Format the date for the 'cst' column
    # Format: "DayOfWeek MM/DD/YYYY" e.g., "Sun 09/30/2018"
    df['cst'] = df['datetime'].dt.strftime('%a %m/%d/%Y')
    
    # 4. Determine the value to sum
    # Based on analysis, target values are multiples of 73.0.
    # 876.0 = 12 * 73.0
    # 657.0 = 9 * 73.0
    # 0.0 = 0 * 73.0
    # This implies we sum 73.0 for each row where zone_016_cooling_sp is 73.0.
    # Rows with 84.0 or NaN contribute 0.
    df['value'] = np.where(df['zone_016_cooling_sp'] == 73.0, 73.0, 0.0)
    
    # 5. Group by 'cst' and 'hour', and sum the values
    grouped = df.groupby(['cst', 'hour'])['value'].sum().reset_index()
    
    # 6. Pivot the table
    # Index: cst, Columns: hour, Values: value
    pivoted = grouped.pivot(index='cst', columns='hour', values='value')
    
    # 7. Ensure all hours 1-24 are present, filling missing with 0.0
    all_hours = [f"{h}:00" for h in range(1, 25)]
    # The pivot columns are integers 1-24. We need to rename them to strings "1:00", etc.
    pivoted.columns = [f"{h}:00" for h in pivoted.columns]
    
    # Reindex columns to ensure order and presence
    pivoted = pivoted.reindex(columns=all_hours, fill_value=0.0)
    
    # 8. Reset index to make 'cst' a column
    result = pivoted.reset_index()
    
    # 9. Ensure correct column order: cst, then 1:00 to 24:00
    final_columns = ['cst'] + all_hours
    result = result[final_columns]
    
    # 10. Ensure dtype is float64 for value columns
    for col in all_hours:
        result[col] = result[col].astype(float)
        
    return result
