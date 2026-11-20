import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date and format to YYYY-MM-DD 00:00:00
    # Source date format is M/D/YYYY or MM/DD/YYYY
    dt = pd.to_datetime(source['date'])
    
    out = pd.DataFrame()
    out['date'] = dt.strftime('%Y-%m-%d 00:00:00')
    
    # Map value columns to target hour columns
    target_hours = [
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", 
        "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 AM", 
        "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", 
        "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM", "12:00 PM"
    ]
    
    for i, target_col in enumerate(target_hours):
        source_col = f'value{i+1}'
        out[target_col] = source[source_col]
        
    return out.reset_index(drop=True)
