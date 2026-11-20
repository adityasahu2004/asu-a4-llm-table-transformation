import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map Time Period to month
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    out = pd.DataFrame()
    out['month'] = source['Time Period'].map(month_map).astype('float64')
    out['hour'] = source['Hour Ending'].astype('int64')
    
    # Identify HVAC and Water Heating end uses
    # Assuming "HVAC" is the string for hvac and "Water Heater" for water_heating
    # Other common names might exist, but based on limited info, we check for containment or exact match.
    # Given "End Use" distinct is 15, let's assume standard names.
    
    hvac_mask = source['End Use'].str.contains('HVAC', case=False, na=False)
    wh_mask = source['End Use'].str.contains('Water Heater', case=False, na=False)
    
    # Extract demand
    demand = source['Average Demand Per Home With This End Use [kW]']
    
    # hvac: keep nulls if demand is null, else 0.0
    out['hvac'] = np.where(hvac_mask, demand, 0.0)
    # For non-HVAC, it's 0.0. For HVAC, it's demand (which can be null).
    
    # water_heating: fill nulls with 0.0
    out['water_heating'] = np.where(wh_mask, demand.fillna(0.0), 0.0)
    
    # Other columns are 0
    other_cols = [
        'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher',
        'cooking_range', 'pool_spa_pumps', 'interior_lighting', 
        'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    for col in other_cols:
        out[col] = 0
    
    # Ensure dtypes
    out['month'] = out['month'].astype('float64')
    out['hour'] = out['hour'].astype('int64')
    out['hvac'] = out['hvac'].astype('float64')
    out['water_heating'] = out['water_heating'].astype('float64')
    for col in other_cols:
        out[col] = out[col].astype('int64')
        
    return out
