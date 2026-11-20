import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # Create the 'cst' column for grouping
    source['cst'] = source['dt'].dt.strftime('%a %m/%d/%Y')
    
    # Create hour labels 1:00 to 24:00 based on 0-23 hours
    # Hour 0 -> 1:00, Hour 1 -> 2:00, ..., Hour 23 -> 24:00
    source['hour_label'] = source['dt'].dt.hour.apply(lambda h: f"{h + 1}:00")
    
    # Aggregate by day and hour
    grouped = source.groupby(['cst', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot to wide format
    target = grouped.pivot(index='cst', columns='hour_label', values='cerc_logger_1')
    
    # Ensure column order is 1:00 to 24:00
    ordered_cols = [f"{h}:00" for h in range(1, 25)]
    target = target[ordered_cols]
    
    # Reset index to make 'cst' a column
    target = target.reset_index()
    
    return target
