import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Extract month and day type from SEASON DAY TYPE
    # Format: "Month WD" or "Month WE"
    month_str = source['SEASON DAY TYPE'].str.split().str[0]
    day_type_str = source['SEASON DAY TYPE'].str.split().str[1]
    
    # Map day type
    daytype_map = {'WD': 'WEEKDAY', 'WE': 'WEEKEND'}
    daytype = day_type_str.map(daytype_map)
    
    # Map season
    # Assuming Jun, Jul, Aug -> SUMMER
    # Assuming Sep, Oct, Nov, Dec -> SPRING
    def get_season(month):
        if month in ['June', 'July', 'August']:
            return 'SUMMER'
        else:
            return 'SPRING'
            
    season = month_str.apply(get_season)
    
    # Hour
    hour = source['HOUR'].astype('int64')
    
    # Temperature range, low_end, high_end
    # Assuming low_end = T_MIN_1, high_end = T_MAX_1
    low_end = source['T_MIN_1'].astype('int64')
    high_end = source['T_MAX_1'].astype('int64')
    temperature_range = (high_end - low_end).astype('int64')
    
    # Constant and Coefficient are null in target
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
