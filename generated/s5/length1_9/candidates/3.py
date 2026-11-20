import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    # Format: M/D/YYYY H:MM
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%-m/%-d/%Y %-H:%M')
    source['date_str'] = source['dt'].dt.strftime('%m/%d/%Y')
    source['hour'] = source['dt'].dt.hour
    
    # Identify unique dates
    unique_dates = source['date_str'].unique()
    
    results = []
    
    # Define target hour columns
    hour_cols = [f'{h}:00' for h in range(1, 25)]
    
    for date in unique_dates:
        # Filter rows for this date
        df_date = source[source['date_str'] == date].copy()
        
        # Drop nulls in zone_016 for calculation
        df_valid = df_date.dropna(subset=['zone_016'])
        
        row_data = {'cst': date}
        
        # Check if we have 24 rows (one per hour) to map individually
        # Assuming if count is 24, we map. Otherwise, sum to 24:00.
        if len(df_valid) == 24:
            # Initialize zeros
            for col in hour_cols:
                row_data[col] = 0.0
            
            # Map each row to its hour
            # Source Hour H -> Target Column H+1
            # If H=23, Target is 24:00
            for _, row in df_valid.iterrows():
                h = int(row['hour'])
                target_col_idx = h + 1 # 0->1, 23->24
                if 1 <= target_col_idx <= 24:
                    col_name = f'{target_col_idx}:00'
                    row_data[col_name] += row['zone_016']
        else:
            # Sum all values into 24:00
            total = df_valid['zone_016'].sum()
            for col in hour_cols:
                if col == '24:00':
                    row_data[col] = total
                else:
                    row_data[col] = 0.0
                    
        results.append(row_data)
        
    out = pd.DataFrame(results)
    
    # Format CST as "ddd MM/DD/YYYY"
    # We need to parse the date string back to datetime to get day name
    out['cst_dt'] = pd.to_datetime(out['cst'], format='%m/%d/%Y')
    out['cst'] = out['cst_dt'].dt.strftime('%a %m/%d/%Y')
    out = out.drop(columns=['cst_dt'])
    
    # Ensure column order
    final_cols = ['cst'] + hour_cols
    out = out[final_cols]
    
    # Reset index
    out = out.reset_index(drop=True)
    
    return out
