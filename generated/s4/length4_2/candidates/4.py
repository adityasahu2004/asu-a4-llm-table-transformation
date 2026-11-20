import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date from M/D/YYYY to datetime
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Format to YYYY-MM-DD HH:MM:SS
    formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define the target column names in the exact order provided
    target_cols = [
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", 
        "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 AM", 
        "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", 
        "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM", "12:00 PM"
    ]
    
    # Map source value1..value24 to target columns positionally
    # value1 -> 1:00 AM (index 0)
    # value12 -> 12:00 AM (index 11)
    # value13 -> 1:00 PM (index 12)
    # value24 -> 12:00 PM (index 23)
    result = pd.DataFrame()
    result['date'] = formatted_date
    
    for i in range(1, 25):
        src_col = f'value{i}'
        tgt_col = target_cols[i-1]
        result[tgt_col] = source[src_col]
        
    return result
