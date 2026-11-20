import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the CST column to datetime
    # Format: "Sat 12/01/2012" -> "%a %m/%d/%Y"
    source = source.copy()
    source['date'] = pd.to_datetime(source['CST'], format='%a %m/%d/%Y')
    
    # 2. Derive month and daytype
    # Month name, padded to 10 characters as observed in target distinct values
    source['month'] = source['date'].dt.strftime('%B').str.ljust(10)
    
    # Day type: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: 0=Mon, ..., 4=Fri, 5=Sat, 6=Sun
    source['daytype'] = np.where(source['date'].dt.dayofweek < 5, 'weekday', 'weekend')
    
    # 3. Melt the hourly columns
    # Identify hourly columns (all except CST and the new date/month/daytype cols)
    # The source has columns like "1:00", "2:00", ..., "24:00:00"
    hour_cols = [c for c in source.columns if c not in ['CST', 'date', 'month', 'daytype']]
    
    melted = source.melt(
        id_vars=['month', 'daytype'],
        value_vars=hour_cols,
        var_name='hour_label',
        value_name='value'
    )
    
    # 4. Clean hour labels to integers
    # "1:00" -> 1, "24:00:00" -> 24
    melted['hour'] = melted['hour_label'].str.extract(r'(\d+)').astype(int)
    
    # 5. Aggregate: Mean value for each month, daytype, and hour
    agg_df = melted.groupby(['month', 'daytype', 'hour'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format
    # Columns will be 1, 2, ..., 24
    pivoted = agg_df.pivot_table(
        index=['month', 'daytype'],
        columns='hour',
        values='value'
    ).reset_index()
    
    # 7. Rename columns to hr1, hr2, ..., hr24
    # Ensure all hours 1-24 are present, filling NaNs if necessary (though distinct counts suggest data exists)
    expected_hours = range(1, 25)
    pivoted.columns.name = None # Remove column name
    
    # Rename numeric columns to hrN
    new_col_names = {}
    for col in pivoted.columns:
        if col in expected_hours:
            new_col_names[col] = f'hr{col}'
        else:
            new_col_names[col] = col
            
    pivoted.rename(columns=new_col_names, inplace=True)
    
    # Ensure column order: month, daytype, hr1...hr24
    final_cols = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    result = pivoted[final_cols]
    
    # Sort by month alphabetically to ensure deterministic order
    result = result.sort_values('month').reset_index(drop=True)
    
    return result
