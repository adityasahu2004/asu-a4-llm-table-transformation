import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    # Format: "1/2/2018 0:11"
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # Create dt_strata: MM/dd/yy
    dt_strata = dt.dt.strftime('%m/%d/%y')
    
    # Create dow: ISO day of week (Monday=1, Sunday=7)
    dow = dt.dt.isocalendar().day.astype(int)
    
    # Prepare hourly columns
    # Source hour 0 -> Target column 24
    # Source hour 1-23 -> Target column 1-23
    # Source hour 24? (Unlikely in 24h format, but if exists, map to 24)
    
    # Calculate the value: zone_016 * minutes (if minutes==0, use 60)
    minutes = dt.dt.minute
    # Replace 0 minutes with 60 for the calculation factor
    factor = minutes.replace(0, 60)
    value = source['zone_016'] * factor
    
    # Determine target hour column index
    # Hour 0 maps to 24, others map to themselves
    hours = dt.dt.hour
    target_hour = hours.where(hours != 0, 24)
    
    # Create a DataFrame for the hourly values
    # We need to pivot this data so that each row in source becomes a contribution to the daily aggregate
    # Construct a series with MultiIndex (dt_strata, target_hour)
    index = pd.MultiIndex.from_arrays([dt_strata, target_hour.astype(str).str.zfill(2).map(lambda x: f'pct_hourly_{x}00')])
    # Actually, let's keep the hour number for now to map to columns
    
    # Let's create a temporary dataframe with dt_strata, dow, and the value mapped to the correct column name
    # We will group by dt_strata and sum (or aggregate) the values
    
    # Map hour to column name
    def get_col_name(h):
        return f'pct_hourly_{h:02d}00'
        
    col_names = target_hour.apply(get_col_name)
    
    # Create a DataFrame with dt_strata, dow, and one-hot encoded values?
    # No, we can use pd.crosstab or pivot_table
    
    # Create a series of values indexed by dt_strata and column name
    val_series = pd.Series(value.values, index=pd.MultiIndex.from_arrays([dt_strata, col_names]))
    
    # Pivot to get one row per dt_strata
    # Since there might be multiple entries for the same hour on the same day, we sum them.
    # Initialize with 0s for missing hours
    hourly_df = val_series.unstack(fill_value=0)
    
    # Ensure all 24 columns exist
    all_cols = [f'pct_hourly_{h:02d}00' for h in range(1, 25)]
    for col in all_cols:
        if col not in hourly_df.columns:
            hourly_df[col] = 0
            
    # Sort columns
    hourly_df = hourly_df[all_cols]
    
    # Add dt_strata and dow
    # Dow is constant per day? Yes. Take the first one.
    dow_series = pd.Series(dow.values, index=dt_strata).groupby(dt_strata).first()
    
    # Combine
    result = hourly_df.reset_index()
    result.rename(columns={'index': 'dt_strata'}, inplace=True)
    
    # Add dow
    result['dow'] = result['dt_strata'].map(dow_series)
    
    # Reorder columns
    cols = ['dt_strata', 'dow'] + all_cols
    result = result[cols]
    
    # Add pct_hourly_2500
    result['pct_hourly_2500'] = 0
    
    return result
