import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Derive season from MONTH
    # Months: 12, 1, 2 -> WINTER; 3, 4, 5 -> SPRING; 6, 7, 8 -> SUMMER; 9, 10, 11 -> FALL
    month_map = {
        12.0: 'WINTER', 1.0: 'WINTER', 2.0: 'WINTER',
        3.0: 'SPRING', 4.0: 'SPRING', 5.0: 'SPRING',
        6.0: 'SUMMER', 7.0: 'SUMMER', 8.0: 'SUMMER',
        9.0: 'FALL', 10.0: 'FALL', 11.0: 'FALL'
    }
    out = pd.DataFrame(index=source.index)
    out['season'] = source['MONTH'].map(month_map)
    
    # 2. Derive daytype from YEAR, MONTH, DAY
    # Construct a datetime object to determine weekday
    # YEAR is 2015.0 in sample, but we use the column
    dates = pd.to_datetime(
        source['YEAR'].astype(int).astype(str) + '-' + 
        source['MONTH'].astype(int).astype(str).str.zfill(2) + '-' + 
        source['DAY'].astype(int).astype(str).str.zfill(2)
    )
    # Python weekday: Monday=0, Sunday=6. 
    # Weekend: Saturday (5) and Sunday (6)
    out['daytype'] = np.where(dates.dt.weekday >= 5, 'WEEKEND', 'WEEKDAY')
    
    # 3. Hour
    out['hour'] = source['HOUR']
    
    # 4. Temperature range
    # Target shows constant 100998.0 which is 99999 - (-999)
    out['temperature_range'] = 100998.0
    
    # 5. Constant
    out['constant'] = source['CONSTANT']
    
    # 6. Coefficient
    # Mapping COEFF_1 to coefficient
    out['coefficient'] = source['COEFF_1']
    
    # 7. Low end
    # Target shows constant -999.0
    out['low_end'] = -999.0
    
    # 8. High end
    # Target shows constant 99999.0
    out['high_end'] = 99999.0
    
    return out.reset_index(drop=True)
