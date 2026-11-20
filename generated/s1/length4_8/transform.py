import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms a long-format time series dataframe into a wide-format daily summary.
    
    Steps:
    1. Parse the 'date' column into datetime.
    2. Extract date and hour components.
    3. Map 24-hour hours to 12-hour AM/PM strings.
    4. Pivot the data to have dates as rows and hours as columns.
    5. Format the date column as MM/DD/YYYY.
    6. Reorder columns to match the specific target sequence.
    """
    
    # 1. Parse dates
    # Source format: "7/28/2019 4:50" -> M/D/YYYY H:MM
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %I:%M %p', errors='coerce')
    
    # Handle cases where format might be ambiguous or simple M/D/Y
    # If the above fails for some, try a more flexible parser, but the sample suggests consistent format.
    # Let's try a more robust parsing if the strict format fails, though the sample is consistent.
    # Actually, '7/28/2019 4:50' doesn't have AM/PM. It's likely 24h or 12h without indicator?
    # Looking at sample: "7/28/2019 4:50", "9/13/2019 9:30", "12/20/2019 0:50".
    # "0:50" implies 24-hour format or midnight. "4:50" could be 4:50 AM or PM.
    # However, the target has distinct hours for every hour of the day.
    # Let's assume the hour part is the hour of the day (0-23).
    # The format string '%m/%d/%Y %H:%M' handles 24h. '%m/%d/%Y %I:%M' handles 12h.
    # Given "0:50", it's likely 24h format for the hour part.
    
    # Re-parse with 24h hour assumption
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M', errors='coerce')
    
    # If some fail, try 12h without AM/PM? Unlikely given "0:50".
    # Let's ensure we have valid datetimes
    if df['datetime'].isnull().all():
        # Fallback to generic parsing if strict format fails
        df['datetime'] = pd.to_datetime(df['date'], infer_datetime_format=True)

    # 2. Extract Date and Hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map Hour to Target Column Name
    # Target columns: 
    # 1:00 AM, 2:00 AM, ..., 11:00 AM, 12:00 PM, 1:00 PM, ..., 11:00 PM, 12:00 AM
    # Mapping:
    # 0 -> 12:00 AM
    # 1 -> 1:00 AM
    # ...
    # 11 -> 11:00 AM
    # 12 -> 12:00 PM
    # 13 -> 1:00 PM
    # ...
    # 23 -> 11:00 PM
    
    def map_hour_to_label(h):
        if pd.isna(h):
            return None
        h = int(h)
        if h == 0:
            return "12:00 AM"
        elif h < 12:
            return f"{h}:00 AM"
        elif h == 12:
            return "12:00 PM"
        else:
            return f"{h-12}:00 PM"
            
    df['hour_label'] = df['hour'].apply(map_hour_to_label)
    
    # 4. Pivot
    # We need to aggregate if there are multiple entries for the same date/hour.
    # The source has distinct dates, but let's use mean to be safe against duplicates.
    pivot_df = df.pivot_table(
        index='date_only', 
        columns='hour_label', 
        values='cerc_logger_1', 
        aggfunc='mean'
    )
    
    # 5. Format Date Column
    # Target date format: "05/08/2019" (MM/DD/YYYY)
    pivot_df.index = pivot_df.index.strftime('%m/%d/%Y')
    pivot_df.index.name = 'date'
    
    # 6. Reorder Columns
    # The target order is specific: 1AM, 2AM, ..., 11AM, 12PM, 1PM, ..., 11PM, 12AM
    target_order = [
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", "7:00 AM", "8:00 AM",
        "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM",
        "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM", "12:00 AM"
    ]
    
    # Ensure all target columns exist, filling with NaN if not present in data
    for col in target_order:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    pivot_df = pivot_df[target_order]
    
    # 7. Reset Index to make 'date' a column
    result = pivot_df.reset_index()
    
    return result
