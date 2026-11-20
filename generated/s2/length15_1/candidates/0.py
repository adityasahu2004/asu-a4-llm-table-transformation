import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse time
    source = source.copy()
    source['time_dt'] = pd.to_datetime(source['time'])
    source['hour'] = source['time_dt'].dt.hour
    source['month'] = source['time_dt'].dt.month
    
    # Define Season
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Fall' # Not in target distinct values, but good to have logic
        else:
            return 'Unknown'
            
    source['season'] = source['month'].apply(get_season)
    
    # Define columns for aggregation
    hvac_cols = ['electricity_heating_kwh', 'electricity_cooling_kwh']
    water_cols = ['electricity_water_systems_kwh']
    major_appliance_cols = [
        'electricity_refrigerator_kwh', 
        'electricity_clothes_washer_kwh', 
        'electricity_clothes_dryer_kwh', 
        'electricity_cooking_range_kwh', 
        'electricity_dishwasher_kwh'
    ]
    lighting_cols = ['electricity_interior_lighting_kwh', 'electricity_exterior_lighting_kwh']
    
    # Miscellaneous plug loads: Everything else that is an electricity consumption column
    # We can identify them by excluding the ones above and the total/net column
    all_elec_cols = [c for c in source.columns if c.startswith('electricity_')]
    misc_cols = [c for c in all_elec_cols if c not in hvac_cols and c not in water_cols and c not in major_appliance_cols and c not in lighting_cols]
    
    # Group by season and hour
    grouped = source.groupby(['season', 'hour'])
    
    # Aggregate
    agg_data = grouped.agg(
        hvac=(hvac_cols[0], 'sum'), # We will sum the list below
        domestic_water_heating=(water_cols[0], 'sum'),
        major_appliances=(major_appliance_cols[0], 'sum'),
        lighting=(lighting_cols[0], 'sum'),
        miscellaneous_plug_loads=(misc_cols[0], 'sum'),
        total=('net_site_electricity_kwh', 'sum')
    ).reset_index()
    
    # Correctly sum the lists for the aggregated columns
    # The above agg only took the first column of each list. We need to sum all columns in the list.
    # It's safer to create the sums before grouping or use a custom agg.
    # Let's create the summed columns in the source dataframe first.
    
    source['hvac'] = source[hvac_cols].sum(axis=1)
    source['domestic_water_heating'] = source[water_cols].sum(axis=1)
    source['major_appliances'] = source[major_appliance_cols].sum(axis=1)
    source['lighting'] = source[lighting_cols].sum(axis=1)
    source['miscellaneous_plug_loads'] = source[misc_cols].sum(axis=1)
    
    # Now group and sum these new columns
    result = source.groupby(['season', 'hour']).agg(
        hvac=('hvac', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        lighting=('lighting', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum'),
        total=('net_site_electricity_kwh', 'sum')
    ).reset_index()
    
    # Ensure column order
    result = result[['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    return result
