import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date string
    # Format is M/D/YYYY H:MM
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date part and hour part
    df['date_key'] = df['dt'].dt.date
    df['hour_idx'] = df['dt'].dt.hour
    
    # Map hour 0-23 to "Hour 1" - "Hour 24"
    df['hour_label'] = df['hour_idx'].apply(lambda h: f"Hour {h + 1}")
    
    # Pivot the table
    # Index: date_key, Columns: hour_label, Values: zone_016
    pivoted = df.pivot_table(index='date_key', columns='hour_label', values='zone_016', aggfunc='first')
    
    # Reset index to bring date back as a column
    pivoted = pivoted.reset_index()
    
    # Rename index column to 'date'
    pivoted = pivoted.rename(columns={'date_key': 'date'})
    
    # Format date as MM/DD/YYYY
    pivoted['date'] = pivoted['date'].apply(lambda d: d.strftime('%m/%d/%Y'))
    
    # Ensure all 24 hour columns exist, filling missing with NaN
    expected_cols = [f"Hour {i}" for i in range(1, 25)]
    for col in expected_cols:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # Select and order columns: date, then Hour 1 to Hour 24
    final_cols = ['date'] + expected_cols
    result = pivoted[final_cols]
    
    # Sort by date descending to match target sample order
    # Convert back to datetime for sorting, then drop helper if needed, 
    # but since we formatted to string, we can sort by the string if format is consistent, 
    # or better, use the original date object if we kept it. 
    # Let's re-parse for sorting to be safe, or just sort by the formatted string 
    # since MM/DD/YYYY sorts correctly lexicographically? 
    # No, MM/DD/YYYY does not sort correctly lexicographically (e.g. 01/02 vs 12/01).
    # We need to sort by the actual date.
    
    # Re-create a sortable key
    result['sort_key'] = pd.to_datetime(result['date'], format='%m/%d/%Y')
    result = result.sort_values('sort_key', ascending=False)
    result = result.drop(columns=['sort_key'])
    
    return result.reset_index(drop=True)
