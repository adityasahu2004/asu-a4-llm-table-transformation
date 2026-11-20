import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Derive season
    def get_season(month):
        if month in [1, 2, 3]:
            return 'SPRING'
        elif month in [4, 5, 6]:
            return 'SUMMER'
        elif month in [7, 8, 9]:
            return 'FALL'
        else:
            return 'WINTER'
    
    source['season'] = source['MONTH'].apply(get_season)
    
    # Derive daytype
    def get_daytype(profile_class):
        if profile_class in ['MP1', 'MT1']:
            return 'WEEKDAY'
        else:
            return 'WEEKEND'
            
    source['daytype'] = source['PROFILE_CLASS'].apply(get_daytype)
    
    # Create target dataframe
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
