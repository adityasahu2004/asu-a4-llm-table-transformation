import pandas as pd
   
   def transform(source: pd.DataFrame) -> pd.DataFrame:
       # Parse date
       source = source.copy()
       source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
       
       # Extract components
       source['date_part'] = source['dt'].dt.date
       source['hour'] = source['dt'].dt.hour
       source['minute'] = source['dt'].dt.minute
       
       # Calculate value
       source['val'] = source['zone_016'] * source['minute']
       
       # Map hour to target column name
       def map_hour(h):
           if h == 0:
               return '24:00'
           else:
               return f'{h}:00'
       
       source['target_col'] = source['hour'].apply(map_hour)
       
       # Pivot
       pivot = source.pivot_table(index='date_part', columns='target_col', values='val', aggfunc='sum')
       
       # Fill NaN with 0
       pivot = pivot.fillna(0.0)
       
       # Ensure all 24 columns are present
       all_cols = [f'{h}:00' for h in range(1, 24)] + ['24:00']
       for col in all_cols:
           if col not in pivot.columns:
               pivot[col] = 0.0
       
       # Reorder columns
       pivot = pivot[all_cols]
       
       # Format date
       pivot.index = pd.to_datetime(pivot.index).strftime('%a %m/%d/%Y')
       pivot.index.name = 'cst'
       
       # Reset index
       result = pivot.reset_index()
       
       return result
