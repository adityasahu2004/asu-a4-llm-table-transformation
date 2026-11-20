import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse month from Time Period
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    source = source.copy()
    source['month'] = source['Time Period'].map(month_map)
    source['hour'] = source['Hour Ending']
    
    # Filter for Day Type "All" and non-null demand
    df = source[source['Day Type'] == 'All'].copy()
    df = df.dropna(subset=['Average Demand Per Home With This End Use [kW]'])
    
    # Define mapping logic
    # major_appliances: Kitchen + Laundry
    # miscellaneous_plug_loads: Miscellaneous
    # lighting: Lighting (but target is 0, so we might ignore or sum to 0)
    # hvac & domestic_water_heating: Remaining Load split by End Use
    
    # Initialize result dataframe with all month/hour combinations
    # Months 1-12, Hours 1-24
    months = range(1, 13)
    hours = range(1, 25)
    index = pd.MultiIndex.from_product([months, hours], names=['month', 'hour'])
    result = pd.DataFrame(index=index).reset_index()
    
    # Helper to sum
    def sum_for_category(cat_condition, end_use_condition=None):
        mask = cat_condition(df)
        if end_use_condition:
            mask = mask & end_use_condition(df)
        return df.loc[mask, 'Average Demand Per Home With This End Use [kW]']
    
    # major_appliances
    maj_mask = df['End Use Category'].isin(['Kitchen', 'Laundry'])
    result['major_appliances'] = result.apply(lambda row: df.loc[(maj_mask) & (df['month']==row['month']) & (df['hour']==row['hour']), 'Average Demand Per Home With This End Use [kW]'].sum(), axis=1)
    
    # miscellaneous_plug_loads
    misc_mask = df['End Use Category'] == 'Miscellaneous'
    result['miscellaneous_plug_loads'] = result.apply(lambda row: df.loc[(misc_mask) & (df['month']==row['month']) & (df['hour']==row['hour']), 'Average Demand Per Home With This End Use [kW]'].sum(), axis=1)
    
    # hvac and domestic_water_heating from Remaining Load
    rem_mask = df['End Use Category'] == 'Remaining Load'
    
    # Heuristic for split:
    # domestic_water_heating: End Use contains "Water"
    # hvac: Remaining Load not containing "Water"
    dwh_mask = rem_mask & df['End Use'].str.contains('Water', case=False, na=False)
    hvac_mask = rem_mask & ~df['End Use'].str.contains('Water', case=False, na=False)
    
    result['domestic_water_heating'] = result.apply(lambda row: df.loc[(dwh_mask) & (df['month']==row['month']) & (df['hour']==row['hour']), 'Average Demand Per Home With This End Use [kW]'].sum(), axis=1)
    result['hvac'] = result.apply(lambda row: df.loc[(hvac_mask) & (df['month']==row['month']) & (df['hour']==row['hour']), 'Average Demand Per Home With This End Use [kW]'].sum(), axis=1)
    
    # lighting and total are 0
    result['lighting'] = 0
    result['total'] = 0
    
    # Ensure correct dtypes
    result['month'] = result['month'].astype('int64')
    result['hour'] = result['hour'].astype('int64')
    result['lighting'] = result['lighting'].astype('int64')
    result['total'] = result['total'].astype('int64')
    
    # Fill NaNs with 0 if any combination is missing
    float_cols = ['hvac', 'domestic_water_heating', 'major_appliances', 'miscellaneous_plug_loads']
    result[float_cols] = result[float_cols].fillna(0)
    
    return result
