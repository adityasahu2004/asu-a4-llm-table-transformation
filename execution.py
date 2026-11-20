"""Fail-closed execution: AST checks, macOS/Linux guards, and wall timeout.

This is a coursework runner, not a general hostile-code isolation service.
No unsafe subprocess fallback is provided on unsupported platforms.
"""
import ast
import datetime
import decimal
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import numpy as np
import pandas as pd

ALLOWED_IMPORTS = {'pandas','numpy','math','re','datetime','calendar','collections',
                   'itertools','functools','statistics','decimal','string','typing','operator'}
BLOCKED = {'open','eval','exec','compile','__import__','getattr','setattr','delattr',
           'globals','locals','vars','input','breakpoint','help','exit','quit'}

def check_code(code):
    tree = ast.parse(code)
    if not any(isinstance(n, ast.FunctionDef) and n.name == 'transform' for n in tree.body):
        raise ValueError('Missing transform function')
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in n.names] if isinstance(n, ast.Import) else [n.module or '']
            if isinstance(n, ast.ImportFrom) and n.level:
                raise ValueError('Relative imports forbidden')
            if any(x.split('.')[0] not in ALLOWED_IMPORTS for x in names):
                raise ValueError(f'Forbidden import: {names}')
            if any(x.split('.')[0] in {'pandas','numpy'} and '.' in x
                   and not x.startswith(('pandas.api.types','numpy.linalg')) for x in names):
                raise ValueError(f'Forbidden library submodule: {names}')
            if isinstance(n,ast.ImportFrom) and any(a.name=='*' or a.name.startswith(('read_','load','save'))
                    or a.name in {'random','DataSource','fromfile','genfromtxt','memmap','ExcelFile','ExcelWriter','HDFStore'}
                    for a in n.names):
                raise ValueError('Forbidden imported I/O or randomness helper')
        if isinstance(n, ast.Name) and (n.id in BLOCKED or n.id.startswith('__')):
            raise ValueError(f'Forbidden name: {n.id}')
        if isinstance(n, ast.Attribute):
            attr = n.attr
            if (attr.startswith('_') or attr.startswith('read_') or attr.startswith('save')
                or attr.startswith('load') or attr.startswith('write')
                or attr in {'random','ctypes','io','lib','f2py','testing','test','eval','query',
                            'fromfile','fromregex','genfromtxt','memmap','DataSource','dump','ExcelFile','ExcelWriter','HDFStore'}
                or attr.startswith('to_') and attr not in {
                    'to_numeric','to_datetime','to_timedelta','to_numpy','to_frame',
                    'to_list','to_flat_index','to_period','to_timestamp','to_dict','to_records'}):
                raise ValueError(f'Forbidden attribute: {attr}')

def fingerprint(df):
    """Row permutation and column order invariant; row associations are retained."""
    if df.columns.duplicated().any():
        raise ValueError('Duplicate column names')
    frame = df.reindex(columns=sorted(df.columns)).reset_index(drop=True)
    rows = np.sort(pd.util.hash_pandas_object(frame, index=False).to_numpy())
    digest = hashlib.sha256()
    digest.update(json.dumps({'columns':list(frame.columns),'shape':frame.shape}).encode())
    digest.update(rows.tobytes())
    return digest.hexdigest()

