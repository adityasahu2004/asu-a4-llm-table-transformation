import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract features
    df['Hour'] = df['dt'].dt.hour
    df['Month'] = df['dt'].dt.strftime('%B') # Capitalized month name
    
    # Pivot table
    # Index: Hour, Columns: Month, Values: zone_016
    pivoted = df.pivot_table(index='Hour', columns='Month', values='zone_016', aggfunc='first')
    
    # Define all month names to ensure complete columns
    all_months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Reindex columns to include all months, filling missing with NaN
    pivoted = pivoted.reindex(columns=all_months)
    
    # Sort by Hour
    pivoted = pivoted.sort_index()
    
    # Reset index to make Hour a column
    result = pivoted.reset_index()
    
    return result
