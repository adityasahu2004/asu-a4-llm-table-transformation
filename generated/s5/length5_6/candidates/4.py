import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Filter out rows with non-zero DSL (assuming 0.119509 is invalid/placeholder)
    # If DSL is not 0.0, it's likely noise based on the distinct values provided.
    df = source[source['DSL'] == 0.0].copy()
    
    # Format the date column
    # Source format: "7/3/2014" -> Target format: "2014-01-01 00:00:00"
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d 00:00:00')
    
    # Define the mapping from source AM/PM columns to target value columns
    # Order: 1AM, 2AM, ..., 11AM, 12PM, 1PM, ..., 11PM, 12AM
    hour_cols = [
        "1:00 AM", "2:00 AM", "3:00 AM", "4:00 AM", "5:00 AM", "6:00 AM", "7:00 AM", "8:00 AM",
        "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM",
        "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM", "12:00 AM"
    ]
    
    target_cols = [f"value{i}" for i in range(1, 25)]
    
    rename_map = dict(zip(hour_cols, target_cols))
    
    # Rename the columns
    df = df.rename(columns=rename_map)
    
    # Select only the required columns in the correct order
    result_cols = ['date'] + target_cols
    df = df[result_cols]
    
    return df.reset_index(drop=True)
