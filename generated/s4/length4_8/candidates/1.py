import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    # Source format: "7/28/2019 4:50" -> M/d/yyyy H:mm
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %I:%M %p', errors='coerce')
    # Fallback for 24h format if present, though sample looks like 12h without AM/PM explicitly in string but context implies standard time
    # Actually, looking at sample: "7/28/2019 4:50". This is ambiguous. 
    # However, standard pd.to_datetime handles "M/d/yyyy H:mm" if we specify format or let it infer.
    # Let's try inferring or using a generic format.
    # The sample "7/28/2019 4:50" suggests 24h clock or 12h without indicator? 
    # Usually "4:50" is AM. "18:50" is PM.
    # Let's use infer_datetime_format for robustness or specific format if known.
    # Given "18:50" in sample, it's 24h clock.
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['cal_date'] = df['dt'].dt.date
    df['hour_int'] = df['dt'].dt.hour
    
    # 3. Map hour_int to target column names
    # Target order: 1:00 AM, 2:00 AM, ..., 11:00 AM, 12:00 PM, 1:00 PM, ..., 11:00 PM, 12:00 AM
    # Hour 0 -> 12:00 AM
    # Hour 1 -> 1:00 AM
    # ...
    # Hour 11 -> 11:00 AM
    # Hour 12 -> 12:00 PM
    # Hour 13 -> 1:00 PM
    # ...
    # Hour 23 -> 11:00 PM
    
    def map_hour(h):
        if h == 0:
            return "12:00 AM"
        elif h < 12:
            return f"{h}:00 AM"
        elif h == 12:
            return "12:00 PM"
        else:
            return f"{h-12}:00 PM"
            
    df['hour_label'] = df['hour_int'].apply(map_hour)
    
    # 4. Pivot the data
    # Index: cal_date, Columns: hour_label, Values: cerc_logger_1
    # Since target has one row per date, we assume unique values per date/hour or take mean/max.
    # Given "distinct" counts in target are low (~60-70) compared to source rows, 
    # and source has 74k rows, it's likely one reading per hour or we average.
    # However, logger data often has multiple readings. 
    # Let's look at the target distinct values: ~60-70. Source distinct: 1279.
    # If we simply pivot, we might get conflicts. 
    # Standard practice for this type of "hourly profile" extraction is often mean or last.
    # Given the precision of the target values (e.g., 24.25), and source values (24.562), 
    # it's possible there's only one value per hour in the subset that matters, or an average.
    # Let's try pivot_table with mean to be safe against duplicates, though unique pivot is faster.
    # Actually, looking at the source sample, dates are unique. 
    # But source has 74k rows and target has 521 rows.
    # 74848 / 521 ≈ 143 hours? No, 521 days * 24 hours = 12504.
    # The data is sparse.
    # We will use pivot_table with mean to aggregate if necessary.
    
    pivoted = df.pivot_table(index='cal_date', columns='hour_label', values='cerc_logger_1', aggfunc='mean')
    
    # 5. Format date index to string MM/dd/yyyy
    pivoted.index = pd.to_datetime(pivoted.index).strftime('%m/%d/%Y')
    pivoted = pivoted.reset_index()
    pivoted.rename(columns={'index': 'date'}, inplace=True)
    
    # 6. Define the specific column order
    hour_labels_order = [
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", "7:00 AM", 
        "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", 
        "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", 
        "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM", "12:00 AM"
    ]
    
    # Ensure all columns exist, filling missing ones with NaN if not present in data
    for col in hour_labels_order:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # Select and order columns
    result = pivoted[['date'] + hour_labels_order]
    
    return result
