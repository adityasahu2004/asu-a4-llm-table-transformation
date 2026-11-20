import ast
import hashlib
import json
from pathlib import Path
import sys
import pytest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from execution import check_code, execute, fingerprint
from prompting import extract_code
from strategies.common import choose_candidate
from validation import validate_autopipeline_style
from config import CONFIG
from strategies.s1 import generate
from summarize import read_results

def test_result_replay_keeps_latest_score_and_original_cost(tmp_path):
    directory=tmp_path/'results'
    directory.mkdir()
    first={'case':'length1_4','wall_seconds':12,'autopipeline':{'is_correct':False}}
    replay={'case':'length1_4','wall_seconds':1,'autopipeline':{'is_correct':True}}
    (directory/'s1.jsonl').write_text(json.dumps(first)+'\n'+json.dumps(replay)+'\n')
    row=read_results(tmp_path)['s1'][0]
    assert row['autopipeline']['is_correct']
    assert row['wall_seconds']==12

def test_cached_replay_uses_frozen_prompt_without_source_profiling(tmp_path,monkeypatch):
    monkeypatch.setattr(CONFIG,'output',tmp_path)
    monkeypatch.setattr(CONFIG,'replay_only',True)
    case=tmp_path/'synthetic_case_without_csvs'
    folder=tmp_path/'logs'/'s1'/case.name
    folder.mkdir(parents=True)
    request={'model':'unit-test','temperature':0,'n':1,'max_tokens':CONFIG.max_tokens,
             'reasoning_effort':CONFIG.reasoning_effort,'messages':[{'role':'user','content':'Frozen prompt.'}]}
    key=hashlib.sha256(json.dumps({'base_url':CONFIG.base_url,**request},sort_keys=True).encode()).hexdigest()
    program='def transform(source):\n return source.copy()\n'
    response={'request_hash':key,'api_attempts':1,'latency_seconds':0,
        'completion':{'choices':[{'index':0,'finish_reason':'stop','message':{'content':'Plan: identity.\n```python\n'+program+'```'}}],'usage':{}}}
    (folder/'prompt.json').write_text(json.dumps(request))
    (folder/'response.json').write_text(json.dumps(response))
    assert generate(case,None,'unit-test')==program

def test_extraction_last_block_and_rejection():
    assert 'return source' in extract_code('```python\nx=1\n```\n```python\ndef transform(source):\n return source\n```')
    with pytest.raises(ValueError):
        extract_code('def transform(source): return source')
    with pytest.raises(SyntaxError):
        extract_code('```python\nthis is invalid python !\n```')

@pytest.mark.parametrize('code',[
    'import os\ndef transform(source): return source',
    'def transform(source): return pd.read_csv("target.csv")',
    'def transform(source): return source.to_pickle("x")',
    'def transform(source): return source.__class__',
    'def transform(source): return eval("1")',
    'from numpy.random import default_rng\ndef transform(source): return source',
    'from numpy import loadtxt\ndef transform(source): return source',
    'def transform(source): return np.fromfile("target.csv")',
    'def transform(source): return np.fromregex("target.csv", "x", float)'])
def test_reject_unsafe_programs(code):
    with pytest.raises(ValueError):
        check_code(code)

def test_vote_behavior_and_tie():
    records=[{'index':i,'execution':{'status':'ok','fingerprint':h}} for i,h in enumerate(['a','b','b','a'])]
    assert choose_candidate(records)[0]==0
    records.append({'index':4,'execution':{'status':'ok','fingerprint':'b'}})
    assert choose_candidate(records)[0]==1
    with pytest.raises(RuntimeError):
        choose_candidate([{'index':0,'execution':{'status':'timeout'}}])

def test_fingerprint_retains_row_associations():
    a=pd.DataFrame({'x':[1,2],'y':[3,4]})
    assert fingerprint(a)==fingerprint(a.iloc[::-1][['y','x']])
    assert fingerprint(a)!=fingerprint(pd.DataFrame({'x':[1,2],'y':[4,3]}))

