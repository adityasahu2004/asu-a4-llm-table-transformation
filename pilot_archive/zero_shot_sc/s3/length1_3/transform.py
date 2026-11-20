import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Define the mapping from source column names (12-hour format) to target column names (24-hour format)
    # Source: 12:00 AM -> Target: 1:00
    # Source: 1:00 AM -> Target: 2:00
    # ...
    # Source: 11:00 AM -> Target: 12:00
    # Source: 12:00 PM -> Target: 13:00
    # ...
    # Source: 11:00 PM -> Target: 24:00
    
    col_mapping = {
        '12:00 AM': '1:00',
        '1:00 AM': '2:00',
        '2:00 AM': '3:00',
        '3:00 AM': '4:00',
        '4:00 AM': '5:00',
        '5:00 AM': '6:00',
        '6:00 AM': '7:00',
        '7:00 AM': '8:00',
        '8:00 AM': '9:00',
        '9:00 AM': '10:00',
        '10:00 AM': '11:00',
        '11:00 AM': '12:00',
        '12:00 PM': '13:00',
        '1:00 PM': '14:00',
        '2:00 PM': '15:00',
        '3:00 PM': '16:00',
        '4:00 PM': '17:00',
        '5:00 PM': '18:00',
        '6:00 PM': '19:00',
        '7:00 PM': '20:00',
        '8:00 PM': '21:00',
        '9:00 PM': '22:00',
        '10:00 PM': '23:00',
        '11:00 PM': '24:00'
    }

    # Create a copy to avoid modifying the original
    df = source.copy()

    # Rename the hourly columns
    df.rename(columns=col_mapping, inplace=True)

    # Drop the DSL column as it is not in the target
    if 'DSL' in df.columns:
        df.drop(columns=['DSL'], inplace=True)

    # Parse the date column
    # Source format: M/D/YYYY (e.g., 7/3/2014)
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')

    # Format the date to target format: "DayName MM/DD/YYYY" (e.g., "Wed 01/01/2014")
    # %a gives abbreviated weekday name (Wed)
    # %m gives zero-padded month
    # %d gives zero-padded day
    # %Y gives 4-digit year
    df['cst'] = df['date'].dt.strftime('%a %m/%d/%Y')

    # Drop the original date column
    df.drop(columns=['date'], inplace=True)

    # Define the target column order
    target_columns = ['cst'] + [f'{h}:00' for h in range(1, 25)]

    # Ensure all target columns exist and reorder
    # Note: The mapping above ensures the columns exist if the source was valid.
    df = df[target_columns]

    return df
