import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a date object to determine day of week
    # Using pd.to_datetime on year, month, day
    dates = pd.to_datetime({
        'year': source['YEAR'].astype(int),
        'month': source['MONTH'].astype(int),
        'day': source['DAY'].astype(int)
    })
    
    # Determine Season
    months = dates.dt.month
    season = np.select(
        [
            months.isin([12, 1, 2]),
            months.isin([3, 4, 5]),
            months.isin([6, 7, 8]),
            months.isin([9, 10, 11])
        ],
        ['WINTER', 'SPRING', 'SUMMER', 'FALL'],
        default='UNKNOWN'
    )
    
    # Determine Daytype
    # 5 is Saturday, 6 is Sunday
    day_of_week = dates.dt.dayofweek # Monday=0, Sunday=6
    daytype = np.where(day_of_week >= 5, 'WEEKEND', 'WEEKDAY')
    
    # Construct Output
    out = pd.DataFrame({
        'season': season,
        'daytype': daytype,
        'hour': source['HOUR'],
        'temperature_range': 100998.0,
        'constant': source['CONSTANT'],
        'coefficient': source['COEFF_1'],
        'low_end': -999.0,
        'high_end': 99999.0
    })
    
    return out