def test_original_validator_and_case_alignment():
    a=pd.DataFrame({'Name':['A','B'],'value':[1.0,2.0]})
    assert validate_autopipeline_style(a,a,'autopipeline')[1]
    assert validate_autopipeline_style(a.rename(columns={'Name':'NAME'}),a,'hard_match')[1]
    assert not validate_autopipeline_style(a.iloc[:1],a,'autopipeline')[1]
    assert not validate_autopipeline_style(a.assign(extra=3),a,'hard_match')[1]

@pytest.mark.skipif(sys.platform not in {'darwin','linux'},reason='macOS or Linux sandbox required')
def test_subprocess_output_and_timeout():
    source=pd.DataFrame({'x':[1.5,None,3.0],'text':['a','b','c']})
    result,info=execute('def transform(source):\n return source.copy()\n',source)
    assert info['status']=='ok',info
    pd.testing.assert_frame_equal(result,source)
    _,info=execute('def transform(source):\n while True: pass\n',source,timeout=1)
    assert info['status']=='timeout'

@pytest.mark.skipif(sys.platform not in {'darwin','linux'},reason='macOS or Linux sandbox required')
def test_date_output_preserves_temporal_type():
    import datetime
    source=pd.DataFrame({'date':['2020-01-01']})
    result,info=execute('import pandas as pd\ndef transform(source):\n return pd.DataFrame({"date":pd.to_datetime(source["date"]).dt.date})\n',source)
    assert info['status']=='ok',info
    assert isinstance(result.loc[0,'date'],datetime.date)

@pytest.mark.skipif(sys.platform not in {'darwin','linux'},reason='macOS or Linux sandbox required')
@pytest.mark.parametrize('kind',['infinity','small_float','decimal','bytes','nanoseconds','time','timedelta'])
def test_dataframe_transport_preserves_scalar_semantics(kind):
    import datetime
    from decimal import Decimal
    source=pd.DataFrame({'value':['2020-01-01 12:34:56.123456789']})
    if kind in {'infinity','small_float'}:
        source=pd.DataFrame({'value':[1.0,float('inf'),float('-inf')] if kind=='infinity' else [1e-20,-1e-18,0.0]})
        program='def transform(source):\n return source.copy()\n'
    elif kind=='decimal':
        source=pd.DataFrame({'value':[1.25]})
        program='from decimal import Decimal\ndef transform(source):\n return source.assign(value=source["value"].map(lambda x: Decimal(str(x))))\n'
    elif kind=='bytes':
        program='def transform(source):\n return source.assign(value=source["value"].str.encode("utf-8"))\n'
    elif kind=='nanoseconds':
        source=pd.DataFrame({'value':['2020-01-01 12:34:56.123456789',None],'keep':[1,2]})
        program='import pandas as pd\ndef transform(source):\n return source.assign(value=pd.to_datetime(source["value"]))\n'
    elif kind=='timedelta':
        source=pd.DataFrame({'value':[1,None,3],'keep':[1,2,3]})
        program='import pandas as pd\ndef transform(source):\n return source.assign(value=pd.to_timedelta(source["value"],unit="ns"))\n'
    else:
        program='import pandas as pd\ndef transform(source):\n return source.assign(value=pd.to_datetime(source["value"]).dt.time)\n'
    result,info=execute(program,source)
    assert info['status']=='ok',info
    if kind in {'infinity','small_float'}:
        pd.testing.assert_frame_equal(result,source,check_exact=True)
    elif kind=='decimal':
        assert isinstance(result.loc[0,'value'],Decimal)
    elif kind=='bytes':
        assert isinstance(result.loc[0,'value'],bytes)
    elif kind=='nanoseconds':
        assert result.loc[0,'value'].nanosecond==789
        assert result.loc[1,'value'] is pd.NaT
    elif kind=='timedelta':
        assert result.loc[0,'value'].value==1
        assert result.loc[1,'value'] is pd.NaT
    else:
        assert isinstance(result.loc[0,'value'],datetime.time)

