import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dates = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    
    # Create month column with specific padding: 10 chars total
    # January (7) + 3 spaces = 10
    # February (8) + 2 spaces = 10
    # March (5) + 5 spaces = 10
    # etc.
    month_names = dates.dt.strftime('%B')
    month_padded = month_names.str.pad(width=10, side='right')
    
    # Create daytype column
    # pandas dayofweek: Mon=0 ... Sun=6
    is_weekend = dates.dt.dayofweek.isin([5, 6])
    daytype = np.where(is_weekend, 'weekend', 'weekday')
    
    # Rename hourly columns
    hour_cols = [f'Hr {i}' for i in range(1, 25)]
    new_hour_cols = [f'hr{i}' for i in range(1, 25)]
    
    out = source[hour_cols].copy()
    out.columns = new_hour_cols
    
    # Add metadata columns
    out['month'] = month_padded
    out['daytype'] = daytype
    
    # Reorder columns to match target schema
    final_cols = ['month', 'daytype'] + new_hour_cols
    out = out[final_cols]
    
    return out.reset_index(drop=True)
