import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the source date
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # Create a weekly resample index
    # Assuming the target covers the same year as the source data
    # We create a range of weeks covering the source date range
    start_date = source['dt'].min().normalize()
    end_date = source['dt'].max().normalize()
    
    # Generate weekly dates
    weekly_dates = pd.date_range(start=start_date, end=end_date, freq='W-SUN')
    
    # Initialize the target DataFrame
    target = pd.DataFrame(index=weekly_dates)
    target['cst'] = target.index.strftime('%a %m/%d/%Y')
    
    # Initialize hourly columns with 0
    for h in range(1, 25):
        target[f'{h}:00'] = 0.0
        
    # For each week, aggregate the source data
    for week_date in weekly_dates:
        # Get the start and end of the week
        week_start = week_date
        week_end = week_date + pd.Timedelta(days=7)
        
        # Filter source data for this week
        week_data = source[(source['dt'] >= week_start) & (source['dt'] < week_end)]
        
        if week_data.empty:
            continue
            
        # For each hour, calculate the average setpoint and multiply by 12
        for h in range(1, 25):
            # Extract the hour from the timestamp
            hour_data = week_data[week_data['dt'].dt.hour == h-1]
            if not hour_data.empty:
                mean_val = hour_data['zone_016_cooling_sp'].mean()
                # Apply scaling factor
                target.loc[week_date, f'{h}:00'] = mean_val * 12
                
    return target.reset_index(drop=True)
