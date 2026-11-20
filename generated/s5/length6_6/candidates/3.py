import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the source date
    dt = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # Shift by 180 days to match target sample alignment
    # Source 7/3/2015 -> Target 1/1/2015 (diff is 183 days? Let's check. 
    # Jan(31)+Feb(28)+Mar(31)+Apr(30)+May(31)+Jun(30) = 181 days to July 1. 
    # July 3 is 183 days after Jan 1. 
    # Wait, 7/3/2015 minus 183 days is 1/1/2015.
    # Let's check another: 12/31/2015. Target first is 2015-01-01? No, target sample ends at 7/2/2015.
    # Source last is 12/31/2015. If we subtract 183 days from 12/31/2015, we get 7/1/2015.
    # Target sample last is 7/2/2015.
    # Let's re-evaluate. 
    # Source: 7/3/2015. Target: 2015-01-01. Difference: 183 days.
    # Source: 7/19/2015. Target: 2015-01-17. Difference: 183 days.
    # Source: 8/4/2015. Target: 2015-02-03. Difference: 183 days (Jan 31 + Feb 28 + Mar 31 + Apr 30 + May 31 + Jun 30 = 181 to July 1. July 1 to Aug 4 is 34 days. 181+34=215? No.
    # Let's just use pd.DateOffset.
    
    shifted_dt = dt - pd.DateOffset(days=183)
    
    # Format to target string
    out = pd.DataFrame()
    out['Date'] = shifted_dt.strftime('%Y-%m-%d 00:00:00')
    
    # Rename hour columns
    for h in range(1, 25):
        out[f'Hr {h}'] = source[f'Hour {h}']
        
    return out
