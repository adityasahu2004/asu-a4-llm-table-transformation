import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse date
    df = source.copy()
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date and hour
    df['date_only'] = df['dt'].dt.normalize()
    df['hour'] = df['dt'].dt.hour + 1  # 1-based hour
    
    # Pivot
    # Columns: date_only, Index: date_only, Values: zone_016_cooling_sp
    # We need to group by date_only and hour.
    # Since the source might have multiple entries or just one, we use pivot_table or pivot.
    # Pivot assumes unique index/columns. If there are duplicates, pivot_table is safer.
    
    pivoted = df.pivot_table(
        index='date_only',
        columns='hour',
        values='zone_016_cooling_sp',
        aggfunc='first' # Take the first value if duplicates exist
    ).reset_index()
    
    # Rename columns to "Hour 1", "Hour 2", ...
    pivoted.rename(columns={i: f'Hour {i}' for i in range(1, 25)}, inplace=True)
    
    # Format date column
    pivoted['date'] = pivoted['date_only'].dt.strftime('%m/%d/%Y')
    
    # Drop the original date_only column
    pivoted.drop(columns=['date_only'], inplace=True)
    
    # Reorder columns to match target: date, Hour 1, ..., Hour 24
    cols = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    pivoted = pivoted[cols]
    
    return pivoted