@pytest.mark.skipif(sys.platform not in {'darwin','linux'},reason='macOS or Linux sandbox required')
@pytest.mark.parametrize('kind',['string','object_na','object_nat'])
def test_nullable_output_preserves_missing_scalar(kind):
    source=pd.DataFrame({'value':['a',None],'keep':[1,2]})
    if kind=='string':
        expression='source["value"].astype("string")'
    else:
        marker='pd.NaT' if kind=='object_nat' else 'pd.NA'
        expression=f'pd.Series([{marker} if pd.isna(x) else x for x in source["value"]], index=source.index, dtype=object)'
    program='import pandas as pd\ndef transform(source):\n return source.assign(value='+expression+')\n'
    result,info=execute(program,source)
    assert info['status']=='ok',info
    assert result.loc[1,'value'] is (pd.NaT if kind=='object_nat' else pd.NA)

def test_shared_config_writes_are_atomic(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    import json
    from strategies.common import dump
    path=tmp_path/'config.json'
    payloads=[{'worker':i,'values':[i]*100} for i in range(24)]
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda payload:dump(path,payload),payloads))
    assert json.loads(path.read_text()) in payloads
    assert list(tmp_path.iterdir())==[path]

def test_target_weekday_constraints_choose_better_candidate_and_preserve_ties():
    from target_constraints import derive_constraints,constraint_loss,select
    dates=pd.date_range('2020-01-01',periods=14)
    target=pd.DataFrame({'date':dates.strftime('%m/%d/%Y'),'dow':(dates.dayofweek+1)%7})
    profile={'sample':json.loads(target.to_json(orient='split',index=False))}
    constraints=derive_constraints(profile)
    assert constraints['relations'][0]['convention']=='sunday0'
    wrong=target.assign(dow=dates.dayofweek)
    good_loss,_=constraint_loss(target,constraints)
    bad_loss,_=constraint_loss(wrong,constraints)
    assert good_loss<bad_loss
    records=[{'index':0,'execution':{'status':'ok'},'constraint_loss':bad_loss},
             {'index':1,'execution':{'status':'ok'},'constraint_loss':good_loss}]
    assert select(records,0)[0]==1
    records[0]['constraint_loss']=good_loss
    assert select(records,0)[0]==0

def test_target_weekday_constraint_requires_unambiguous_sample():
    from target_constraints import derive_constraints
    dates=pd.date_range('2020-01-06',periods=6)  # no Sunday: ISO and Sunday-zero coincide
    target=pd.DataFrame({'date':dates.strftime('%m/%d/%Y'),'dow':dates.dayofweek+1})
    profile={'sample':json.loads(target.to_json(orient='split',index=False))}
    assert derive_constraints(profile)['relations']==[]

@pytest.mark.skipif(sys.platform!='linux',reason='Linux kernel guard test')
def test_linux_guard_denies_external_file_and_native_network():
    import subprocess
    script='''
import ctypes,errno,platform,tempfile
from pathlib import Path
from linux_sandbox import install
libc=ctypes.CDLL(None,use_errno=True)
number=198 if platform.machine() in {'aarch64','arm64'} else 41
directory=tempfile.mkdtemp()
install(Path(directory))
try:
    open('/etc/passwd').read()
    raise AssertionError('External file read was allowed')
except PermissionError:
    pass
result=libc.syscall(number,2,1,0)
assert result==-1 and ctypes.get_errno()==errno.EPERM
Path(directory,'allowed.txt').write_text('ok')
print('guard checks passed')
'''
    result=subprocess.run([sys.executable,'-c',script],text=True,capture_output=True,timeout=20,
        cwd=Path(__file__).resolve().parents[1])
    assert result.returncode==0,result.stderr
    assert 'guard checks passed' in result.stdout
