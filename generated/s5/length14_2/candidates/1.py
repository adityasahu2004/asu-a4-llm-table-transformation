import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse timestamp
    source['datetime'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    source['month'] = source['datetime'].dt.month
    source['hour'] = source['datetime'].dt.hour
    
    # Define column mappings
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'pool1_sum', 'pool2_sum', 'poolpump1_sum', 'jacuzzi1_sum',
        'housefan1_sum', 'venthood1_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum'
    ]
    
    dhw_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    major_cols = [
        'refrigerator1_sum', 'refrigerator2_sum',
        'dishwasher1_sum',
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum',
        'drye1_sum', 'dryg1_sum',
        'oven1_sum', 'oven2_sum',
        'microwave1_sum',
        'range1_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum',
        'poollight1_sum'
    ]
    
    misc_cols = [
        'kitchen1_sum', 'kitchen2_sum', 'kitchenapp1_sum', 'kitchenapp2_sum',
        'livingroom1_sum', 'livingroom2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum',
        'diningroom1_sum', 'diningroom2_sum',
        'office1_sum', 'utilityroom1_sum',
        'garage1_sum', 'garage2_sum', 'shed1_sum',
        'aquarium1_sum', 'battery1_sum',
        'car1_sum', 'car2_sum',
        'circpump1_sum',
        'disposal1_sum',
        'icemaker1_sum',
        'pump1_sum',
        'security1_sum', 'sewerpump1_sum', 'sprinkler1_sum', 'sumppump1_sum', 'wellpump1_sum',
        'winecooler1_sum'
    ]

    # Helper to sum columns, treating NaNs as 0
    def sum_cols(cols):
        return source[cols].sum(axis=1, skipna=True)

    # Create temporary dataframe for aggregation
    agg_df = source[['month', 'hour']].copy()
    agg_df['hvac'] = sum_cols(hvac_cols)
    agg_df['domestic_water_heating'] = sum_cols(dhw_cols)
    agg_df['major_appliances'] = sum_cols(major_cols)
    agg_df['lighting'] = sum_cols(lighting_cols)
    agg_df['miscellaneous_plug_loads'] = sum_cols(misc_cols)
    
    # Calculate total
    agg_df['total'] = (agg_df['hvac'] + agg_df['domestic_water_heating'] + 
                       agg_df['major_appliances'] + agg_df['lighting'] + 
                       agg_df['miscellaneous_plug_loads'])

    # Group by month and hour, summing the already summed values (which effectively aggregates the 15-min intervals)
    # Since we summed across columns first, we now sum across rows for each month/hour bin
    result = agg_df.groupby(['month', 'hour'], as_index=False).sum()

    # Ensure correct types
    result['month'] = result['month'].astype(int)
    result['hour'] = result['hour'].astype(int)
    
    # Select and order columns
    result = result[['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    return result
