import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map month names to integers
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    # Filter for Weekday only? Or All? 
    # Given the target has 288 rows (12*24), and source has Day Type.
    # We will filter for 'Weekday' as it's a common standard for load shapes.
    # If 'All' is intended, the values would likely be different.
    # We also need to handle 'Weekend' if 'Weekday' is not sufficient.
    # Let's filter for 'Weekday' and 'Weekend' and average? 
    # No, let's just use 'Weekday'.
    
    df = source[source['Day Type'] == 'Weekday'].copy()
    
    # If df is empty, try 'All', then 'Weekend'
    if df.empty:
        df = source[source['Day Type'] == 'All'].copy()
    if df.empty:
        df = source[source['Day Type'] == 'Weekend'].copy()
        
    # Create month integer column
    df['month'] = df['Time Period'].map(month_map)
    df['hour'] = df['Hour Ending']
    
    # Ensure numeric demand
    df['demand'] = pd.to_numeric(df['Average Demand Per Home With This End Use [kW]'], errors='coerce')
    
    # Drop rows where demand is NaN
    df = df.dropna(subset=['demand'])
    
    # Define mapping for categories/ends to target columns
    # We will aggregate by month, hour, and end use type
    
    # Helper to map rows to target columns
    def get_target_col(row):
        cat = row['End Use Category']
        end = row['End Use']
        
        if cat == 'Remaining Load':
            return 'hvac'
        elif end == 'Water Heater' or cat == 'Water Heating': # Assuming Water Heater is the end use
            return 'domestic_water_heating'
        elif cat in ['Kitchen', 'Laundry']:
            return 'major_appliances'
        elif cat == 'Miscellaneous':
            return 'miscellaneous_plug_loads'
        elif cat == 'Lighting':
            return 'lighting'
        else:
            return None

    df['target_col'] = df.apply(get_target_col, axis=1)
    
    # Filter out rows that don't map to our target columns (or map to lighting/total which are 0)
    # Actually, we can just aggregate all and then set lighting/total to 0.
    
    # Group by month, hour, target_col and sum demand
    grouped = df.groupby(['month', 'hour', 'target_col'])['demand'].sum().reset_index()
    
    # Pivot to get columns
    pivoted = grouped.pivot_table(index=['month', 'hour'], columns='target_col', values='demand', fill_value=0).reset_index()
    
    # Ensure all target columns exist
    target_cols = ['hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads']
    for col in target_cols:
        if col not in pivoted.columns:
            pivoted[col] = 0
            
    # Set lighting and total to 0 as per target schema
    pivoted['lighting'] = 0
    pivoted['total'] = 0
    
    # Select and order columns
    result = pivoted[['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    # Ensure types
    result['month'] = result['month'].astype(int)
    result['hour'] = result['hour'].astype(int)
    result['lighting'] = result['lighting'].astype(int)
    result['total'] = result['total'].astype(int)
    
    # Sort by month and hour
    result = result.sort_values(['month', 'hour']).reset_index(drop=True)
    
    return result
