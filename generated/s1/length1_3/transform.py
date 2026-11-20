import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Define the mapping from source time columns to target time columns
    # Source: 12-hour format with AM/PM
    # Target: 24-hour format (1:00 to 24:00)
    col_mapping = {
        '1:00 AM': '1:00',
        '2:00 AM': '2:00',
        '3:00 AM': '3:00',
        '4:00 AM': '4:00',
        '5:00 AM': '5:00',
        '6:00 AM': '6:00',
        '7:00 AM': '7:00',
        '8:00 AM': '8:00',
        '9:00 AM': '9:00',
        '10:00 AM': '10:00',
        '11:00 AM': '11:00',
        '12:00 PM': '12:00',
        '1:00 PM': '13:00',
        '2:00 PM': '14:00',
        '3:00 PM': '15:00',
        '4:00 PM': '16:00',
        '5:00 PM': '17:00',
        '6:00 PM': '18:00',
        '7:00 PM': '19:00',
        '8:00 PM': '20:00',
        '9:00 PM': '21:00',
        '10:00 PM': '22:00',
        '11:00 PM': '23:00',
        '12:00 AM': '24:00'
    }

    # Create a copy to avoid modifying the original
    df = source.copy()

    # Rename the time columns
    df.rename(columns=col_mapping, inplace=True)

    # Parse the date column
    # Source format: M/D/YYYY (e.g., 7/3/2014)
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')

    # Format the date column to target format: DayOfWeek MM/DD/YYYY (e.g., Wed 01/01/2014)
    # %a gives abbreviated weekday name (e.g., Wed)
    # %m gives zero-padded month
    # %d gives zero-padded day
    # %Y gives 4-digit year
    df['cst'] = df['date'].dt.strftime('%a %m/%d/%Y')

    # Define the target column order
    target_columns = ['cst'] + [f'{h}:00' for h in range(1, 25)]

    # Select and reorder columns
    # Note: The source 'date' column is no longer needed, and 'DSL' is dropped.
    result = df[target_columns]

    return result
