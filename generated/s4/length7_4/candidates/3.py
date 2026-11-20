import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse date
    source['dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # 2. Derive grouping keys
    # Month name padded to 9 characters
    source['month'] = source['dt'].dt.strftime('%B').str.ljust(9)
    # Day type: weekday or weekend
    source['daytype'] = np.where(source['dt'].dt.weekday < 5, 'weekday', 'weekend')
    
    # 3. Select value columns for aggregation
    value_cols = [f'value{i}' for i in range(1, 25)]
    
    # 4. Group and aggregate (mean)
    grouped = source.groupby(['month', 'daytype'], sort=False)[value_cols].mean()
    
    # 5. Rename columns
    grouped.columns = [f'hr{i}' for i in range(1, 25)]
    
    # 6. Reset index to make month and daytype columns
    result = grouped.reset_index()
    
    # 7. Sort for deterministic output
    # Sort by month (chronological via original dt logic is hard after groupby, 
    # but we can sort by the string representation if we know the order, 
    # or simply sort by the index if we want to preserve input order of groups.
    # The sample order is complex. Standard practice is sorting by keys.
    # Let's sort by month (alphabetical is Jan, Apr, Feb... which is wrong).
    # We need to sort chronologically.
    # Re-attach dt to sort chronologically?
    
    # Better approach: Create a sortable month key
    source['month_sort'] = source['dt'].dt.to_period('M').astype(str)
    source['month'] = source['dt'].dt.strftime('%B').str.ljust(9)
    source['daytype'] = np.where(source['dt'].dt.weekday < 5, 'weekday', 'weekend')
    
    # Groupby using the sort key internally but outputting the formatted month
    # Actually, groupby on ['month_sort', 'daytype']
    grouped = source.groupby(['month_sort', 'daytype'], sort=True)[value_cols].mean()
    grouped.columns = [f'hr{i}' for i in range(1, 25)]
    result = grouped.reset_index()
    
    # Replace month_sort with the formatted month string
    # We need to map '2011-01' -> 'January   '
    # Since we grouped by month_sort, we can reconstruct the month string from the sort key
    # Or simpler: just format the first date of each group? No, we dropped dt.
    # Let's map the sort key back to the formatted string.
    
    def format_month(sort_key):
        # sort_key is like "2011-01"
        year, month_num = sort_key.split('-')
        month_num = int(month_num)
        month_name = pd.to_datetime(month_num, format='%m').strftime('%B')
        return month_name.ljust(9)
        
    result['month'] = result['month_sort'].apply(format_month)
    
    # Drop the sort key column
    result = result.drop(columns=['month_sort'])
    
    # Reorder columns to match target: month, daytype, hr1...
    col_order = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    result = result[col_order]
    
    # Final sort: The sample shows Jan, Feb, Mar... which is chronological.
    # Our sort on 'month_sort' (YYYY-MM) ensures chronological order.
    # Within month, the sample order varies (Jan: weekend, weekday; Feb: weekday, weekend).
    # This implies the order might be determined by the first appearance in the source data 
    # for that month/daytype combination, or a specific custom order.
    # Without clear logic, we will sort by month (chronological) and then daytype alphabetically 
    # as a standard deterministic fallback, or preserve the groupby order if sort=False was used 
    # with a pre-sorted source. The source dates are sorted chronologically.
    # If we groupby sort=False on a sorted dataframe, the order of groups is first-appearance.
    # Let's try to replicate the sample order logic if possible.
    # Jan: 7/3/2011 (Fri, weekday) appears first? No, 7/3 is July.
    # Source starts with 7/3/2011.
    # Sample starts with January.
    # The sample is sorted by Month (Chronological).
    # Within Jan: weekend, weekday.
    # Within Feb: weekday, weekend.
    # This is not alphabetical.
    # Let's look at the source data for Jan 2011.
    # If we sort the source by date, and then groupby with sort=False, 
    # the order of daytypes will be the order they first appear in that month.
    
    # Let's re-do the grouping with sort=False on a chronologically sorted source.
    
    source_sorted = source.sort_values('dt')
    # Recalculate keys on sorted source to be safe
    source_sorted['month'] = source_sorted['dt'].dt.strftime('%B').str.ljust(9)
    source_sorted['daytype'] = np.where(source_sorted['dt'].dt.weekday < 5, 'weekday', 'weekend')
    
    grouped_sorted = source_sorted.groupby(['month', 'daytype'], sort=False)[value_cols].mean()
    grouped_sorted.columns = [f'hr{i}' for i in range(1, 25)]
    result_sorted = grouped_sorted.reset_index()
    
    # Sort by month chronologically to ensure Jan, Feb, Mar order
    # We can use the 'month' string for sorting if we map it back, or just rely on the fact 
    # that groupby with sort=False on sorted data preserves the chronological order of the first key 'month'.
    # However, the groups are (Month, Daytype).
    # The sample is sorted by Month.
    # So we should sort the result by Month.
    
    # Create a sort key for month
    result_sorted['month_sort_key'] = result_sorted['month'].map({
        'January  ': 1, 'February ': 2, 'March    ': 3, 'April    ': 4,
        'May      ': 5, 'June     ': 6, 'July     ': 7, 'August   ': 8,
        'September': 9, 'October  ': 10, 'November ': 11, 'December': 12
    })
    
    result_sorted = result_sorted.sort_values(['month_sort_key']).reset_index(drop=True)
    result_sorted = result_sorted.drop(columns=['month_sort_key'])
    
    return result_sorted
