import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map month names to numbers
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    # Filter for 'All' day type to get the aggregate profile
    df = source[source['Day Type'] == 'All'].copy()
    
    # Parse Month
    df['month'] = df['Time Period'].map(month_map)
    
    # Identify categories
    # Major Appliances: Kitchen and Laundry
    df['is_major_appliances'] = df['End Use Category'].isin(['Kitchen', 'Laundry'])
    
    # Miscellaneous Plug Loads
    df['is_misc'] = df['End Use Category'] == 'Miscellaneous'
    
    # HVAC: Look for specific end uses in Remaining Load or generally
    # Assuming specific end uses like 'Central AC', 'Heat Pump', etc. exist in the 15 distinct End Uses
    # We check if the End Use string contains common HVAC keywords
    df['is_hvac'] = df['End Use'].str.contains('AC|Heat|HVAC|Cooling|Heating', case=False, na=False) & (df['End Use Category'] != 'Miscellaneous') & (df['End Use Category'] != 'Lighting') & (df['End Use Category'] != 'Kitchen') & (df['End Use Category'] != 'Laundry')
    # Note: If 'Remaining Load' is the category for HVAC, we might need to check End Use specifically.
    # If 'Remaining Load' is the only category for these, and End Use is 'Remaining Load', this fails.
    # However, if End Use is 'Central AC', Category might be 'Remaining Load' or 'HVAC'.
    # Given 'Remaining Load' is a category in the source, and HVAC is likely inside it or a specific End Use.
    # Let's also check if End Use Category is 'Remaining Load' and End Use is NOT 'Remaining Load' (implying specific meter)
    # Or simpler: Just match keywords in End Use regardless of category, excluding known others.
    
    # Domestic Water Heating
    df['is_dwh'] = df['End Use'].str.contains('Water', case=False, na=False) & (~df['is_hvac'])
    
    # Drop rows with null demand for aggregation, or fill with 0
    df['demand'] = df['Average Demand Per Home With This End Use [kW]'].fillna(0)
    
    # Aggregate
    agg_df = df.groupby(['month', 'Hour Ending']).agg(
        hvac=('is_hvac', lambda x: df.loc[x.index, 'demand'].sum()),
        domestic_water_heating=('is_dwh', lambda x: df.loc[x.index, 'demand'].sum()),
        major_appliances=('is_major_appliances', lambda x: df.loc[x.index, 'demand'].sum()),
        miscellaneous_plug_loads=('is_misc', lambda x: df.loc[x.index, 'demand'].sum())
    ).reset_index()
    
    # Rename Hour Ending to hour
    agg_df = agg_df.rename(columns={'Hour Ending': 'hour'})
    
    # Add constant columns as per target sample
    agg_df['lighting'] = 0
    agg_df['total'] = 0
    
    # Ensure correct column order
    cols = ['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    agg_df = agg_df[cols]
    
    # Ensure dtypes
    agg_df['month'] = agg_df['month'].astype(int)
    agg_df['hour'] = agg_df['hour'].astype(int)
    agg_df['lighting'] = agg_df['lighting'].astype(int)
    agg_df['total'] = agg_df['total'].astype(int)
    
    return agg_df
