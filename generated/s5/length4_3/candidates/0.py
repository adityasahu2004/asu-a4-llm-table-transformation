import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    
    # Format date
    out['date'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # Define the mapping from source column names to target column names
    target_cols = [
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM",
        "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 AM",
        "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM",
        "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM", "12:00 PM"
    ]
    
    for i, target_col in enumerate(target_cols):
        hour_idx = i + 1
        source_col = f"PCT_HOURLY_{hour_idx:02d}00"
        out[target_col] = source[source_col]
        
    return out.reset_index(drop=True)
