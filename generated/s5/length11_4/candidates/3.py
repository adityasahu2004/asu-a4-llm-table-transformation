import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Map Time Period to month number
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    out = pd.DataFrame(index=source.index)
    out['month'] = source['Time Period'].map(month_map).astype('float64')
    out['hour'] = source['Hour Ending'].astype('int64')
    
    # Initialize columns with defaults
    # hvac: NaN, water_heating: 0.0, others: 0
    out['hvac'] = np.nan
    out['water_heating'] = 0.0
    int_cols = [
        'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher',
        'cooking_range', 'pool_spa_pumps', 'interior_lighting', 
        'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    for col in int_cols:
        out[col] = 0
    
    # Helper to map end use to column
    def get_col_name(end_use):
        if pd.isna(end_use):
            return None
        eu = end_use.lower()
        if any(k in eu for k in ['hvac', 'heating', 'cooling', 'space heat', 'space cool', 'furnace', 'ac']):
            return 'hvac'
        if any(k in eu for k in ['water heater', 'water heating']):
            return 'water_heating'
        if any(k in eu for k in ['refrigerator', 'freezer']):
            return 'refrigerator'
        if 'clothes washer' in eu:
            return 'clothes_washer'
        if 'clothes dryer' in eu:
            return 'clothes_dryer'
        if 'dishwasher' in eu:
            return 'dishwasher'
        if any(k in eu for k in ['cooking range', 'range', 'oven', 'microwave']):
            return 'cooking_range'
        if any(k in eu for k in ['pool pump', 'spa pump']):
            return 'pool_spa_pumps'
        if 'interior lighting' in eu:
            return 'interior_lighting'
        if 'exterior lighting' in eu:
            return 'exterior_lighting'
        if 'lighting' in eu:
            return 'lighting'
        if any(k in eu for k in ['tv', 'computer', 'misc', 'plug']):
            return 'plug'
        if any(k in eu for k in ['pool heater', 'spa heater']):
            return 'pool_spa_heater'
        return None

    # Apply mapping
    for idx, row in source.iterrows():
        col_name = get_col_name(row['End Use'])
        val = row['Average Demand Per Home With This End Use [kW]']
        
        if col_name == 'hvac':
            out.at[idx, 'hvac'] = val
        elif col_name == 'water_heating':
            out.at[idx, 'water_heating'] = val
        elif col_name in int_cols:
            out.at[idx, col_name] = int(val) if not pd.isna(val) else 0
            
    return out