def execute(code, source, timeout=120):
    start = time.perf_counter()
    try:
        check_code(code)
    except Exception as e:
        return None, {'status':'constraint_violation','error':str(e),'seconds':time.perf_counter()-start}
    if sys.platform not in {'darwin','linux'} or (sys.platform=='darwin' and not shutil.which('sandbox-exec')):
        return None, {'status':'sandbox_unavailable','error':'Use Linux (seccomp + audit guard) or macOS sandbox-exec.'}
    with tempfile.TemporaryDirectory(prefix='tbt-') as tmp:
        work = Path(tmp).resolve()
        (work/'transform.py').write_text(code)
        source.to_csv(work/'source.csv', index=False)
        worker = Path(__file__).with_name('worker.py').resolve()
        # macOS Python needs broad library metadata reads. Deny coursework data and
        # common credential roots explicitly; the AST gate also forbids generated I/O.
        project = Path(__file__).resolve().parent
        blocked = [project/'.env', project/'logs', project/'demos',
                   Path.home()/'.ssh', Path.home()/'.aws', Path.home()/'.config',
                   Path.home()/'Library/Keychains', Path.home()/'.codex']
        blocked.extend(project.parent.glob('length*/*.csv'))
        deny_reads = ' '.join(f'(subpath {json.dumps(str(p))})' for p in blocked)
        profile = f'''(version 1) (deny default)
        (allow process* sysctl-read mach-lookup file-read*)
        (deny process-fork)
        (deny file-read-data {deny_reads})
        (allow file-write* (subpath {json.dumps(str(work))}) (literal "/dev/null"))'''
        env = {k:v for k,v in os.environ.items() if k in {'PATH','LANG','LC_ALL','TZ','SYSTEMROOT'}}
        env.update({'HOME':str(work),'TMPDIR':str(work),'PYTHONDONTWRITEBYTECODE':'1',
                    'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONHASHSEED':'0'})
        command = [sys.executable,'-I',str(worker)]
        if sys.platform == 'darwin':
            command = ['sandbox-exec','-p',profile] + command
        process = subprocess.Popen(command,
            cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            return None, {'status':'timeout','seconds':time.perf_counter()-start}
        info = {'status':'ok' if process.returncode == 0 else 'execution_error',
                'returncode':process.returncode, 'stdout':stdout.decode(errors='replace')[-4000:],
                'stderr':stderr.decode(errors='replace')[-8000:], 'seconds':time.perf_counter()-start}
        if process.returncode:
            if process.returncode == 78:
                info['status'] = 'sandbox_unavailable'
            return None, info
        try:
            payload = json.loads((work/'output.json').read_text())
            frame = pd.DataFrame(payload['data'], columns=payload['columns'])
            if frame.columns.duplicated().any():
                raise ValueError('Duplicate output columns')
            for c, dtype in zip(frame.columns, payload['dtypes']):
                native=payload.get('native_temporal',{}).get(c)
                if native:
                    if native['kind']=='datetime':
                        values=pd.to_datetime(native['values'],unit=native['unit'],utc=bool(native['timezone']))
                        if native['timezone']:
                            values=values.tz_convert(native['timezone'])
                    else:
                        values=pd.to_timedelta(native['values'],unit=native['unit'])
                    frame[c]=pd.Series(values,index=frame.index).astype(dtype)
                elif dtype.startswith(('int','uint','float','bool','Int','UInt','Float')):
                    frame[c] = frame[c].astype(dtype)
                elif dtype.startswith('datetime64'):
                    frame[c] = pd.to_datetime(frame[c]).astype(dtype)
                elif dtype.startswith('timedelta64'):
                    frame[c] = pd.to_timedelta(frame[c]).astype(dtype)
                elif dtype == 'object':
                    frame[c] = frame[c].astype(object)
                elif dtype == 'string':
                    frame[c] = frame[c].astype('string')
            for c,values in payload.get('temporal_objects',{}).items():
                frame[c] = frame[c].astype(object)
                for i,kind,value in values:
                    constructor = {'date':datetime.date.fromisoformat,'datetime':datetime.datetime.fromisoformat,
                                   'time':datetime.time.fromisoformat,'timestamp':pd.Timestamp}[kind]
                    frame.at[i,c] = constructor(value)
            for c,values in payload.get('special_scalars',{}).items():
                if any(kind!='float' for _,kind,_ in values):
                    frame[c] = frame[c].astype(object)
                for i,kind,value in values:
                    if kind in {'nat','na'}:
                        frame.at[i,c] = pd.NaT if kind=='nat' else pd.NA
                    else:
                        constructor = {'float':float,'decimal':decimal.Decimal,'bytes':bytes.fromhex}[kind]
                        frame.at[i,c] = constructor(value)
            info['shape'] = list(frame.shape)
            info['fingerprint'] = fingerprint(frame)
            return frame, info
        except Exception as e:
            info.update(status='invalid_output', error=str(e))
            return None, info
