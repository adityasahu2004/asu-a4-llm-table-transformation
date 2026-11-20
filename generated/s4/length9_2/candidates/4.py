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
        else:
            return 'FALL'
            
    source['season'] = source['MONTH'].astype(int).apply(get_season)
    
    # Derive daytype from YEAR, MONTH, DAY
    # Create a date object to determine weekday
    dates = pd.to_datetime(
        source['YEAR'].astype(int).astype(str) + '-' + 
        source['MONTH'].astype(int).astype(str).str.zfill(2) + '-' + 
        source['DAY'].astype(int).astype(str).str.zfill(2),
        format='%Y-%m-%d'
    )
    
    # Weekday: 0=Monday, ..., 5=Saturday, 6=Sunday
    is_weekend = dates.dt.weekday.isin([5, 6])
    source['daytype'] = np.where(is_weekend, 'WEEKEND', 'WEEKDAY')
    
    # Construct output
    out = pd.DataFrame()
    out['season'] = source['season']
    out['daytype'] = source['daytype']
    out['hour'] = source['HOUR']
    out['temperature_range'] = 100998.0
    out['constant'] = source['CONSTANT']
    out['coefficient'] = source['COEFF_1']
    out['low_end'] = -999.0
    out['high_end'] = 99999.0
    
    return out
