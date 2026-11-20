import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format date as required
    out = pd.DataFrame()
    out['date'] = dt.dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define mapping from source column names to target column indices (1-24)
    # Source columns are like "1:00 AM", "12:00 PM"
    # Target columns are "Hour 1", ..., "Hour 24"
    
    # Helper to convert source label to hour index 1-24
    def get_hour_index(col_name):
        # Split by space to get time part and AM/PM part
        parts = col_name.split()
        time_part = parts[0]
        ampm = parts[1]
        
        # Split time by :
        h, m = time_part.split(':')
        h = int(h)
        
        if ampm == 'AM':
            if h == 12:
                return 1
            else:
                return h + 1
        else: # PM
            if h == 12:
                return 13
            else:
                return h + 13

    # Create the mapping dictionary
    col_mapping = {}
    for col in source.columns:
        if col == 'date' or col == 'DSL':
            continue
        # Check if column looks like an hour column
        if 'AM' in col or 'PM' in col:
            try:
                h_idx = get_hour_index(col)
                col_mapping[col] = f'Hour {h_idx}'
            except:
                pass

    # Build the output dataframe columns
    for i in range(1, 25):
        target_col = f'Hour {i}'
        # Find source col that maps to this target
        src_col = None
        for s_col, t_col in col_mapping.items():
            if t_col == target_col:
                src_col = s_col
                break
        
        if src_col is not None:
            out[target_col] = source[src_col].values
        else:
            # Should not happen if mapping is correct
            out[target_col] = np.nan
            
    return out.reset_index(drop=True)
