import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map Time Period to Season
    def get_season(month):
        if month in ['December', 'January', 'February']:
            return 'Winter'
        elif month in ['March', 'April', 'May']:
            return 'Spring'
        elif month in ['June', 'July', 'August']:
            return 'Summer'
        elif month in ['September', 'October', 'November']:
            return 'Fall'
        else:
            return None

    source = source.copy()
    source['season'] = source['Time Period'].apply(get_season)
    source['hour'] = source['Hour Ending']
    
    # Define End Use mappings
    major_appliances = ['Freezer', 'Clothes Dryer - Electric', 'Clothes Washer']
    misc_plug_loads = ['Primary TV and Peripherals', 'Primary Desktop Computer', 'Misc Metered', 'Pool Pump']
    lighting = ['Lighting']
    water_heating = ['Water Heater'] # Assuming this exists in full data
    hvac = ['Remaining Load'] # Assuming Remaining Load is HVAC
    
    # Function to aggregate
    def aggregate_group(df):
        result = {}
        result['hvac'] = df[df['End Use'].isin(hvac)]['Average Demand Per Home With This End Use [kW]'].sum()
        result['domestic_water_heating'] = df[df['End Use'].isin(water_heating)]['Average Demand Per Home With This End Use [kW]'].sum()
        result['major_appliances'] = df[df['End Use'].isin(major_appliances)]['Average Demand Per Home With This End Use [kW]'].sum()
        result['lighting'] = df[df['End Use'].isin(lighting)]['Average Demand Per Home With This End Use [kW]'].sum()
        result['miscellaneous_plug_loads'] = df[df['End Use'].isin(misc_plug_loads)]['Average Demand Per Home With This End Use [kW]'].sum()
        result['total'] = 0 # Placeholder as per target sample
        return pd.Series(result)

    # Aggregate by season and hour
    seasonal_data = source.groupby(['season', 'hour']).apply(aggregate_group).reset_index()
    
    # Aggregate by hour only for null season
    null_season_data = source.groupby('hour').apply(aggregate_group).reset_index()
    null_season_data['season'] = None
    
    # Combine
    result = pd.concat([seasonal_data, null_season_data], ignore_index=True)
    
    # Ensure correct column types
    result['hour'] = result['hour'].astype(int)
    result['lighting'] = result['lighting'].astype(int)
    result['total'] = result['total'].astype(int)
    
    # Select and order columns
    result = result[['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    return result
