import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse datetime
    source['dt'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    source['month'] = source['dt'].dt.month
    source['hour'] = source['dt'].dt.hour

    # Define category columns
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum', 'venthood1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum'
    ]
    
    major_appl_cols = [
        'refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum', 'icemaker1_sum',
        'dishwasher1_sum', 'microwave1_sum', 'oven1_sum', 'oven2_sum', 'range1_sum',
        'clotheswasher1_sum', 'drye1_sum', 'dryg1_sum', 'clotheswasher_dryg1_sum', 'disposal1_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 'lights_plugs4_sum',
        'lights_plugs5_sum', 'lights_plugs6_sum', 'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum',
        'poollight1_sum'
    ]
    
    # Identify all sum columns
    all_sum_cols = [c for c in source.columns if c.endswith('_sum')]
    
    # Misc is everything else
    misc_cols = [c for c in all_sum_cols if c not in hvac_cols and c not in dwh_cols and c not in major_appl_cols and c not in lighting_cols]

    # Aggregate
    agg_dict = {
        'hvac': (hvac_cols, 'sum'),
        'domestic_water_heating': (dwh_cols, 'sum'),
        'major_appliances': (major_appl_cols, 'sum'),
        'lighting': (lighting_cols, 'sum'),
        'miscellaneous_plug_loads': (misc_cols, 'sum')
    }
    
    # Perform aggregation
    # We need to sum each group of columns for each row first, then group by month/hour
    
    for col_name, (cols, agg_method) in agg_dict.items():
        # Select columns, fill NA with 0 for summing, then sum across axis
        source[col_name] = source[cols].fillna(0).sum(axis=1)
        
    # Group by month and hour and sum the categories
    grouped = source.groupby(['month', 'hour']).agg({
        'hvac': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum'
    }).reset_index()
    
    # Calculate total
    grouped['total'] = grouped['hvac'] + grouped['domestic_water_heating'] + grouped['major_appliances'] + grouped['lighting'] + grouped['miscellaneous_plug_loads']
    
    # Select and order columns
    result = grouped[['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    return result
