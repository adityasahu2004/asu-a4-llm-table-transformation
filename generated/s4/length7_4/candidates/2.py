import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    source['date_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Derive month string with specific padding
    # Target distinct values: "January  ", "February ", "March    ", "April    ", "May      ", "June     ", "July     "
    # This corresponds to .str.ljust(9) on the month name
    source['month'] = source['date_dt'].dt.strftime('%B').str.ljust(9)
    
    # Derive daytype
    # dayofweek: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    source['daytype'] = np.where(source['date_dt'].dt.dayofweek >= 5, 'weekend', 'weekday')
    
    # Select value columns
    value_cols = [f'value{i}' for i in range(1, 25)]
    
    # Group by month and daytype, and calculate mean
    grouped = source.groupby(['month', 'daytype'])[value_cols].mean()
    
    # Rename columns
    grouped = grouped.rename(columns={f'value{i}': f'hr{i}' for i in range(1, 25)})
    
    # Reset index to make month and daytype columns
    result = grouped.reset_index()
    
    return result
