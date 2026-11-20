import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month'] = source['dt'].dt.month
    source['hour'] = source['dt'].dt.hour + 1 # 1-24
    
    # Identify value columns
    val_cols = [f'value{i}' for i in range(1, 25)]
    
    # Group by month and hour, and take the mean of the value columns
    # Note: The target shows specific averages. Since the source has multiple entries per day/hour potentially?
    # Actually, looking at source distinct dates (182) and rows (182), it seems 1 row per date.
    # However, the target has only 12 rows? No, target has 24 rows (one per hour).
    # The target columns are months. The values are averages across all days in that month for that hour.
    
    # Let's group by month and hour
    grouped = source.groupby(['month', 'hour'])[val_cols].mean()
    
    # Pivot so months are columns
    # We want rows to be hours, columns to be months
    pivoted = grouped.unstack(level='month')
    
    # Flatten the column multiindex if necessary, but unstack on level 'month' leaves 'hour' as index and months as columns
    # The columns are now named after the value columns? No, we grouped by month/hour and took mean of val_cols.
    # Wait, the target has ONE value per month/hour.
    # The source has 24 value columns representing the 24 hours of THAT day.
    # Target has columns for months.
    # This implies we need to reshape the source data first?
    
    # Let's re-evaluate.
    # Source: 1 row per day. 24 columns for hours 1-24.
    # Target: 24 rows (hours 1-24). 12 columns (months).
    # Value at (hour=h, month=m) is the average of the h-th hour column across all days in month m.
    
    # Step 1: Melt the source data to long format
    long_df = source.melt(id_vars=['month', 'hour'], value_vars=val_cols, var_name='hour_col', value_name='load')
    
    # Step 2: Extract hour number from hour_col (value1 -> 1, etc.)
    long_df['hour_num'] = long_df['hour_col'].str.extract(r'(\d+)').astype(int)
    
    # Step 3: Group by month and hour_num, calculate mean
    agg_df = long_df.groupby(['month', 'hour_num'])['load'].mean().reset_index()
    
    # Step 4: Pivot
    # Index: hour_num, Columns: month, Values: load
    pivot_df = agg_df.pivot(index='hour_num', columns='month', values='load')
    
    # Step 5: Rename columns to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivot_df.columns = [month_names[m] for m in pivot_df.columns]
    
    # Step 6: Sort index by hour
    pivot_df = pivot_df.sort_index()
    
    # Step 7: Reset index and rename
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'hour_num': 'hour'})
    
    # Step 8: Ensure column order
    cols = ['hour'] + [month_names[i] for i in range(1, 13)]
    # Filter to only existing columns in case some months are missing in data (though target has nulls for some)
    existing_cols = [c for c in cols if c in pivot_df.columns]
    
    # Add missing month columns with NaNs if they don't exist
    for c in cols:
        if c not in pivot_df.columns:
            pivot_df[c] = np.nan
            
    pivot_df = pivot_df[cols]
    
    return pivot_df
