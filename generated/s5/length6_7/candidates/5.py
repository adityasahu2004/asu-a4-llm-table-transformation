import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Define the mapping from source hour columns to target hour columns
    # Source columns are "1:00" to "23:00" and "24:00:00"
    # Target columns are "Hr 1" to "Hr 24"
    
    rename_map = {}
    for h in range(1, 24):
        rename_map[f"{h}:00"] = f"Hr {h}"
    rename_map["24:00:00"] = "Hr 24"
    
    # Select relevant columns and rename
    result = source[["Date"] + [f"{h}:00" for h in range(1, 24)] + ["24:00:00"]].rename(columns=rename_map)
    
    # Reorder columns to match target schema: Date, Hr 1, ..., Hr 24
    target_cols = ["Date"] + [f"Hr {h}" for h in range(1, 25)]
    result = result[target_cols]
    
    return result
