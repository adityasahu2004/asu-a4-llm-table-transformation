import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Select relevant columns: Date and hours 1-24
    df = source[['Date'] + [str(i) for i in range(1, 25)]].copy()
    
    # Rename Date to date
    df = df.rename(columns={'Date': 'date'})
    
    # Format date: parse from 'm/d/yyyy' and format to 'mm/dd/yyyy'
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # Rename hour columns from '1'...'24' to 'Hour 1'...'Hour 24'
    hour_cols = {str(i): f'Hour {i}' for i in range(1, 25)}
    df = df.rename(columns=hour_cols)
    
    # Reset index to ensure standard integer index
    return df.reset_index(drop=True)
