import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Construct date for dayofweek calculation
    dates = pd.to_datetime({
        'year': source['YEAR'].astype(int),
        'month': source['MONTH'].astype(int),
        'day': source['DAY'].astype(int)
    })
    
    # Determine season
    months = source['MONTH'].astype(int)
    season = np.where(
        months.isin([12, 1, 2]), 'WINTER',
        np.where(
            months.isin([3, 4, 5]), 'SPRING',
            np.where(
                months.isin([6, 7, 8]), 'SUMMER',
                'FALL'
            )
        )
    )
    
    # Determine daytype
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    dayofweek = dates.dt.dayofweek
    daytype = np.where(dayofweek < 5, 'WEEKDAY', 'WEEKEND')
    
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
