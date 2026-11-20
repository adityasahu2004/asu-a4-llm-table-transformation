import argparse
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from config import ROOT
from strategies import STRATEGIES

def read_results(directory):
    result={}
    for path in sorted((directory/'results').glob('s[1245].jsonl')):
        latest={}
        for line in path.read_text().splitlines():
            row=json.loads(line)
            previous=latest.get(row['case'])
            if previous:
                row['wall_seconds']=max(row.get('wall_seconds',0),previous.get('wall_seconds',0))
            latest[row['case']]=row
        result[path.stem]=list(latest.values())
    return result

def aggregate(rows):
    n=len(rows)
    if not n:
        return {}
    return {'cases':n,
        'autopipeline_accuracy':sum(r['autopipeline']['is_correct'] for r in rows)/n,
        'hard_match_accuracy':sum(r['hard_match']['is_correct'] for r in rows)/n,
        'hard_match_partial':sum(r['hard_match']['accuracy'] for r in rows)/n,
        'execution_rate':sum(r['execution']['status']=='ok' for r in rows)/n,
        'llm_calls':sum(r.get('generation',{}).get('api_attempts',0) for r in rows),
        'marginal_api_calls':sum(r.get('generation',{}).get('marginal_api_attempts',r.get('generation',{}).get('api_attempts',0)) for r in rows),
        'sampled_completions':sum(r.get('generation',{}).get('candidate_count',0) for r in rows),
        'input_tokens':sum(r.get('generation',{}).get('usage',{}).get('prompt_tokens',0) or 0 for r in rows),
        'output_tokens':sum(r.get('generation',{}).get('usage',{}).get('completion_tokens',0) or 0 for r in rows),
        'api_seconds':sum(r.get('generation',{}).get('latency_seconds',0) for r in rows),
        'wall_seconds':sum(r.get('wall_seconds',0) for r in rows),
        'unmeasured_wait_cases':sum(bool(r.get('generation',{}).get('interruption')) for r in rows),
        'interrupted_calendar_wait_seconds':sum(r.get('generation',{}).get('interruption',{}).get('calendar_wait_seconds',0) for r in rows)}

def csv_write(path,rows):
    if not rows:
        return
    with path.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def summarize(directory):
    data=read_results(directory)
    summary=[]
    lengths=[]
    for strategy,rows in data.items():
        evaluation=[r for r in rows if not r['is_demo']]
        if evaluation:
            summary.append({'strategy':strategy,**aggregate(evaluation)})
        for length in sorted({r['length'] for r in evaluation}):
            lengths.append({'strategy':strategy,'length':length,**aggregate([r for r in evaluation if r['length']==length])})
    csv_write(directory/'summary.csv',summary)
    csv_write(directory/'length_summary.csv',lengths)
    figures=directory/'figures'
    figures.mkdir(exist_ok=True)
    if summary:
        plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
        fig,ax=plt.subplots(figsize=(7.2,2.8),layout='constrained')
        names=[r['strategy'] for r in summary]
        x=list(range(len(names)))
        ax.bar([i-0.18 for i in x],[100*r['autopipeline_accuracy'] for r in summary],width=.36,label='Auto-Pipeline',color='#176b87')
        ax.bar([i+0.18 for i in x],[100*r['hard_match_accuracy'] for r in summary],width=.36,label='Hard match',color='#e7a43c')
        ax.set(xticks=x,xticklabels=names,ylabel='Correct evaluation cases (%)',ylim=(0,105))
        ax.legend(frameon=False)
        fig.savefig(figures/'accuracy.png',dpi=180)
        plt.close(fig)
        fig,ax=plt.subplots(figsize=(8,3.6),layout='constrained')
        for si,s in enumerate(names):
            subset=[r for r in lengths if r['strategy']==s]
            ax.bar([r['length']+(si-(len(names)-1)/2)*.24 for r in subset],
                   [100*r['autopipeline_accuracy'] for r in subset],width=.23,label=s)
        ax.set(xlabel='Nominal pipeline length',ylabel='Auto-Pipeline accuracy (%)',ylim=(0,105),xticks=range(1,16))
        ax.legend(frameon=False,ncol=3)
        fig.savefig(figures/'accuracy_by_length.png',dpi=180)
        plt.close(fig)
    return data,summary,lengths

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,default=ROOT)
    args=p.parse_args()
    _,summary,_=summarize(args.output.resolve())
    for row in summary:
        print(row)
