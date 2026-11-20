import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date/time
    source = source.copy()
    source['dt'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    source['month'] = source['dt'].dt.month
    source['hour'] = source['dt'].dt.hour

    # Define columns for each category
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum', 'jacuzzi1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    major_appliances_cols = [
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum',
        'dishwasher1_sum', 'drye1_sum', 'dryg1_sum',
        'microwave1_sum', 'oven1_sum', 'oven2_sum', 'range1_sum',
        'refrigerator1_sum', 'refrigerator2_sum',
        'freezer1_sum', 'icemaker1_sum'
    ]
    
    lighting_cols = [
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum',
        'diningroom1_sum', 'diningroom2_sum',
        'garage1_sum', 'garage2_sum',
        'kitchen1_sum', 'kitchen2_sum',
        'livingroom1_sum', 'livingroom2_sum',
        'office1_sum',
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum',
        'poollight1_sum',
        'shed1_sum',
        'utilityroom1_sum'
    ]
    
    # Misc is everything else that has '_sum' and is not grid/solar (which are system level)
    # We exclude grid_sum, solar_sum, solar2_sum as they are net/injection, not end-use consumption categories in this breakdown usually.
    # We include plugs, EVs, pool pumps, etc.
    all_sum_cols = [c for c in source.columns if c.endswith('_sum')]
    excluded_system_cols = ['grid_sum', 'solar_sum', 'solar2_sum']
    
    misc_cols = [c for c in all_sum_cols if c not in hvac_cols and c not in dwh_cols 
                 and c not in major_appliances_cols and c not in lighting_cols 
                 and c not in excluded_system_cols]

    # Helper to sum columns safely
    def sum_cols(cols):
        if not cols:
            return pd.Series(0, index=source.index)
        return source[cols].sum(axis=1, min_count=0)

    source['hvac'] = sum_cols(hvac_cols)
    source['domestic_water_heating'] = sum_cols(dwh_cols)
    source['major_appliances'] = sum_cols(major_appliances_cols)
    source['lighting'] = sum_cols(lighting_cols)
    source['miscellaneous_plug_loads'] = sum_cols(misc_cols)

    # Aggregate
    agg_df = source.groupby(['month', 'hour']).agg(
        hvac=('hvac', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        lighting=('lighting', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum')
    ).reset_index()

    # Calculate total
    agg_df['total'] = (agg_df['hvac'] + agg_df['domestic_water_heating'] + 
                       agg_df['major_appliances'] + agg_df['lighting'] + 
                       agg_df['miscellaneous_plug_loads'])

    # Ensure integer types for month and hour
    agg_df['month'] = agg_df['month'].astype('int64')
    agg_df['hour'] = agg_df['hour'].astype('int64')

    # Select final columns
    result = agg_df[['month', 'hour', 'hvac', 'domestic_water_heating', 
                     'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    return result
