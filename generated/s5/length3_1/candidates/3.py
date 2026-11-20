import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse DT_STRATA to datetime. The sample shows '7/2/2016' which is M/D/YYYY.
    # pandas to_datetime handles this flexible format well, but we can be explicit if needed.
    # Using format='%m/%d/%Y' might fail if single digits are not zero-padded in source, 
    # but 'mixed' or default parsing is safer for M/D/YYYY vs MM/DD/YYYY variations.
    # However, looking at the sample "7/2/2016", standard to_datetime handles it.
    dates = pd.to_datetime(source['DT_STRATA'])
    
    # Format as MM/DD/YYYY
    date_str = dates.dt.strftime('%m/%d/%Y')
    
    # Create the date column
    out_df = pd.DataFrame({'date': date_str})
    
    # Select and rename hourly columns
    for h in range(1, 25):
        src_col = f'PCT_HOURLY_{h:02d}00'
        tgt_col = f'Hour {h}'
        out_df[tgt_col] = source[src_col].values
        
    # Ensure correct column order
    cols = ['date'] + [f'Hour {h}' for h in range(1, 25)]
    out_df = out_df[cols]
    
    # Reset index
    out_df = out_df.reset_index(drop=True)
    
    return out_df
