import pandas as pd
def transform(source: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=source.index)
    out['date'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    mapping = {
        'PCT_HOURLY_0100': '1:00 AM',
        'PCT_HOURLY_0200': '2:00 AM',
        'PCT_HOURLY_0300': '3:00 AM',
        'PCT_HOURLY_0400': '4:00 AM',
        'PCT_HOURLY_0500': '5:00 AM',
        'PCT_HOURLY_0600': '6:00 AM',
        'PCT_HOURLY_0700': '7:00 AM',
        'PCT_HOURLY_0800': '8:00 AM',
        'PCT_HOURLY_0900': '9:00 AM',
        'PCT_HOURLY_1000': '10:00 AM',
        'PCT_HOURLY_1100': '11:00 AM',
        'PCT_HOURLY_1200': '12:00 PM',
        'PCT_HOURLY_1300': '1:00 PM',
        'PCT_HOURLY_1400': '2:00 PM',
        'PCT_HOURLY_1500': '3:00 PM',
        'PCT_HOURLY_1600': '4:00 PM',
        'PCT_HOURLY_1700': '5:00 PM',
        'PCT_HOURLY_1800': '6:00 PM',
        'PCT_HOURLY_1900': '7:00 PM',
        'PCT_HOURLY_2000': '8:00 PM',
        'PCT_HOURLY_2100': '9:00 PM',
        'PCT_HOURLY_2200': '10:00 PM',
        'PCT_HOURLY_2300': '11:00 PM',
        'PCT_HOURLY_2400': '12:00 AM',
    }
    
    for src_col, tgt_col in mapping.items():
        out[tgt_col] = source[src_col]
        
    # Ensure column order matches target schema
    target_cols = ['date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM']
    return out[target_cols].reset_index(drop=True)
