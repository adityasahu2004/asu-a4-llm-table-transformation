import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Clean Number of Homes
    # Extract leading digits from strings like "11", "0 (Modeled)", "173"
    def parse_homes(val):
        if pd.isna(val):
            return 0
        # Find first sequence of digits
        import re
        match = re.search(r'\d+', str(val))
        if match:
            return int(match.group())
        return 0

    df = source.copy()
    df['num_homes'] = df['Number of Homes in Bin With This End Use Metered'].apply(parse_homes)
    
    # 2. Calculate Weighted Demand
    # Average Demand is float64, may have NaNs
    df['weighted_demand'] = df['Average Demand Per Home With This End Use [kW]'].fillna(0) * df['num_homes']
    
    # 3. Filter for Day Type "All"
    df = df[df['Day Type'] == 'All'].copy()
    
    # 4. Map Time Period to Month
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    df['month'] = df['Time Period'].map(month_map)
    df['hour'] = df['Hour Ending']
    
    # 5. Map End Use to Target Columns
    # Initialize target columns
    df['hvac'] = 0.0
    df['domestic_water_heating'] = 0.0
    df['major_appliances'] = 0.0
    df['lighting'] = 0.0
    df['miscellaneous_plug_loads'] = 0.0
    
    # Helper to assign weighted demand to the correct column
    def assign_column(row):
        cat = row['End Use Category']
        end_use = str(row['End Use']).lower()
        demand = row['weighted_demand']
        
        if cat in ['Kitchen', 'Laundry']:
            return 'major_appliances'
        elif cat == 'Miscellaneous':
            return 'miscellaneous_plug_loads'
        elif cat == 'Lighting':
            return 'lighting'
        elif cat == 'Remaining Load':
            # Heuristic for HVAC
            if any(kw in end_use for kw in ['hvac', 'ac', 'heating', 'cooling', 'air condition']):
                return 'hvac'
            # Heuristic for Water Heating
            elif any(kw in end_use for kw in ['water', 'heater', 'dhw', 'hot water']):
                return 'domestic_water_heating'
            else:
                # Unknown remaining load, ignore or assign to a bucket not in target
                return None
        else:
            return None

    df['target_col'] = df.apply(assign_column, axis=1)
    
    # Filter out rows that don't map to a target column
    df_valid = df[df['target_col'].notna()].copy()
    
    # 6. Aggregate
    # Group by month, hour, target_col and sum weighted_demand
    agg_df = df_valid.groupby(['month', 'hour', 'target_col'])['weighted_demand'].sum().reset_index()
    
    # Pivot to wide format
    pivot_df = agg_df.pivot(index=['month', 'hour'], columns='target_col', values='weighted_demand').reset_index()
    
    # Ensure all target columns exist
    for col in ['hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads']:
        if col not in pivot_df.columns:
            pivot_df[col] = 0.0
            
    # Fill NaNs with 0
    pivot_df = pivot_df.fillna(0)
    
    # 7. Create full grid of months (1-12) and hours (1-24)
    # The target has 288 rows (12*24). We need to ensure all combinations exist.
    months = range(1, 13)
    hours = range(1, 25)
    grid = pd.MultiIndex.from_product([months, hours], names=['month', 'hour'])
    full_df = pd.DataFrame(index=grid).reset_index()
    
    # Merge with pivot_df
    result = full_df.merge(pivot_df, on=['month', 'hour'], how='left')
    
    # Fill remaining NaNs with 0
    result = result.fillna(0)
    
    # 8. Set lighting and total to 0 as per target sample
    result['lighting'] = 0
    result['total'] = 0
    
    # 9. Select and order columns
    cols = ['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    result = result[cols]
    
    # 10. Cast dtypes
    result['month'] = result['month'].astype('int64')
    result['hour'] = result['hour'].astype('int64')
    result['hvac'] = result['hvac'].astype('float64')
    result['domestic_water_heating'] = result['domestic_water_heating'].astype('float64')
    result['major_appliances'] = result['major_appliances'].astype('float64')
    result['lighting'] = result['lighting'].astype('int64')
    result['miscellaneous_plug_loads'] = result['miscellaneous_plug_loads'].astype('float64')
    result['total'] = result['total'].astype('int64')
    
    return result
