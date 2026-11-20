import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse dates
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Filter for the value present in target (73.0)
    # The target distinct values for hourly cols are [73.0, null]. 84.0 is not present.
    df = df[df['zone_016_cooling_sp'] == 73.0].copy()
    
    # 3. Extract Date and Hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 4. Map 24h hour to 12h AM/PM string
    def hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif h == 12:
            return '12:00 PM'
        elif h < 12:
            return f'{h}:00 AM'
        else:
            return f'{h-12}:00 PM'
            
    df['hour_label'] = df['hour'].apply(hour_to_label)
    
    # 5. Pivot
    # We want Date as index, Hour Label as columns, Value as cell content
    pivot = df.pivot_table(index='date_only', columns='hour_label', values='zone_016_cooling_sp', aggfunc='first')
    
    # 6. Ensure all 24 columns exist in the correct order
    hours_labels = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    pivot = pivot.reindex(columns=hours_labels)
    
    # 7. Format Date column
    pivot.index = pivot.index.strftime('%m/%d/%Y')
    pivot = pivot.reset_index()
    pivot = pivot.rename(columns={'index': 'date'})
    
    return pivot
