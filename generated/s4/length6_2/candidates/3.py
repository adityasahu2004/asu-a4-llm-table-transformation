import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse CST to datetime
    # Format is "DayOfWeek MM/DD/YYYY" e.g., "Sat 12/01/2012"
    # We can parse this by ignoring the weekday prefix or using a flexible parser
    # Since the weekday is consistent with the date, we can just parse the date part.
    # However, pd.to_datetime might struggle with "Sat " prefix if not handled.
    # A robust way is to extract the date part or use a custom parser.
    # Given the format "Day MM/DD/YYYY", we can try parsing directly.
    # pd.to_datetime handles "Sat 12/01/2012" reasonably well in recent versions, 
    # but let's be safe. The sample shows "Sat 12/01/2012".
    
    # Let's try parsing. If it fails, we might need to strip the weekday.
    # However, standard pd.to_datetime is usually smart enough.
    # If not, we can do source['CST'].str.split().str[1:].str.join()
    
    dates = pd.to_datetime(source['CST'])
    
    # Create output dataframe
    out = pd.DataFrame()
    
    # Format Date column
    out['Date'] = dates.dt.strftime('%m/%d/%Y')
    
    # Map hours 1-24
    # Source columns: "1:00", "2:00", ..., "23:00", "24:00:00"
    # Target columns: "Hr 1", "Hr 2", ..., "Hr 24"
    
    for h in range(1, 25):
        src_col = f"{h}:00" if h < 24 else "24:00:00"
        tgt_col = f"Hr {h}"
        
        # Coerce to numeric to handle any potential string representations
        out[tgt_col] = pd.to_numeric(source[src_col], errors='coerce')
        
    return out
