"""Adapters for the supplied content and name-based comparison functions."""
import contextlib
import io
from validators.autopipeline_match import compare_tables
from validators.hard_match import compare_lists_matching

HARD_MATCH_PROVENANCE = 'course-provided hard_match.py and utils.py'

def validate_autopipeline_style(output, target, method='autopipeline'):
    if method == 'hard_match':
        lower = {c.lower():c for c in target.columns}
        output = output.rename(columns={c:lower[c.lower()] for c in output.columns
            if c not in target.columns and c.lower() in lower})
        if output.columns.duplicated().any():
            return 0.0, False, {}, {'error':'duplicate columns after case alignment'}
        with contextlib.redirect_stdout(io.StringIO()):
            return compare_lists_matching(output, target)
    if method == 'autopipeline':
        with contextlib.redirect_stdout(io.StringIO()):
            correct, matched = compare_tables(output, target)
        return float(correct), bool(correct), {}, matched
    raise ValueError(method)

def score(output, target):
    results = {}
    for method in ('autopipeline', 'hard_match'):
        try:
            accuracy, correct, similarities, info = validate_autopipeline_style(output, target, method)
            results[method] = {'accuracy':float(accuracy), 'is_correct':bool(correct),
                               'similarities':similarities, 'info':info}
        except Exception as e:
            results[method] = {'accuracy':0.0, 'is_correct':False, 'error':f'{type(e).__name__}: {e}'}
    results['hard_match_provenance'] = HARD_MATCH_PROVENANCE
    results['exact_schema'] = set(output.columns) == set(target.columns)
    return results
