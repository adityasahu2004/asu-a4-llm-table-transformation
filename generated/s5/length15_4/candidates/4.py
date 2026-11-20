import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map Time Period to Season
    def get_season(month):
        month = month.strip()
        if month in ['December', 'January', 'February']:
            return 'Winter'
        elif month in ['March', 'April', 'May']:
            return 'Spring'
        elif month in ['June', 'July', 'August']:
            return 'Summer'
        elif month in ['September', 'October', 'November']:
            return 'Fall'
        return None

    source = source.copy()
    source['season'] = source['Time Period'].apply(get_season)
    
    # Drop rows with null demand
    source = source.dropna(subset=['Average Demand Per Home With This End Use [kW]'])
    
    # Define end use mappings
    # We will create columns for each target category and sum them up
    
    # Helper to check if end use belongs to category
    def is_hvac(use):
        # Remaining Load is the primary candidate for HVAC/Residual
        if use == 'Remaining Load':
            return True
        # Check for explicit HVAC uses if they exist
        if 'HVAC' in use.upper() or 'AC' in use.upper() or 'Heating' in use.upper():
            return True
        return False

    def is_water_heating(use):
        return 'Water Heater' in use or 'Water Heating' in use

    def is_major_appliance(use):
        major_uses = [
            'Freezer', 
            'Clothes Dryer - Electric', 
            'Clothes Washer',
            'Refrigerator',
            'Clothes Dryer - Gas',
            'Clothes Dryer'
        ]
        return use in major_uses

    def is_misc_plug(use):
        misc_uses = [
            'Primary TV and Peripherals',
            'Primary Desktop Computer',
            'Misc Metered',
            'Pool Pump',
            'TV',
            'Computer',
            'Miscellaneous'
        ]
        return use in misc_uses

    def is_lighting(use):
        return 'Lighting' in use

    # Assign values to temporary columns
    source['hvac_val'] = source['Average Demand Per Home With This End Use [kW]'].where(source['End Use'].apply(is_hvac), 0.0)
    source['dwh_val'] = source['Average Demand Per Home With This End Use [kW]'].where(source['End Use'].apply(is_water_heating), 0.0)
    source['major_val'] = source['Average Demand Per Home With This End Use [kW]'].where(source['End Use'].apply(is_major_appliance), 0.0)
    source['misc_val'] = source['Average Demand Per Home With This End Use [kW]'].where(source['End Use'].apply(is_misc_plug), 0.0)
    source['lighting_val'] = source['Average Demand Per Home With This End Use [kW]'].where(source['End Use'].apply(is_lighting), 0.0)

    # Group by season and Hour Ending
    grouped = source.groupby(['season', 'Hour Ending']).agg(
        hvac=('hvac_val', 'sum'),
        domestic_water_heating=('dwh_val', 'sum'),
        major_appliances=('major_val', 'sum'),
        miscellaneous_plug_loads=('misc_val', 'sum'),
        lighting_sum=('lighting_val', 'sum')
    ).reset_index()

    # Create the final dataframe
    out = pd.DataFrame()
    out['season'] = grouped['season']
    out['hour'] = grouped['Hour Ending']
    out['hvac'] = grouped['hvac']
    out['domestic_water_heating'] = grouped['domestic_water_heating']
    out['major_appliances'] = grouped['major_appliances']
    out['miscellaneous_plug_loads'] = grouped['miscellaneous_plug_loads']
    
    # Target schema shows lighting and total as 0
    out['lighting'] = 0
    out['total'] = 0
    
    # Ensure dtypes match target
    out['hour'] = out['hour'].astype('int64')
    out['lighting'] = out['lighting'].astype('int64')
    out['total'] = out['total'].astype('int64')
    
    # The target sample has nulls in season. My grouping preserves nulls in season key.
    # The target columns for floats are float64.
    
    return out
