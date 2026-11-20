import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date
    df = source.copy()
    df['date_dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract features
    df['dt_strata'] = df['date_dt'].dt.strftime('%m/%d/%y')
    df['dow'] = df['date_dt'].dt.isoweekday() % 7  # Sun=0, Mon=1, ..., Sat=6
    df['hour'] = df['date_dt'].dt.hour
    
    # 3. Map hour to target column name
    # Hour 0 -> pct_hourly_2400
    # Hour 1-23 -> pct_hourly_0100 - pct_hourly_2300
    def map_hour_to_col(h):
        if h == 0:
            return 'pct_hourly_2400'
        return f'pct_hourly_{h:02d}00'
    
    df['hour_col'] = df['hour'].apply(map_hour_to_col)
    
    # 4. Aggregate: Sum zone_016_cooling_sp for each day and hour column
    # Group by dt_strata and hour_col, sum the value
    agg_df = df.groupby(['dt_strata', 'hour_col'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 5. Pivot to wide format
    pivot_df = agg_df.pivot_table(index='dt_strata', columns='hour_col', values='zone_016_cooling_sp', fill_value=0)
    
    # 6. Ensure all expected hour columns exist
    expected_cols = [f'pct_hourly_{h:02d}00' for h in range(1, 24)] + ['pct_hourly_2400']
    for col in expected_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # 7. Add pct_hourly_2500 column with 0
    pivot_df['pct_hourly_2500'] = 0
    
    # 8. Get dow for each dt_strata
    # Since dow is constant for a date, we can get it from the original df
    dow_map = df.drop_duplicates('dt_strata')[['dt_strata', 'dow']].set_index('dt_strata')['dow']
    pivot_df['dow'] = pivot_df.index.map(dow_map)
    
    # 9. Reset index and rename
    pivot_df = pivot_df.reset_index()
    
    # 10. Select and order columns
    final_cols = ['dt_strata', 'dow'] + expected_cols + ['pct_hourly_2500']
    result = pivot_df[final_cols]
    
    # 11. Convert numeric columns to int
    for col in result.columns:
        if col != 'dt_strata':
            result[col] = result[col].astype(int)
            
    return result
