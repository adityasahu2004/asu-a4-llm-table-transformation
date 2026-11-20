import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map Time Period to Month
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    out = pd.DataFrame(index=source.index)
    
    # Month: map known months, else NaN
    out['month'] = source['Time Period'].map(month_map).astype('float64')
    
    # Hour
    out['hour'] = source['Hour Ending'].astype('int64')
    
    # Initialize columns
    out['hvac'] = np.nan
    out['water_heating'] = 0.0
    out['refrigerator'] = 0
    out['clothes_washer'] = 0
    out['clothes_dryer'] = 0
    out['dishwasher'] = 0
    out['cooking_range'] = 0
    out['pool_spa_pumps'] = 0
    out['interior_lighting'] = 0
    out['exterior_lighting'] = 0
    out['lighting'] = 0
    out['plug'] = 0
    out['pool_spa_heater'] = 0
    
    # Map HVAC (Remaining Load)
    hvac_mask = source['End Use'] == 'Remaining Load'
    out.loc[hvac_mask, 'hvac'] = source.loc[hvac_mask, 'Average Demand Per Home With This End Use [kW]']
    
    # Map Water Heating (Assuming 'Water Heater' is the end use name)
    wh_mask = source['End Use'] == 'Water Heater'
    out.loc[wh_mask, 'water_heating'] = source.loc[wh_mask, 'Average Demand Per Home With This End Use [kW]']
    
    # Ensure dtypes
    out['month'] = out['month'].astype('float64')
    out['hour'] = out['hour'].astype('int64')
    out['hvac'] = out['hvac'].astype('float64')
    out['water_heating'] = out['water_heating'].astype('float64')
    
    # Integer columns
    int_cols = ['refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 
                'cooking_range', 'pool_spa_pumps', 'interior_lighting', 
                'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    for col in int_cols:
        out[col] = out[col].astype('int64')
        
    return out
