import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map Time Period to month number
    month_map = {
        'January': 1.0, 'February': 2.0, 'March': 3.0, 'April': 4.0,
        'May': 5.0, 'June': 6.0, 'July': 7.0, 'August': 8.0,
        'September': 9.0, 'October': 10.0, 'November': 11.0, 'December': 12.0
    }
    months = source['Time Period'].map(month_map)
    
    # Hour
    hours = source['Hour Ending'].astype('int64')
    
    # Initialize output dataframe
    out = pd.DataFrame(index=source.index)
    out['month'] = months
    out['hour'] = hours
    
    # Prepare demand column, coercing to float
    demand = pd.to_numeric(source['Average Demand Per Home With This End Use [kW]'], errors='coerce')
    
    # Map HVAC
    # Assuming "Remaining Load" maps to hvac
    hvac_mask = source['End Use'] == 'Remaining Load'
    out['hvac'] = np.where(hvac_mask, demand, np.nan)
    
    # Map Water Heating
    # Assuming "Water Heater" maps to water_heating. If not present, it stays 0.0
    wh_mask = source['End Use'] == 'Water Heater'
    out['water_heating'] = np.where(wh_mask, demand, 0.0)
    
    # All other columns are 0
    zero_cols = [
        'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher',
        'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting',
        'lighting', 'plug', 'pool_spa_heater'
    ]
    for col in zero_cols:
        out[col] = 0
        
    # Ensure dtypes
    out['month'] = out['month'].astype('float64')
    out['hour'] = out['hour'].astype('int64')
    out['hvac'] = out['hvac'].astype('float64')
    out['water_heating'] = out['water_heating'].astype('float64')
    
    for col in zero_cols:
        out[col] = out[col].astype('int64')
        
    return out
