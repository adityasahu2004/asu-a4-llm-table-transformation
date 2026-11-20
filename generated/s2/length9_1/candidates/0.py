import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying source
    df = source.copy()
    
    # 1. Derive Season
    def get_season(month):
        if month in [12, 1, 2]:
            return "WINTER"
        elif month in [3, 4, 5]:
            return "SPRING"
        elif month in [6, 7, 8]:
            return "SUMMER"
        else:
            return "FALL"
            
    df['season'] = df['MONTH'].apply(get_season)
    
    # 2. Derive Daytype
    # Construct date from YEAR, MONTH, DAY
    # Ensure types are correct for date construction
    df['date'] = pd.to_datetime(
        year=df['YEAR'].astype(int),
        month=df['MONTH'].astype(int),
        day=df['DAY'].astype(int)
    )
    
    def get_daytype(dt):
        # weekday(): Monday=0, Sunday=6
        if dt.weekday() >= 5:
            return "WEEKEND"
        else:
            return "WEEKDAY"
            
    df['daytype'] = df['date'].apply(get_daytype)
    
    # 3. Select and Rename Columns
    # Target columns: season, daytype, hour, temperature_range, constant, coefficient, low_end, high_end
    
    out = pd.DataFrame()
    out['season'] = df['season']
    out['daytype'] = df['daytype']
    out['hour'] = df['HOUR']
    out['temperature_range'] = 100998.0
    out['constant'] = df['CONSTANT']
    out['coefficient'] = df['COEFF_1']
    out['low_end'] = -999.0
    out['high_end'] = 99999.0
    
    # Reset index to ensure clean output
    return out.reset_index(drop=True)
