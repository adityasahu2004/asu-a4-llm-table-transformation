import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Extract month string from SEASON DAY TYPE
    month_str = source['SEASON DAY TYPE'].str.split().str[0]
    
    # Define summer months
    summer_months = ['June', 'July', 'August']
    
    # Determine season
    season = np.where(month_str.isin(summer_months), 'SUMMER', 'SPRING')
    
    # Determine daytype
    daytype_str = source['SEASON DAY TYPE'].str.split().str[1]
    daytype = np.where(daytype_str == 'WD', 'WEEKDAY', 'WEEKEND')
    
    # Hour
    hour = source['HOUR']
    
    # Low and High ends
    low_end = source['T_MIN_1'].astype('int64')
    high_end = source['T_MAX_1'].astype('int64')
    
    # Temperature range
    temperature_range = high_end - low_end
    
    # Constant and Coefficient are null
    constant = pd.Series([np.nan] * len(source), dtype='float64')
    coefficient = pd.Series([np.nan] * len(source), dtype='float64')
    
    out = pd.DataFrame({
        'season': season,
        'daytype': daytype,
        'hour': hour,
        'temperature_range': temperature_range,
        'constant': constant,
        'coefficient': coefficient,
        'low_end': low_end,
        'high_end': high_end
    })
    
    return out
