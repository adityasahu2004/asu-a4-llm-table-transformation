import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Group by date and hour, and calculate the mean of the sensor value
    # This handles the irregular timestamps by bucketing them into hours
    grouped = df.groupby(['date_only', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot the table to have hours as columns
    # hour 0 -> value1, hour 1 -> value2, ..., hour 23 -> value24
    pivoted = grouped.pivot(index='date_only', columns='hour', values='cerc_logger_1')
    
    # Rename columns to value1, value2, ... value24
    pivoted.columns = [f'value{h+1}' for h in pivoted.columns]
    
    # Reset index to make date_only a column
    pivoted = pivoted.reset_index()
    
    # Format the date column as MM/DD/YYYY
    pivoted['date'] = pd.to_datetime(pivoted['date_only']).dt.strftime('%m/%d/%Y')
    
    # Select and order the columns
    result = pivoted[['date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 
                      'value7', 'value8', 'value9', 'value10', 'value11', 'value12', 
                      'value13', 'value14', 'value15', 'value16', 'value17', 'value18', 
                      'value19', 'value20', 'value21', 'value22', 'value23', 'value24']]
    
    # Sort by date to ensure consistent ordering
    result = result.sort_values('date').reset_index(drop=True)
    
    return result
