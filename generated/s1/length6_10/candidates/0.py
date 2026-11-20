import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # Source format: "11/6/2018 21:45" -> %m/%d/%Y %H:%M
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract the calendar date for grouping
    df['date_only'] = df['parsed_date'].dt.date
    
    # 3. Group by date and aggregate the value
    # The target shows that for a given day, all 24 hours have the same value.
    # This implies the source value for that day is broadcasted.
    # We take the first non-null value for each day.
    grouped = df.groupby('date_only')['zone_016_cooling_sp'].first().reset_index()
    
    # 4. Create the 24 hour columns
    # Initialize a new dataframe with the date
    result = pd.DataFrame(grouped['date_only'], columns=['Date'])
    
    # Broadcast the value to all 24 hours
    for i in range(1, 25):
        result[f'Hr {i}'] = grouped['zone_016_cooling_sp']
        
    # 5. Format the Date column as MM/DD/YYYY
    result['Date'] = pd.to_datetime(result['Date']).dt.strftime('%m/%d/%Y')
    
    # 6. Ensure correct column order
    cols = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    result = result[cols]
    
    return result
