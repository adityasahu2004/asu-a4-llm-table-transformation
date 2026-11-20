import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map month names to integers
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    # Parse month
    source = source.copy()
    source['month'] = source['Time Period'].map(month_map)
    source['hour'] = source['Hour Ending']
    
    # Parse number of homes
    # Handle "0 (Modeled)" and other non-numeric strings
    def parse_homes(val):
        if pd.isna(val):
            return 0
        val_str = str(val).strip()
        if val_str.startswith('0'):
            return 0
        try:
            return float(val_str)
        except ValueError:
            return 0
            
    source['num_homes'] = source['Number of Homes in Bin With This End Use Metered'].apply(parse_homes)
    
    # Calculate total demand for each row
    source['total_demand'] = source['num_homes'] * source['Average Demand Per Home With This End Use [kW]']
    
    # Define mapping for End Use to target columns
    # HVAC
    hvac_uses = ['Heating', 'Cooling', 'HVAC']
    # Water Heating
    wh_uses = ['Water Heating', 'Water Heater']
    # Major Appliances: Kitchen and Laundry categories
    # Miscellaneous: Miscellaneous category
    # Lighting: Lighting category (but target is 0)
    
    # Initialize columns for aggregation
    source['hvac'] = 0.0
    source['domestic_water_heating'] = 0.0
    source['major_appliances'] = 0.0
    source['miscellaneous_plug_loads'] = 0.0
    
    # Map HVAC
    mask_hvac = source['End Use'].isin(hvac_uses)
    source.loc[mask_hvac, 'hvac'] = source.loc[mask_hvac, 'total_demand']
    
    # Map Water Heating
    mask_wh = source['End Use'].isin(wh_uses)
    source.loc[mask_wh, 'domestic_water_heating'] = source.loc[mask_wh, 'total_demand']
    
    # Map Major Appliances (Kitchen and Laundry)
    mask_major = source['End Use Category'].isin(['Kitchen', 'Laundry'])
    source.loc[mask_major, 'major_appliances'] = source.loc[mask_major, 'total_demand']
    
    # Map Miscellaneous Plug Loads
    mask_misc = source['End Use Category'] == 'Miscellaneous'
    source.loc[mask_misc, 'miscellaneous_plug_loads'] = source.loc[mask_misc, 'total_demand']
    
    # Aggregate by month and hour
    agg_df = source.groupby(['month', 'hour']).agg(
        hvac=('hvac', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum')
    ).reset_index()
    
    # Ensure all 12 months and 24 hours are present
    all_months = range(1, 13)
    all_hours = range(1, 25)
    index = pd.MultiIndex.from_product([all_months, all_hours], names=['month', 'hour'])
    agg_df = agg_df.set_index(['month', 'hour']).reindex(index, fill_value=0.0).reset_index()
    
    # Add lighting and total columns as 0
    agg_df['lighting'] = 0
    agg_df['total'] = 0
    
    # Select and order columns
    result = agg_df[['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    # Ensure dtypes
    result['month'] = result['month'].astype('int64')
    result['hour'] = result['hour'].astype('int64')
    result['lighting'] = result['lighting'].astype('int64')
    result['total'] = result['total'].astype('int64')
    
    return result
