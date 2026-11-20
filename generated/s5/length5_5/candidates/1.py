import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'])
    df['date_str'] = df['dt'].dt.strftime('%m/%d/%Y')
    df['hour'] = df['dt'].dt.hour
    
    pivoted = df.pivot_table(index='date_str', columns='hour', values='zone_016_cooling_sp')
    
    # Rename columns
    pivoted.columns = [f'value{h+1}' for h in pivoted.columns]
    
    result = pivoted.reset_index()
    result = result.rename(columns={'date_str': 'date'})
    
    # Define expected columns
    cols = ['date'] + [f'value{i}' for i in range(1, 25)]
    result = result[cols]
    
    # Cast value11 to value22 to int64 if no nulls
    for i in range(11, 23):
        col = f'value{i}'
        if col in result.columns and result[col].notna().all():
            result[col] = result[col].astype(int)
            
    return result
