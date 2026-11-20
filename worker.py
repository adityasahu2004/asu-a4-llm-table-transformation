"""Trusted subprocess wrapper. Never import this module in the runner."""
import json
import datetime
import decimal
import math
import resource
import traceback
import sys
import importlib.util
from pathlib import Path
import numpy as np
import pandas as pd

resource.setrlimit(resource.RLIMIT_CPU, (600,600))
resource.setrlimit(resource.RLIMIT_FSIZE, (512*1024*1024,512*1024*1024))
resource.setrlimit(resource.RLIMIT_NOFILE, (128,128))

try:
    source = pd.read_csv('source.csv', float_precision='round_trip')
    namespace = {'__name__':'generated_transform'}
    with open('transform.py') as stream:
        program = stream.read()
    if sys.platform == 'linux':
        # Load trusted guard and permitted modules before restricting file reads.
        spec=importlib.util.spec_from_file_location('tbt_linux_guard',Path(__file__).with_name('linux_sandbox.py'))
        guard=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guard)
        for module in ['math','re','datetime','calendar','collections','itertools',
                       'functools','statistics','decimal','string','typing','operator']:
            __import__(module)
        try:
            guard.install(Path.cwd())
        except guard.SandboxUnavailable as e:
            print(str(e),file=sys.stderr)
            raise SystemExit(78)
    exec(compile(program, 'transform.py', 'exec'), namespace)
    output = namespace['transform'](source)
    if not isinstance(output, pd.DataFrame):
        raise TypeError('transform must return a pandas DataFrame')
    if not all(isinstance(c,str) for c in output.columns) or output.columns.duplicated().any():
        raise ValueError('Output must have unique string column names')
    payload = json.loads(output.to_json(orient='split', index=False, date_format='iso', date_unit='ns', double_precision=15))
    payload['dtypes'] = [str(t) for t in output.dtypes]
    payload['temporal_objects'] = {}
    payload['special_scalars'] = {}
    payload['native_temporal'] = {}
    # Preserve Python date objects in object columns: silently stringifying them
    # could create a false positive against a CSV string in the official matcher.
    for column_index,column in enumerate(output.columns):
        dtype=output[column].dtype
        is_datetime=pd.api.types.is_datetime64_any_dtype(dtype)
        if is_datetime or pd.api.types.is_timedelta64_dtype(dtype):
            unit=dtype.unit if hasattr(dtype,'unit') else np.datetime_data(dtype)[0]
            timezone=getattr(dtype,'tz',None)
            payload['native_temporal'][column]={'kind':'datetime' if is_datetime else 'timedelta',
                'unit':unit,'timezone':str(timezone) if timezone is not None else None,
                'values':output[column].array.asi8.tolist()}
            continue
        specials=[]
        if pd.api.types.is_numeric_dtype(output[column].dtype):
            numeric=output[column].to_numpy(dtype=float,na_value=np.nan)
            if pd.api.types.is_float_dtype(output[column].dtype):
                # pandas' JSON encoder rounds very small floats to zero even at
                # double_precision=15; the official matcher uses relative error.
                # Python's JSON encoder round-trips finite binary floats instead.
                for i,value in enumerate(numeric):
                    if math.isfinite(value):
                        payload['data'][i][column_index]=float(value)
            for i in np.flatnonzero(np.isinf(numeric)):
                specials.append([int(i),'float',str(numeric[i])])
        if output[column].dtype != object:
            if specials:
                payload['special_scalars'][column]=specials
            continue
        tagged=[]
        for i,value in enumerate(output[column]):
            if value is pd.NaT:
                specials.append([i,'nat',None])
                continue
            if value is pd.NA:
                specials.append([i,'na',None])
                continue
            if isinstance(value,pd.Timestamp):
                tagged.append([i,'timestamp',value.isoformat()])
            elif isinstance(value,datetime.datetime):
                tagged.append([i,'datetime',value.isoformat()])
            elif isinstance(value,datetime.date):
                tagged.append([i,'date',value.isoformat()])
            elif isinstance(value,datetime.time):
                tagged.append([i,'time',value.isoformat()])
            elif isinstance(value,decimal.Decimal):
                specials.append([i,'decimal',str(value)])
            elif isinstance(value,bytes):
                specials.append([i,'bytes',value.hex()])
            elif isinstance(value,(float,np.floating)):
                specials.append([i,'float',repr(float(value))])
        if tagged:
            payload['temporal_objects'][column]=tagged
        if specials:
            payload['special_scalars'][column]=specials
    with open('output.json','w') as stream:
        stream.write(json.dumps(payload, allow_nan=False, separators=(',',':')))
except Exception:
    traceback.print_exc()
    raise SystemExit(1)
