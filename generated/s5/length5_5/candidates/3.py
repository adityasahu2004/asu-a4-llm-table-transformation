import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['date_dt'] = pd.to_datetime(df['date'])
    df['day'] = df['date_dt'].dt.date
    
    # Create sequential index within each day
    df['idx'] = df.groupby('day').cumcount()
    
    # Create column names value1, value2, ...
    df['col_name'] = 'value' + (df['idx'] + 1).astype(str)
    
    # Pivot
    pivot = df.pivot_table(index='day', columns='col_name', values='zone_016_cooling_sp')
    
    # Reset index to make 'day' a column
    pivot = pivot.reset_index()
    
    # Rename 'day' to 'date'
    pivot = pivot.rename(columns={'day': 'date'})
    
    # Format date as MM/DD/YYYY
    pivot['date'] = pd.to_datetime(pivot['date']).dt.strftime('%m/%d/%Y')
    
    # Ensure correct column order
    # The pivot columns might not be sorted numerically (e.g., value1, value10, value2...)
    # We need to sort them to get value1, value2, ..., value24
    cols = ['date'] + sorted([c for c in pivot.columns if c != 'date'], key=lambda x: int(x.replace('value', '')))
    pivot = pivot[cols]
    
    return pivot
