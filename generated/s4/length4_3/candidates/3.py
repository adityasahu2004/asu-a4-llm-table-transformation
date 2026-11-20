import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    
    # Format date
    out['date'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # Map hours to 12-hour format labels
    # 1-11 -> 1 AM - 11 AM
    # 12 -> 12 AM
    # 13-23 -> 1 PM - 11 PM
    # 24 -> 12 PM
    
    for h in range(1, 12):
        out[f'{h}:00 AM'] = source[f'PCT_HOURLY_{h:02d}00']
        
    out['12:00 AM'] = source['PCT_HOURLY_1200']
    
    for h in range(13, 24):
        pm_hour = h - 12
        out[f'{pm_hour}:00 PM'] = source[f'PCT_HOURLY_{h:02d}00']
        
    out['12:00 PM'] = source['PCT_HOURLY_2400']
    
    # Reorder columns to match target specification
    target_cols = ['date', 
                   '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', 
                   '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
                   '12:00 AM', 
                   '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
                   '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
                   '12:00 PM']
    
    return out[target_cols].reset_index(drop=True)
