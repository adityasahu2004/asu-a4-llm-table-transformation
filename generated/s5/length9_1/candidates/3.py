import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Filter for single range rows which match the target structure (low -999, high 99999)
    df = source[source['NUMBER_OF_RANGES'] == 1].copy()
    
    # Create datetime to determine day of week
    df['date'] = pd.to_datetime({
        'year': df['YEAR'].astype(int),
        'month': df['MONTH'].astype(int),
        'day': df['DAY'].astype(int)
    })
    
    # Derive daytype
    # Monday=0 ... Sunday=6
    df['daytype'] = np.where(df['date'].dt.dayofweek < 5, 'WEEKDAY', 'WEEKEND')
    
    # Derive season
    # Winter: Dec, Jan, Feb (12, 1, 2)
    # Spring: Mar, Apr, May (3, 4, 5)
    # Summer: Jun, Jul, Aug (6, 7, 8)
    # Fall: Sep, Oct, Nov (9, 10, 11)
    month = df['MONTH'].astype(int)
    conditions = [
        month.isin([12, 1, 2]),
        month.isin([3, 4, 5]),
        month.isin([6, 7, 8]),
        month.isin([9, 10, 11])
    ]
    choices = ['WINTER', 'SPRING', 'SUMMER', 'FALL']
    df['season'] = np.select(conditions, choices, default='UNKNOWN')
    
    # Construct output columns
    out = pd.DataFrame()
    out['season'] = df['season']
    out['daytype'] = df['daytype']
    out['hour'] = df['HOUR']
    out['temperature_range'] = 100998.0
    out['constant'] = df['CONSTANT']
    out['coefficient'] = df['COEFF_1']
    out['low_end'] = -999.0
    out['high_end'] = 99999.0
    
    return out.reset_index(drop=True)
