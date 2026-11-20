import argparse
import json
from pathlib import Path
import re
import zipfile
from config import ROOT
from summarize import read_results

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--asurite',required=True)
    args=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+',args.asurite):
        raise SystemExit('ASURITE must contain letters, digits, underscores or hyphens')
    data=read_results(ROOT)
    for s in ('s1','s2','s4','s5'):
        rows=data.get(s,[])
        if len(rows)!=105 or sum(not r['is_demo'] for r in rows)!=100:
            raise SystemExit(f'{s}: need 105 complete case records (100 evaluation + 5 diagnostics)')
        for r in rows:
            if not (ROOT/r['prompt_path']).exists() or not (ROOT/r['completion_path']).exists():
                raise SystemExit(f'{s}/{r["case"]}: missing API logs')
    analysis=ROOT/'analysis.json'
    if not analysis.exists() or not json.loads(analysis.read_text()).get('reviewed'):
        raise SystemExit('Reviewed analysis.json is required')
    pdf=ROOT/'output'/'pdf'/'A4_report.pdf'
    if not pdf.exists():
        raise SystemExit('Run make_report.py first')
    destination=ROOT/'submission'
    destination.mkdir(exist_ok=True)
    final_pdf=destination/f'A4_{args.asurite}.pdf'
    final_pdf.write_bytes(pdf.read_bytes())
    zip_path=destination/f'A4_{args.asurite}.zip'
    roots=['strategies','validators','demos','results','generated','logs','figures','tests','pilot_archive']
    files=list(ROOT.glob('*.py'))+[ROOT/n for n in ['README.md','requirements.txt','environment-lock.txt','analysis.json','summary.csv','length_summary.csv','Dockerfile','.dockerignore','pytest.ini']]
    for name in roots:
        files.extend(p for p in (ROOT/name).rglob('*') if p.is_file())
    with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in sorted(set(files)):
            relative=path.relative_to(ROOT)
            if path.suffix in {'.csv'} and path.name not in {'summary.csv','length_summary.csv'}:
                raise SystemExit(f'Refusing benchmark CSV: {relative}')
            if any((part.startswith('.') and part!='.dockerignore') or part=='__pycache__' for part in relative.parts) or path.suffix=='.pyc':
                continue
            archive.write(path,relative)
    # Validate the allowlist so a future code change cannot silently include secrets.
    with zipfile.ZipFile(zip_path) as archive:
        assert not any('.env' in p or 'training_0.csv' in p or 'test_0.csv' in p or 'target.csv' in p for p in archive.namelist())
    print(zip_path)
    print(final_pdf)

if __name__=='__main__':
    main()
