import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Derive season from MONTH
    def get_season(month):
        if month in [12, 1, 2]:
            return 'WINTER'
        elif month in [3, 4, 5]:
            return 'SPRING'
        elif month in [6, 7, 8]:
            return 'SUMMER'
        elif month in [9, 10, 11]:
            return 'FALL'
        return 'UNKNOWN'
    
    source['season'] = source['MONTH'].astype(int).apply(get_season)
    
    # Derive daytype from YEAR, MONTH, DAY
    # Create a datetime object
    source['date_dt'] = pd.to_datetime(
        source['YEAR'].astype(int).astype(str) + '-' + 
        source['MONTH'].astype(int).astype(str).str.zfill(2) + '-' + 
        source['DAY'].astype(int).astype(str).str.zfill(2)
    )
    
    def get_daytype(dt):
        # weekday() returns 0 (Mon) to 6 (Sun)
        if dt.weekday() >= 5:
            return 'WEEKEND'
        else:
            return 'WEEKDAY'
            
    source['daytype'] = source['date_dt'].apply(get_daytype)
    
    # Construct the output dataframe
    out = pd.DataFrame()
    out['season'] = source['season']
    out['daytype'] = source['daytype']
    out['hour'] = source['HOUR']
    
    # Temperature range is constant in target: 99999 - (-999) = 100998
    out['temperature_range'] = 100998.0
    
    # Constant and Coefficient
    # Assuming COEFF_1 is the primary coefficient
    out['constant'] = source['CONSTANT']
    out['coefficient'] = source['COEFF_1']
    
    # Low and High ends are constant in target
    out['low_end'] = -999.0
    out['high_end'] = 99999.0
    
    return out
