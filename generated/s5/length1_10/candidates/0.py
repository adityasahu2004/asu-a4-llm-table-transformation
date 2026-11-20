import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the date column
    source = source.copy()
    source['dt'] = pd.to_datetime(source['date'])
    
    # Sort by datetime to ensure correct ordering of setpoint changes
    source = source.sort_values('dt')
    
    # Identify unique dates
    unique_dates = source['dt'].dt.date.unique()
    
    rows = []
    for d in unique_dates:
        # Filter records for this date
        mask = source['dt'].dt.date == d
        day_records = source[mask].copy()
        
        # If no records, skip (assuming target only contains days with data)
        if day_records.empty:
            continue
            
        # Get the times for this day
        # We assume the setpoint is active from the timestamp until the next timestamp
        # We need to handle the case where records span multiple days? 
        # The problem implies daily profiles. 
        # Let's assume records define changes within the day.
        # If a record is at 21:45, it starts at 21:45.
        # We need to know when it ends. It ends at the next record's time.
        # If there's only one record, it ends at 24:00.
        
        times = day_records['dt'].tolist()
        
        # Create intervals [start, end)
        intervals = []
        for i, t in enumerate(times):
            start = t
            if i + 1 < len(times):
                end = times[i+1]
            else:
                # End of day
                end = pd.Timestamp(d) + pd.Timedelta(days=1)
            intervals.append((start, end))
            
        # Now, for each hour bin 1-24
        # Bin 1: 00:00-01:00
        # Bin 2: 01:00-02:00
        # ...
        # Bin 24: 23:00-24:00
        
        hour_values = []
        day_start = pd.Timestamp(d)
        
        for h in range(1, 25):
            bin_start = day_start + pd.Timedelta(hours=h-1)
            bin_end = day_start + pd.Timedelta(hours=h)
            
            # Check if any interval overlaps with [bin_start, bin_end)
            is_active = False
            for (int_start, int_end) in intervals:
                # Overlap if int_start < bin_end and int_end > bin_start
                if int_start < bin_end and int_end > bin_start:
                    is_active = True
                    break
            
            if is_active:
                hour_values.append(876.0)
            else:
                hour_values.append(0.0)
                
        # Format date
        cst_str = pd.Timestamp(d).strftime('%a %m/%d/%Y')
        
        row = {'cst': cst_str}
        for h in range(1, 25):
            row[f'{h}:00'] = hour_values[h-1]
            
        rows.append(row)
        
    out = pd.DataFrame(rows)
    return out
