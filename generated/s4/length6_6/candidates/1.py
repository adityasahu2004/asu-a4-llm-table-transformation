import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the source
    df = source.copy()
    
    # Parse the date string 'MM/DD/YYYY' to datetime
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # Format to 'YYYY-MM-DD 00:00:00'
    df['Date'] = df['parsed_date'].dt.strftime('%Y-%m-%d 00:00:00')
    
    # Rename hourly columns from "Hour X" to "Hr X"
    rename_map = {}
    for h in range(1, 25):
        rename_map[f'Hour {h}'] = f'Hr {h}'
    
    df.rename(columns=rename_map, inplace=True)
    
    # Select and order the columns to match the target schema
    target_cols = ['Date'] + [f'Hr {h}' for h in range(1, 25)]
    
    return df[target_cols].reset_index(drop=True)
