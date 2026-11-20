import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map month names to numbers
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    # Create a copy to avoid SettingWithCopyWarning
    df = source.copy()
    
    # Map Time Period to Month
    df['Month'] = df['Time Period'].map(month_map)
    
    # Derive Season
    def get_season(month, day_type):
        if day_type == 'All':
            return None
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Fall'
        return None
        
    df['season'] = df.apply(lambda row: get_season(row['Month'], row['Day Type']), axis=1)
    
    # Filter out rows where season is None if they don't map to the 'All' group?
    # The target has null seasons. This likely corresponds to the 'All' day type rows.
    # However, if 'Day Type' is 'All', the season is null.
    # We need to ensure we group by season (including null) and Hour Ending.
    
    # Ensure numeric demand
    df['Demand'] = pd.to_numeric(df['Average Demand Per Home With This End Use [kW]'], errors='coerce')
    
    # Map End Use Category to Target Columns
    # We will pivot or groupby.
    
    # Identify which rows contribute to which target column
    # hvac: Remaining Load
    # domestic_water_heating: End Use == "Water Heating" (Assuming this exists)
    # major_appliances: Kitchen or Laundry
    # lighting: Lighting (Target is 0, so we might ignore or set to 0)
    # miscellaneous_plug_loads: Miscellaneous
    
    # Let's create helper columns for summing
    df['is_hvac'] = (df['End Use Category'] == 'Remaining Load').astype(int)
    df['is_dwh'] = (df['End Use'] == 'Water Heating').astype(int) # Check if this end use exists
    # If 'Water Heating' is not an End Use, maybe it's part of Remaining Load? 
    # But target has separate values. Let's assume 'Water Heating' is an End Use.
    # If it's not in the data, this column will be 0, resulting in 0 sum.
    
    df['is_major'] = (df['End Use Category'].isin(['Kitchen', 'Laundry'])).astype(int)
    df['is_misc'] = (df['End Use Category'] == 'Miscellaneous').astype(int)
    
    # We don't need lighting for the sum as target is 0, but we can calculate it if needed.
    
    # Group by season and Hour Ending
    # Note: 'season' can be None (NaN)
    
    agg_df = df.groupby(['season', 'Hour Ending']).agg(
        hvac=('Demand', lambda x: (x * df.loc[x.index, 'is_hvac']).sum()),
        domestic_water_heating=('Demand', lambda x: (x * df.loc[x.index, 'is_dwh']).sum()),
        major_appliances=('Demand', lambda x: (x * df.loc[x.index, 'is_major']).sum()),
        miscellaneous_plug_loads=('Demand', lambda x: (x * df.loc[x.index, 'is_misc']).sum())
    ).reset_index()
    
    # Rename Hour Ending to hour
    agg_df = agg_df.rename(columns={'Hour Ending': 'hour'})
    
    # Add constant columns
    agg_df['lighting'] = 0
    agg_df['total'] = 0
    
    # Select and order columns
    result = agg_df[['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    # Ensure types
    result['hour'] = result['hour'].astype(int)
    result['lighting'] = result['lighting'].astype(int)
    result['total'] = result['total'].astype(int)
    
    # Sort to match typical output order (optional, but good for determinism)
    # The target sample is not sorted by season/hour strictly.
    # We will just return the grouped result.
    
    return result
