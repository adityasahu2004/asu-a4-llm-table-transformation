import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Extract month and day type from SEASON DAY TYPE
    parts = source['SEASON DAY TYPE'].str.split()
    month = parts.str[0]
    dtype_str = parts.str[1]
    
    # Map month to season
    summer_months = ['June', 'July', 'August']
    season = month.map(lambda m: 'SUMMER' if m in summer_months else 'SPRING')
    
    # Map day type
    daytype = dtype_str.map({'WD': 'WEEKDAY', 'WE': 'WEEKEND'})
    
    # Construct output dataframe
    out = pd.DataFrame(index=source.index)
    out['season'] = season
    out['daytype'] = daytype
    out['hour'] = source['HOUR']
    
    # Temperature range calculations
    low_end = source['T_MIN_1']
    high_end = source['T_MAX_1'].astype(int)
    
    out['low_end'] = low_end
    out['high_end'] = high_end
    out['temperature_range'] = (high_end - low_end).astype(int)
    
    # Constant and coefficient are all null in target
    out['constant'] = np.nan
    out['coefficient'] = np.nan
    
    return out.reset_index(drop=True)
