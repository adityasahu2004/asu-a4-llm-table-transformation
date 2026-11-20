import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format observed: "7/28/2019 4:50" -> %m/%d/%Y %H:%M or %m/%d/%Y %I:%M
    # Using mixed format parsing or specific format. 
    # Note: 24h format is implied by "18:50", "20:00" etc. in sample if present, 
    # but sample shows "4:50", "9:30". "18:50" is in sample data row 3. So 24h.
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract Hour and Month
    df['Hour'] = df['dt'].dt.hour
    df['Month'] = df['dt'].dt.month
    
    # Map month numbers to names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['MonthName'] = df['Month'].map(month_map)
    
    # Aggregate mean by Hour and MonthName
    # The target has 24 rows, implying one row per hour.
    # The values in the target sample look like averages (e.g., 24.562 is a specific value, 
    # but looking at December Hour 0 in target: 85.0. In source, is there an 85.0? 
    # The source sample doesn't show 85.0, but distinct values for December in target include 85.0.
    # Assuming simple mean aggregation as is standard for this type of transformation.
    
    agg_df = df.groupby(['Hour', 'MonthName'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot to wide format
    pivot_df = agg_df.pivot(index='Hour', columns='MonthName', values='cerc_logger_1')
    
    # Reset index to get Hour as a column
    pivot_df = pivot_df.reset_index()
    
    # Ensure all month columns are present and sorted
    all_months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Reindex columns to ensure order and presence
    pivot_df = pivot_df.reindex(columns=['Hour'] + all_months)
    
    # Sort by Hour
    pivot_df = pivot_df.sort_values('Hour').reset_index(drop=True)
    
    # Cast Hour to int64
    pivot_df['Hour'] = pivot_df['Hour'].astype('int64')
    
    return pivot_df
