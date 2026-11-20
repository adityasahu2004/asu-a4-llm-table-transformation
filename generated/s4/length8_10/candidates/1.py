import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse dates
    source['DateParsed'] = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    source['Month'] = source['DateParsed'].dt.month
    
    # Select hourly columns
    hour_cols = [f'{h}:00' if h < 24 else '24:00:00' for h in range(1, 25)]
    
    # Group by month and calculate mean for each hour
    # Result is a DataFrame indexed by Month, with columns as hours
    grouped = source.groupby('Month')[hour_cols].mean()
    
    # Pivot to have hours as rows and months as columns
    # Transpose the grouped data
    pivoted = grouped.T
    
    # Create the final DataFrame
    result = pd.DataFrame()
    result['hour'] = pivoted.index.astype(int)
    
    # Map month numbers to names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    # Add month columns
    for month_num in range(1, 13):
        if month_num in pivoted.columns:
            result[month_names[month_num]] = pivoted[month_num]
            
    # Ensure all month columns are present (though groupby should handle existing months)
    # Sort by hour
    result = result.sort_values('hour').reset_index(drop=True)
    
    return result
