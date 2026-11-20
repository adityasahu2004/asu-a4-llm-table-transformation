import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format is "m/d/Y H:M" e.g., "7/28/2019 4:50"
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour for grouping
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # Calculate mean for each hour of each day
    # Group by date and hour, then mean
    hourly_means = df.groupby(['date_only', 'hour'])['cerc_logger_1'].mean().unstack(level='hour')
    
    # Ensure all 24 hours are present, filling missing with NaN (though distinct count suggests no nulls in target, 
    # the source might have sparse data. The target distinct counts are high, implying dense data.
    # However, if an hour is missing for a day, unstack puts NaN.
    # The target schema says nulls: 0. This implies either data is complete or we need to handle missing.
    # Given "distinct" values in target are ~340-360 and rows are 521, it's likely complete or interpolated.
    # But simple mean aggregation is the standard interpretation. If NaNs exist, we might need to forward fill 
    # or the data is guaranteed complete. Let's assume standard aggregation.
    # If the target has 0 nulls, but source is sparse, we might need to fill. 
    # However, without explicit instruction, we stick to aggregation. 
    # Note: The target sample shows 0.0 values in some cells for a different dataset, but here distinct counts are high.
    # Let's proceed with mean.
    
    # Reorder columns 0 to 23
    hourly_means = hourly_means.reindex(columns=range(24), axis=1)
    
    # Rename columns to match target: 1:00 to 24:00
    # Mapping: Hour 0 -> "1:00", Hour 1 -> "2:00", ..., Hour 23 -> "24:00"
    new_cols = [f"{h+1}:00" for h in range(24)]
    hourly_means.columns = new_cols
    
    # Format the date index for the 'cst' column
    # The index of hourly_means is 'date_only' (python date objects)
    # We need to format it as "%a %m/%d/%Y"
    # Create a series for cst
    cst_dates = pd.Series(hourly_means.index, index=hourly_means.index)
    # Convert to datetime for formatting, then format
    cst_formatted = pd.to_datetime(cst_dates).dt.strftime('%a %m/%d/%Y')
    
    # Combine
    result = hourly_means.copy()
    result.insert(0, 'cst', cst_formatted)
    
    # Reset index to get a clean DataFrame
    result = result.reset_index(drop=True)
    
    return result
