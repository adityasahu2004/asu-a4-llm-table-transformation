"""Rebuild a six-page main report plus full prompt-template appendix from logs."""
import argparse
from html import escape
import json
from pathlib import Path
import textwrap
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Preformatted, KeepTogether
from config import ROOT, DEMO_CASES
from prompting import SYSTEM
from summarize import summarize, aggregate
from target_constraints import POLICY

STRATEGY_IDS=('s1','s2','s4','s5')

INK=colors.HexColor('#172c3a')
TEAL=colors.HexColor('#176b87')
GOLD=colors.HexColor('#e7a43c')
LIGHT=colors.HexColor('#edf4f6')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleA4',fontName='Helvetica-Bold',fontSize=22,leading=26,textColor=INK,spaceAfter=12))
styles.add(ParagraphStyle(name='SectionA4',fontName='Helvetica-Bold',fontSize=13,leading=16,textColor=TEAL,spaceBefore=10,spaceAfter=6))
styles.add(ParagraphStyle(name='BodyA4',fontName='Helvetica',fontSize=9.5,leading=13.5,textColor=INK,spaceAfter=7))
styles.add(ParagraphStyle(name='SmallA4',fontName='Helvetica',fontSize=8,leading=11,textColor=INK,spaceAfter=5))
styles.add(ParagraphStyle(name='CodeA4',fontName='Courier',fontSize=7,leading=9,textColor=INK,spaceAfter=7))
styles.add(ParagraphStyle(name='FailureA4',fontName='Helvetica-Bold',fontSize=10,leading=12,textColor=TEAL,spaceBefore=7,spaceAfter=3))

def para(text,style='BodyA4'):
    return Paragraph(escape(str(text)),styles[style])

def code(text,width=94):
    lines=[]
    for line in text.splitlines():
        lines.extend(textwrap.wrap(line,width=width,replace_whitespace=False,drop_whitespace=False) or [''])
    return Preformatted('\n'.join(lines),styles['CodeA4'])

def table(rows,widths=None,small=True):
    cells=[[para(str(c),'SmallA4' if small else 'BodyA4') for c in row] for row in rows]
    t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LINEBELOW',(0,0),(-1,0),.6,TEAL),('LINEBELOW',(0,-1),(-1,-1),.4,TEAL),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    return t

