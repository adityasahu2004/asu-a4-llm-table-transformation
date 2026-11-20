import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column
    # Format in source: "M/D/YYYY H:MM"
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract components for grouping and pivoting
    # 1. Date string for 'cst' column: "DayOfWeek MM/DD/YYYY"
    #    e.g., "Sat 07/20/2019"
    df['cst'] = df['datetime'].dt.strftime('%a %m/%d/%Y')
    
    # 2. Hour bin for columns 1:00 to 24:00
    #    Source hour 0 (0:00-0:59) -> Column "1:00"
    #    Source hour 23 (23:00-23:59) -> Column "24:00"
    df['hour_bin'] = df['datetime'].dt.hour + 1
    
    # Pivot the table
    # Index: cst
    # Columns: hour_bin
    # Values: cerc_logger_1
    # Aggregation: sum (inferred from magnitude difference ~24 -> ~130 with ~6 readings/hr)
    pivot_df = df.pivot_table(
        index='cst',
        columns='hour_bin',
        values='cerc_logger_1',
        aggfunc='sum'
    )
    
    # Rename columns to match target format "1:00", "2:00", ... "24:00"
    pivot_df.columns = [f"{int(col)}:00" for col in pivot_df.columns]
    
    # Reset index to make 'cst' a regular column
    result = pivot_df.reset_index()
    
    # Ensure column order: 'cst' first, then 1:00 to 24:00
    # The pivot table should naturally have sorted columns if hour_bin was numeric, 
    # but let's enforce the order to be safe.
    expected_cols = ['cst'] + [f"{h}:00" for h in range(1, 25)]
    
    # Select only the expected columns to handle any missing hours (though distinct counts suggest all present)
    # and ensure correct order.
    result = result[expected_cols]
    
    return result
