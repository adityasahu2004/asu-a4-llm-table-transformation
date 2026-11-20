"""Build a static review inventory to support semantic inspection."""
import ast
import hashlib
import json
from pathlib import Path
from config import ROOT
from execution import check_code

def inventory(directory=ROOT):
    records=[]
    for path in sorted((directory/'generated').rglob('*.py')):
        text=path.read_text()
        try:
            tree=ast.parse(text)
        except SyntaxError as e:
            records.append({'path':str(path.relative_to(directory)),
                'sha256':hashlib.sha256(text.encode()).hexdigest(),
                'flags':['SyntaxError: '+str(e)]})
            continue
        flags=[]
        try:
            check_code(text)
        except Exception as e:
            flags.append(str(e))
        transform=next((n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='transform'),None)
        if transform:
            parameter=transform.args.args[0].arg if transform.args.args else ''
            if not any(isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load) and n.id==parameter for n in ast.walk(transform)):
                flags.append('Source parameter not used')
        numbers=sorted({str(n.value) for n in ast.walk(tree) if isinstance(n,ast.Constant)
                        and isinstance(n.value,(float,int)) and not isinstance(n.value,bool)})
        if len(numbers)>40:
            flags.append('Many numeric literals: inspect for copied target values')
        for n in ast.walk(tree):
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='DataFrame' and n.args:
                try:
                    value=ast.literal_eval(n.args[0])
                    if value:
                        flags.append('Literal DataFrame data: inspect for target-row embedding')
                except (ValueError,TypeError):
                    pass
            if isinstance(n,(ast.List,ast.Tuple)) and sum(isinstance(v,ast.Constant) and isinstance(v.value,float) for v in n.elts)>4:
                flags.append('Float vector literal: inspect for target-value embedding')
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in {'head','tail'} and n.args:
                if isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,int) and n.args[0].value>1:
                    flags.append('Fixed head/tail row count: inspect generality')
        calls=sorted({ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n,ast.Call)})
        records.append({'path':str(path.relative_to(directory)),'sha256':hashlib.sha256(text.encode()).hexdigest(),
                        'lines':len(text.splitlines()),'numeric_literals':numbers,'calls':calls,'flags':sorted(set(flags))})
    return records

if __name__=='__main__':
    records=inventory()
    (ROOT/'results'/'review_inventory.json').write_text(json.dumps(records,indent=2))
    print(f'{len(records)} program artifacts inventoried; {sum(bool(r["flags"]) for r in records)} flagged.')
