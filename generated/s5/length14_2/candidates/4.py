import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    source = source.copy()
    source['dt'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    source['month'] = source['dt'].dt.month.astype(int)
    source['hour'] = source['dt'].dt.hour.astype(int)
    
    # Define column mappings
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum', 'jacuzzi1_sum', 'poolpump1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    major_appl_cols = [
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum', 'dishwasher1_sum',
        'drye1_sum', 'dryg1_sum', 'microwave1_sum', 'oven1_sum', 'oven2_sum',
        'range1_sum', 'refrigerator1_sum', 'refrigerator2_sum', 'winecooler1_sum',
        'freezer1_sum', 'icemaker1_sum', 'disposal1_sum'
    ]
    
    lighting_cols = [
        'poollight1_sum', 'kitchen1_sum', 'kitchen2_sum', 'livingroom1_sum', 'livingroom2_sum',
        'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum',
        'bathroom1_sum', 'bathroom2_sum', 'office1_sum', 'utilityroom1_sum',
        'garage1_sum', 'garage2_sum', 'diningroom1_sum', 'diningroom2_sum',
        'shed1_sum', 'security1_sum'
    ]
    
    misc_plug_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 'lights_plugs4_sum',
        'lights_plugs5_sum', 'lights_plugs6_sum', 'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum',
        'aquarium1_sum', 'battery1_sum', 'car1_sum', 'car2_sum', 'circpump1_sum',
        'kitchenapp1_sum', 'kitchenapp2_sum', 'sprinkler1_sum', 'sumppump1_sum',
        'wellpump1_sum', 'venthood1_sum'
    ]
    
    # Helper to sum columns safely
    def sum_cols(cols):
        # Fill NaN with 0 for summation
        return source[cols].fillna(0).sum(axis=1)
        
    source['hvac'] = sum_cols(hvac_cols)
    source['domestic_water_heating'] = sum_cols(dwh_cols)
    source['major_appliances'] = sum_cols(major_appl_cols)
    source['lighting'] = sum_cols(lighting_cols)
    source['miscellaneous_plug_loads'] = sum_cols(misc_plug_cols)
    
    # Group by month and hour and sum the 15-min intervals
    agg_data = source.groupby(['month', 'hour']).agg(
        hvac=('hvac', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        lighting=('lighting', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum')
    ).reset_index()
    
    # Calculate total
    agg_data['total'] = (agg_data['hvac'] + agg_data['domestic_water_heating'] + 
                         agg_data['major_appliances'] + agg_data['lighting'] + 
                         agg_data['miscellaneous_plug_loads'])
    
    # Select and order columns
    result = agg_data[['month', 'hour', 'hvac', 'domestic_water_heating', 
                       'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
                       
    return result
