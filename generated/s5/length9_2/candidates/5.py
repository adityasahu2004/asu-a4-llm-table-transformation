import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a datetime object to determine day of week
    # YEAR, MONTH, DAY are floats, convert to int for date construction
    dates = pd.to_datetime(
        year=source['YEAR'].astype(int),
        month=source['MONTH'].astype(int),
        day=source['DAY'].astype(int)
    )
    
    # Determine Season
    # Winter: 12, 1, 2; Spring: 3, 4, 5; Summer: 6, 7, 8; Fall: 9, 10, 11
    month = source['MONTH'].astype(int)
    season = pd.Series(np.where(
        month.isin([12, 1, 2]), 'WINTER',
        np.where(month.isin([3, 4, 5]), 'SPRING',
                 np.where(month.isin([6, 7, 8]), 'SUMMER', 'FALL'))
    ), index=source.index)
    
    # Determine DayType
    # 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    dayofweek = dates.dt.dayofweek
    daytype = pd.Series(np.where(dayofweek >= 5, 'WEEKEND', 'WEEKDAY'), index=source.index)
    
    # Construct Output
    out = pd.DataFrame()
    out['season'] = season
    out['daytype'] = daytype
    out['hour'] = source['HOUR']
    out['temperature_range'] = 100998.0
    out['constant'] = source['CONSTANT']
    out['coefficient'] = source['COEFF_1']
    out['low_end'] = -999.0
    out['high_end'] = 99999.0
    
    return out