def page_footer(canvas,doc):
    canvas.saveState()
    canvas.setStrokeColor(TEAL)
    canvas.line(19*mm,16*mm,A4[0]-19*mm,16*mm)
    canvas.setFont('Helvetica',8)
    canvas.setFillColor(INK)
    canvas.drawString(19*mm,11*mm,'A4 | LLM transformation by target | Smart Building')
    canvas.drawRightString(A4[0]-19*mm,11*mm,str(doc.page))
    canvas.restoreState()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--author',default='Individual submission')
    args=p.parse_args()
    data,summary,lengths=summarize(ROOT)
    for s in STRATEGY_IDS:
        if len([r for r in data.get(s,[]) if not r['is_demo']])!=100:
            raise SystemExit('Report requires 100 evaluation cases for every strategy; run is incomplete.')
    analysis=json.loads((ROOT/'analysis.json').read_text())
    if not analysis.get('reviewed'):
        raise SystemExit('Review and annotate analysis.json first.')
    by_id={r['strategy']:r for r in summary}
    conf=json.loads((ROOT/'results'/'s1_config.json').read_text())
    n_all={s:aggregate(rows) for s,rows in data.items()}
    story=[]
    def h(text): story.append(para(text,'SectionA4'))
    def b(text): story.append(para(text))
    def page(): story.append(PageBreak())
    story.append(para('Synthesizing pandas pipelines\nfrom target tables','TitleA4'))
    b(args.author+' | Individual work | Experiments: November 19-20, 2026')
    h('1. Problem and experimental setup')
    b('Transformation by target (TbT) asks a system to infer a program from a source table and a target specification. Unlike paired transformation-by-example, the target may summarize many source rows, change granularity, or reshape an entire table. A schema-only rename is insufficient for tasks combining aggregation, pivoting, date formatting, and unit conversion.')
    b('This experiment compares three prompting baselines and a fourth custom selection strategy using one fixed model. Table profiles, code interface and validators are shared. Each generated program defines transform(source) and is evaluated on test_0.csv, which is never included in a synthesis prompt or candidate selection. The target is both a visible specification and the reference output, as required by the benchmark.')
    story.append(table([
        ['Setting','Value'],['Model / provider',conf['model']+' / ASU Research Computing'],
        ['Decoding','s1/s2: temperature 0; s4: 0.7. s5 pools both settings. max_tokens=6000; reasoning_effort=none.'],
        ['Self-consistency','k=5 completions in one request; successful training-source output votes.'],
        ['Demonstration holdout',', '.join(DEMO_CASES)],
        ['Scored denominator','100 evaluation cases per strategy; five held-out cases also run as diagnostics.'],
        ['Runtime',f'Python {conf["python"].split()[0]}, pandas {conf["pandas"]}; measured on macOS; Linux backend also tested.'],
        ['Timeout / sampling','120 seconds per candidate/evaluation execution; 12 evenly spaced rows per table.']
    ],[43*mm,128*mm]))
    h('Data split and integrity')
    b('The case split is fixed across all strategies. Three held-out cases supply worked examples; two are reserved but not shown. Cases can share the same underlying building source, so case-level holdout does not establish generalization to unseen buildings. All generated programs come from logged API responses, with no manual edits to scored code. Only schema information and small row samples are sent to the ASU endpoint; benchmark CSVs and credentials are excluded from the submission.')
    b('The assignment specifies both a 600-second grader ceiling and a 120-second runner limit. This implementation uses the stricter 120-second wall-clock limit consistently. API calls use at most three concurrent requests and exponential backoff for transient gateway errors.')
    b('API waiting is separate: the initial client limit was 600 seconds, later extended to 3,600 for recovery. s5 reuses the exact s2/s4 responses, adding no new model draws. Its policy was frozen before its full run, after baseline error inspection; this is exploratory development rather than an independent tuning holdout.')
    page()
    h('2. Prompting and candidate selection')
    b('The shared system prompt requests a concise operator plan and one fenced Python block. The common JSON profile includes exact names, dtypes, row/null/distinct counts, low-cardinality values, first/last date-like cells, and 12 evenly spaced rows. It explicitly distinguishes training and evaluation row counts. Appendix A provides the templates and worked completions.')
    story.append(table([
        ['Strategy','Only ingredient changed','Calls per case'],
        ['s1: zero-shot CoT','Shared prompt, no examples; greedy decoding.','1'],
        ['s2: few-shot CoT','Three fixed source/target, plan and code examples precede the same case block.','1'],
        ['s4: few-shot CoT + SC','Same messages as s2; sample five candidates at temperature 0.7 and vote on execution.','1 request, 5 samples'],
        ['s5: target-constraint reranking','Fixed six-program pool from s2+s4; training-output constraints select a program.','2 logical requests, 6 samples']
    ],[40*mm,102*mm,29*mm]))
    h('Behavioural self-consistency')
    b('s4 executes all five candidates on training data. Failures do not vote. SHA-256 fingerprints combine lexical column order and sorted pandas row hashes, retaining row associations and duplicate multiplicities while ignoring row/column order. The largest cluster wins; ties select its earliest completion index. An empty vote fails. Names and exact numeric representations remain part of the fingerprint, so numerically close outputs can split into different clusters.')
    h('Custom strategy: target-constraint reranking')
    b('s5 executes all six pooled programs on training data. The target prompt sample supplies exact names and date-to-weekday relations, enforced only when at least four distinct dates identify one unique convention: Monday-zero/one or Sunday-zero/one. Loss is lexicographic: schema differences, then weekday violation fractions on up to 128 evenly spaced output rows. A strict improvement replaces the s4 winner; ties retain it, then use earliest index. No case-specific rules, target row counts, test executions or validator scores rank candidates.')
    h('Execution and evaluation')
    b('AST checks reject forbidden imports, I/O, dynamic execution, private attributes and randomness. macOS uses sandbox-exec. Linux uses a kernel seccomp network/process filter plus a Python file audit guard, with no unsafe fallback. Linux validation passed 31 tests and seven benchmark replays. The trusted wrapper transports JSON with dtype metadata, never untrusted pickle. This layered coursework guard can reject valid idioms; it is not a general hostile-code service.')
    b('Auto-Pipeline is the headline metric: equal row counts, column-content matching, ignored names, dropped NaNs and 10% relative numeric tolerance. Auxiliary hard_match aligns names case-insensitively, uses an absolute 0.01 threshold for pure numeric columns, and normalizes string case/whitespace. Both exact flags and mean diagnostic partial credit are reported. Failures score zero; execution rate concerns the selected program on evaluation data.')
    b('Supplied code governs scoring: hard_match deduplicates rows and has a legacy half-table branch; Auto-Pipeline does not require bijective column matching or row associations. Metric gaps therefore are not exclusively naming errors. Original validators, hashes, responses, code, votes and diagnostics are archived.')
    page()
    h('3. Results on the 100 evaluation cases')
    rows=[['Strategy','Auto %','Hard %','Partial %','Exec %','Calls / samples / new','Input / output tokens','Wall min']]
    for r in summary:
        marker='>=' if r['unmeasured_wait_cases'] else ''
        rows.append([r['strategy'],f'{100*r["autopipeline_accuracy"]:.0f}',f'{100*r["hard_match_accuracy"]:.0f}',f'{100*r["hard_match_partial"]:.1f}',f'{100*r["execution_rate"]:.0f}',f'{r["llm_calls"]} / {r["sampled_completions"]} / {r["marginal_api_calls"]}',f'{r["input_tokens"]:,} / {r["output_tokens"]:,}',marker+f'{r["wall_seconds"]/60:.1f}'])
    story.append(table(rows,[15*mm,12*mm,12*mm,14*mm,12*mm,25*mm,53*mm,28*mm]))
    story.append(Spacer(1,4*mm))
    story.append(Image(str(ROOT/'figures'/'accuracy.png'),width=171*mm,height=66.5*mm))
    b('Calls / samples / new means logical standalone requests (including retries), sampled completions, and additional physical API requests. s5 inherits s2+s4 usage and API time; its additional requests are zero. Wall time adds inherited generation latency to local execution. Costs cover 100 cases; ASU charges no fee. Shared requests and overlapping runs must not be summed as elapsed time. Audit replay time is separate; API-only latency is retained in summary.csv.')
    if any(r['unmeasured_wait_cases'] for r in summary):
        b('Times are recorded active intervals, excluding system sleep. Interrupted s4 requests from sleep/connection drops and a cancelled overlapping resume had no recoverable active duration or usage; available calendar intervals are logged separately. The affected time totals are lower bounds (>=), not a complete latency measurement.')
    b('All 105 cases including diagnostics: '+ '; '.join(f'{s}: {n_all[s]["llm_calls"]} logical requests, {n_all[s]["sampled_completions"]} samples' for s in STRATEGY_IDS)+'.')
    b('Development pilots are excluded: zero-shot self-consistency was replaced for response brevity, and an authored demo was corrected before the final s2 run. Pilot logs and separate usage totals are retained in the archive.')
    b(analysis['results_interpretation'])
    page()
    h('4. Pipeline length and observed failure modes')
    story.append(Image(str(ROOT/'figures'/'accuracy_by_length.png'),width=171*mm,height=77*mm))
    grid=[['Length / n']+[s+' auto / partial' for s in STRATEGY_IDS]]
    for length in range(1,16):
        values=[]
        n=0
        for s in STRATEGY_IDS:
            r=next((r for r in lengths if r['strategy']==s and r['length']==length),None)
            n=r['cases'] if r else n
            values.append(f'{100*r["autopipeline_accuracy"]:.0f}% / {100*r["hard_match_partial"]:.1f}%' if r else 'n/a')
        grid.append([f'{length} / {n}']+values)
    story.append(table(grid,[30*mm]+[35.25*mm]*4))
    b('Each cell reports official exact accuracy / mean diagnostic partial credit. Later length groups contain fewer cases, so a single case can change a percentage substantially. Nominal SQL pipeline length is an imperfect proxy for pandas program complexity.')
    b(analysis['length_interpretation'])
    page()
    h('5. Observed failure modes')
    b(analysis['failure_summary'])
    evidence=json.loads((ROOT/'results'/'analysis_evidence.json').read_text())
    failure_rows=[['Official failure family']+list(STRATEGY_IDS)]
    for key,label in [('generation_or_selection_failure','No emitted/selected program'),
                      ('runtime_or_constraint_failure','Runtime / constraint failure'),
                      ('executes_but_official_mismatch','Executed, official mismatch')]:
        failure_rows.append([label]+[evidence['strategies'][s]['official_failure_families'][key] for s in STRATEGY_IDS])
    story.append(table(failure_rows,[71*mm]+[25*mm]*4))
    for example in analysis['failure_examples'][:5]:
        story.append(para(example['category']+' | '+example['strategy']+'/'+example['case'],'FailureA4'))
        story.append(para('Prompt evidence: '+example['prompt_excerpt'],'SmallA4'))
        story.append(code(example['code_excerpt'],100))
        story.append(para('Observed outcome: '+example['validator_observation']+' '+example['explanation'],'SmallA4'))
    page()
    h('6. Interpretation, cost and limitations')
    b(analysis['self_consistency_analysis'])
    b(analysis['custom_strategy_analysis'])
    h('Cost versus accuracy')
    b(analysis['cost_analysis'])
    h('Comparison with SQLMorpher')
    b('SQLMorpher reports 101/105 correct cases (96%) for Prompt-3 with domain information, schema-change hints and iterative prompt optimization [2, Table II]. Its published setup uses GPT-3.5 Turbo 16K at temperature 0 and PostgreSQL 15 [2, Section IV-D]; the handout characterizes the model differently. This is a literature reference rather than a controlled baseline: models, SQL versus pandas, expert hints and repair, samples, case splits and validator details differ. Our fixed ASU model receives no external domain knowledge or repair feedback and is scored on 100 cases. The difference between studies cannot be attributed to prompting alone.')
    h('Limitations and next steps')
    b(analysis['limitations'])
    story.append(para('References [1]-[6] are listed in Appendix B. Benchmark and grading definitions follow the supplied assignment and validator files. AI assistance was used to implement the harness and prepare this report; all scored transformations are generated by the recorded strategy calls.','SmallA4'))
    page()
    h('Appendix A. Full shared prompt and strategy templates')
    b('The following text is the exact shared system message. The per-case schema/sample JSON is substituted at the location specified below. Complete instantiated prompts and raw responses for every case are in logs/<strategy>/<case>/.')
    story.append(code(SYSTEM))
    h('User-message template (identical for all strategies)')
    story.append(code('Infer the transformation from this schema/sample block:\n{\n  "source": <profile(training_0.csv)>,\n  "target": <profile(target.csv)>,\n  "note": "Source row count describes a training sample only, not the evaluation input."\n}'))
    b('Profile fields: rows; columns [{name, dtype, nulls, distinct, distinct_values when distinct <= 12, first_last_non_null for date-like columns}]; sample {columns, data}. Sampling uses sorted unique integer indices from linspace(0, row_count-1, min(12,row_count)); pandas serializes NaNs as null. No test table is profiled.')
    h('s1 template')
    story.append(code('messages = [system: SHARED_SYSTEM, user: USER_TEMPLATE(case)]\ntemperature = 0; n = 1; max_tokens = 6000; reasoning_effort = "none"'))
    h('s2 template')
    story.append(code('messages = [system: SHARED_SYSTEM]\nfor demo in [length1_1, length2_1, length3_1]:\n    append user: USER_TEMPLATE(demo)\n    append assistant: "Operator plan: " + PLAN(demo) + "\\n\\n```python\\n" + CODE(demo) + "```"\nappend user: USER_TEMPLATE(case)\ntemperature = 0; n = 1; max_tokens = 6000; reasoning_effort = "none"'))
    h('s4 template')
    story.append(code('messages = SAME_AS_S2(case)\ntemperature = 0.7; n = 5; max_tokens = 6000; reasoning_effort = "none"\nSelect using training-source output clustering; ties: earliest completion index.'))
    h('s5 custom template and selection policy')
    story.append(code('pool = S4_REQUEST(case) + S2_REQUEST(case)  # same prompts/decoding as above\nExecute all six programs on training_0.csv.\nConventions: Monday0/1, Sunday0/1; require one exact target-sample fit.\nloss = (number_of_schema_differences, sum_of_weekday_violation_fractions)\nSelect a strict loss improvement; retain the s4 winner on ties.\nOtherwise tie-break by earliest pool index (s4 indices 0..4, s2 index 5).\nNever use test rows, validator outputs, target row counts or case-specific rules.\nReuse exact cached requests; a cold run issues the same two requests.'))
    b('All requests specify model=qwen36-27b and x-obleth-boons=off. s2 and s4 messages are identical; only sampling and behavioural selection change. The three worked plan/code completions appear below. Their exact substituted profile messages are retained in demos/demonstrations.json; they use the same USER_TEMPLATE and profiling algorithm, without extra expert rules.')
    demos=json.loads((ROOT/'demos'/'demonstrations.json').read_text())
    for demo in demos:
        story.append(KeepTogether([
            para(demo['case']+' - fixed demonstration completion','SectionA4'),
            code(demo['completion'],110)
        ]))
    page()
    h('Appendix B. References')
    references=[
        '[1] Junwen Yang, Yeye He and Surajit Chaudhuri. Auto-Pipeline: Synthesizing Complex Data Pipelines By-Target Using Reinforcement Learning and Search. PVLDB 14(11), 2563-2575, 2021. DOI: 10.14778/3476249.3476303. https://www.vldb.org/pvldb/vol14/p2563-he.pdf',
        '[2] Ankita Sharma et al. Automatic Data Transformation Using Large Language Model: An Experimental Study on Building Energy Data. IEEE BigData 2023, 1824-1834. DOI: 10.1109/BigData59044.2023.10386931. https://sdm.lbl.gov/oapapers/bigdata23-sharma.pdf',
        '[3] Jason Wei et al. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. NeurIPS 2022. https://arxiv.org/abs/2201.11903',
        '[4] Takeshi Kojima et al. Large Language Models are Zero-Shot Reasoners. NeurIPS 2022. https://arxiv.org/abs/2205.11916',
        '[5] Xuezhi Wang et al. Self-Consistency Improves Chain of Thought Reasoning in Language Models. ICLR 2023. https://arxiv.org/abs/2203.11171',
        '[6] ASU Research Computing. LLM API Access. https://docs.rc.asu.edu/ai/api/ (accessed November 19, 2026).'
    ]
    for reference in references:
        b(reference)
    out=ROOT/'output'/'pdf'/'A4_report.pdf'
    out.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=19*mm,leftMargin=19*mm,topMargin=18*mm,bottomMargin=22*mm,
        title='LLM transformation by target: Smart Building benchmark',author=args.author)
    doc.build(story,onFirstPage=page_footer,onLaterPages=page_footer)
    print(out)

if __name__=='__main__':
    main()
