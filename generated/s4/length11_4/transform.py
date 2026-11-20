import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map month names to numbers
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    # Create output dataframe
    out = pd.DataFrame(index=source.index)
    
    # Month
    out['month'] = source['Time Period'].map(month_map).astype('float64')
    
    # Hour
    out['hour'] = source['Hour Ending'].astype('int64')
    
    # Initialize demand columns
    # hvac and water_heating are float64
    out['hvac'] = np.nan
    out['water_heating'] = 0.0
    
    # Other columns are int64 and appear to be 0 in the target schema
    int_cols = [
        'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher',
        'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting',
        'lighting', 'plug', 'pool_spa_heater'
    ]
    for col in int_cols:
        out[col] = 0
        
    # Map End Use to hvac and water_heating
    # Assuming 'Remaining Load' maps to hvac based on typical residual load usage
    # Assuming 'Water Heating' maps to water_heating
    # Note: The source sample does not explicitly show 'Water Heating' or 'HVAC' strings,
    # but 'Remaining Load' is present.
    
    # Identify rows for Remaining Load
    mask_hvac = source['End Use'].str.lower().isin(['remaining load', 'hvac'])
    out.loc[mask_hvac, 'hvac'] = source.loc[mask_hvac, 'Average Demand Per Home With This End Use [kW]']
    
    # Identify rows for Water Heating
    mask_wh = source['End Use'].str.lower().isin(['water heating', 'water heater'])
    out.loc[mask_wh, 'water_heating'] = source.loc[mask_wh, 'Average Demand Per Home With This End Use [kW]']
    
    # Ensure dtypes
    out['month'] = out['month'].astype('float64')
    out['hour'] = out['hour'].astype('int64')
    out['hvac'] = out['hvac'].astype('float64')
    out['water_heating'] = out['water_heating'].astype('float64')
    for col in int_cols:
        out[col] = out[col].astype('int64')
        
    return out.reset_index(drop=True)
