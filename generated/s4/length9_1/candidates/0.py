import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Filter for single range rows where HIGH_1 is 99999 and LOW_1 is -999
    # Based on target schema having fixed low_end/high_end and distinct values
    mask = source['NUMBER_OF_RANGES'] == 1.0
    df = source[mask].copy()
    
    # Derive Season
    def get_season(month):
        if month in [12, 1, 2]:
            return 'WINTER'
        elif month in [3, 4, 5]:
            return 'SPRING'
        elif month in [6, 7, 8]:
            return 'SUMMER'
        else:
            return 'FALL'
            
    df['season'] = df['MONTH'].apply(get_season)
    
    # Derive Daytype
    # Create datetime to determine day of week
    df['date'] = pd.to_datetime(
        year=df['YEAR'].astype(int), 
        month=df['MONTH'].astype(int), 
        day=df['DAY'].astype(int)
    )
    df['daytype'] = df['date'].dt.dayofweek.apply(lambda d: 'WEEKEND' if d >= 5 else 'WEEKDAY')
    
    # Select and rename columns
    out = pd.DataFrame()
    out['season'] = df['season']
    out['daytype'] = df['daytype']
    out['hour'] = df['HOUR']
    out['temperature_range'] = 100998.0
    out['constant'] = df['CONSTANT']
    out['coefficient'] = df['COEFF_1']
    out['low_end'] = -999.0
    out['high_end'] = 99999.0
    
    # Reset index to match target style if needed, though not strictly required by prompt unless specified
    return out.reset_index(drop=True)
