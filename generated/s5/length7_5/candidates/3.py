import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Derive month name
    month = dt.dt.strftime('%B')
    
    # Derive daytype (0=Mon, 1=Tue, ..., 5=Sat, 6=Sun)
    # Weekend if dayofweek is 5 or 6
    daytype = dt.dt.dayofweek.apply(lambda d: 'weekend' if d >= 5 else 'weekday')
    
    # Map hourly columns
    # Source columns: 
    # 1:00 AM -> hr1
    # 2:00 AM -> hr2
    # ...
    # 11:00 AM -> hr11
    # 12:00 PM -> hr12
    # 1:00 PM -> hr13
    # ...
    # 11:00 PM -> hr23
    # 12:00 AM -> hr24
    
    mapping = {
        '1:00 AM': 'hr1',
        '2:00 AM': 'hr2',
        '3:00 AM': 'hr3',
        '4:00 AM': 'hr4',
        '5:00 AM': 'hr5',
        '6:00 AM': 'hr6',
        '7:00 AM': 'hr7',
        '8:00 AM': 'hr8',
        '9:00 AM': 'hr9',
        '10:00 AM': 'hr10',
        '11:00 AM': 'hr11',
        '12:00 PM': 'hr12',
        '1:00 PM': 'hr13',
        '2:00 PM': 'hr14',
        '3:00 PM': 'hr15',
        '4:00 PM': 'hr16',
        '5:00 PM': 'hr17',
        '6:00 PM': 'hr18',
        '7:00 PM': 'hr19',
        '8:00 PM': 'hr20',
        '9:00 PM': 'hr21',
        '10:00 PM': 'hr22',
        '11:00 PM': 'hr23',
        '12:00 AM': 'hr24'
    }
    
    out = pd.DataFrame()
    out['month'] = month
    out['daytype'] = daytype
    
    for src_col, tgt_col in mapping.items():
        out[tgt_col] = source[src_col]
        
    # Ensure column order
    cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    out = out[cols]
    
    return out.reset_index(drop=True)
