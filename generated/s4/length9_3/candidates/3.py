import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Derive season and daytype
    parts = source['SEASON DAY TYPE'].str.split(n=1, expand=True)
    months = parts[0]
    types = parts[1]
    
    season = months.apply(lambda m: 'SUMMER' if m in ['June', 'July', 'August'] else 'SPRING')
    daytype = types.apply(lambda t: 'WEEKDAY' if t == 'WD' else 'WEEKEND')
    
    # Construct the output DataFrame
    out = pd.DataFrame()
    out['season'] = season
    out['daytype'] = daytype
    out['hour'] = source['HOUR'].astype('int64')
    out['low_end'] = source['T_MIN_1'].astype('int64')
    out['high_end'] = source['T_MAX_1'].astype('int64')
    out['temperature_range'] = out['high_end'] - out['low_end']
    out['constant'] = np.nan
    out['coefficient'] = np.nan
    
    return out[['season', 'daytype', 'hour', 'temperature_range', 'constant', 'coefficient', 'low_end', 'high_end']]
