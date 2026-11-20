import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort by Date to ensure consistent ordering (assuming chronological order is desired)
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Format the Date column to the target format: "Day MM/DD/YYYY"
    # e.g., "Tue 01/01/2013"
    df['cst'] = df['Date'].dt.strftime('%a %m/%d/%Y')
    
    # Rename the numeric columns 1-24 to 1:00-24:00
    rename_map = {}
    for i in range(1, 25):
        rename_map[str(i)] = f"{i}:00"
    
    df = df.rename(columns=rename_map)
    
    # Select the required columns in the correct order
    # Target columns: 'cst', '1:00', ..., '24:00'
    cols = ['cst'] + [f"{i}:00" for i in range(1, 25)]
    
    df = df[cols]
    
    return df
