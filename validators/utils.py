"""Unmodified helper functions extracted from supplied utils-1.py; unused SQL/ML imports omitted."""

def convert_if_number(s):
    if s is None:
        return None
    try:
        return float(s)
    except ValueError:
        return s

def are_elements_equal(elem1, elem2, tolerance=1e-1):
    elem1 = "" if elem1 is None else elem1
    elem2 = "" if elem2 is None else elem2
    elem1, elem2 = convert_if_number(elem1), convert_if_number(elem2)
    if isinstance(elem1, float) and isinstance(elem2, float):
        # Following AutoPipeline's logic for checking numerical closeness
        # abs(i2-i1) != 0 and abs(i2-i1) / max(abs(i2),abs(i1)) > 0.1 gathered from column_summary.py 
        # return abs(elem1 - elem2) < tolerance
        return (abs(elem1 - elem2) / max(abs(elem1), abs(elem2))) < tolerance
    elif isinstance(elem1, str) and isinstance(elem2, str):
        return elem1.strip().lower() == elem2.strip().lower()
    else:
        return elem1 == elem2
