import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Create a datetime object to determine day of week and season
    # Note: YEAR, MONTH, DAY are floats, convert to int for datetime construction
    source = source.copy()
    source['YEAR'] = source['YEAR'].astype(int)
    source['MONTH'] = source['MONTH'].astype(int)
    source['DAY'] = source['DAY'].astype(int)
    
    # Create datetime
    source['datetime'] = pd.to_datetime(source[['YEAR', 'MONTH', 'DAY']])
    
    # 2. Derive 'season'
    # Winter: Dec (12), Jan (1), Feb (2)
    # Spring: Mar (3), Apr (4), May (5)
    # Summer: Jun (6), Jul (7), Aug (8)
    # Fall: Sep (9), Oct (10), Nov (11)
    def get_season(month):
        if month in [12, 1, 2]:
            return 'WINTER'
        elif month in [3, 4, 5]:
            return 'SPRING'
        elif month in [6, 7, 8]:
            return 'SUMMER'
        else:
            return 'FALL'
            
    source['season'] = source['MONTH'].apply(get_season)
    
    # 3. Derive 'daytype'
    # weekday() returns 0 (Mon) to 6 (Sun)
    # WEEKDAY: 0-4, WEEKEND: 5-6
    source['daytype'] = source['datetime'].dt.dayofweek.apply(lambda x: 'WEEKEND' if x >= 5 else 'WEEKDAY')
    
    # 4. Select and rename columns
    # Target columns: season, daytype, hour, temperature_range, constant, coefficient, low_end, high_end
    
    result = pd.DataFrame()
    result['season'] = source['season']
    result['daytype'] = source['daytype']
    result['hour'] = source['HOUR']
    
    # Constant columns based on target distinct values
    result['temperature_range'] = 100998.0
    result['low_end'] = -999.0
    result['high_end'] = 99999.0
    
    # Map CONSTANT and COEFF_1
    result['constant'] = source['CONSTANT']
    result['coefficient'] = source['COEFF_1']
    
    # 5. Sort by hour descending, as observed in target sample
    result = result.sort_values(by='hour', ascending=False).reset_index(drop=True)
    
    # Ensure correct column order
    result = result[['season', 'daytype', 'hour', 'temperature_range', 'constant', 'coefficient', 'low_end', 'high_end']]
    
    return result
