# ASU Assignment 4: LLM table transformation

Private coursework repository for ASURITE **Asahu126**.

- [PDF report](submission/A4_Asahu126.pdf)
- [Gradescope code ZIP](submission/A4_Asahu126.zip)

| Strategy | Official accuracy | Auxiliary accuracy |
|---|---:|---:|
| Zero-shot CoT | 28% | 21% |
| Few-shot CoT | 44% | 38% |
| Few-shot CoT + self-consistency | 49% | 39% |
| Target-constraint reranking | 50% | 40% |

All four strategies were evaluated on 105 cases, with the same five demonstration
cases excluded from each 100-case accuracy denominator. The repository contains
code, generated programs, API logs, results and the final report. The benchmark
CSV files and API key are excluded. Keep this coursework private.

# A4: transformation by target with a fixed LLM

Four strategies synthesize `transform(source: pd.DataFrame) -> pd.DataFrame`:

| ID | Strategy | Temperature | Completions per case |
|---|---|---:|---:|
| s1 | Zero-shot CoT (explicit operator plan) | 0 | 1 |
| s2 | Few-shot CoT (three fixed worked examples) | 0 | 1 |
| s4 | Few-shot CoT plus behavioural self-consistency | 0.7 | 5 |
| s5 | Target-constraint reranking of the fixed s2+s4 pool | 0 and 0.7 | 1 + 5 |

Model: **qwen36-27b**, ASU gateway, `reasoning_effort=none`, `max_tokens=6000`.
Every request disables gateway add-ons with `x-obleth-boons: off`.
No API sampling seed is supplied; fresh stochastic runs can differ. Cached raw
completions support exact program/score replay without resampling.
Prompts require a visible concise operator plan followed by a fenced Python program.
No generated program is hand-edited. Hand-authored demonstrations live in `demos/`
and never contribute to evaluation accuracy.

Development pilots are excluded from the final comparison. An early authored
day-of-week demonstration was corrected before the final few-shot run. A short
zero-shot self-consistency pilot was replaced by few-shot self-consistency because
the examples produced shorter completions; s2 versus s4 isolates sampling.
`results/development_pilots.json` records their API overhead separately. Pilot
completions are retained under `pilot_archive/`, including in the zip, and are
not part of the four complete scored strategies.

## Environment and data

Execution supports **macOS `sandbox-exec` and Linux x86-64/ARM64**. Linux installs
a kernel seccomp filter denying network/process creation plus a Python file audit
guard restricted to scratch files and installed libraries. The AST gate is also
required. This is a constrained coursework sandbox, not a general native-code
security service. Unsupported platforms/kernels fail closed. Windows users can
use Linux/WSL2 or Docker. Original scored runs use macOS; Linux integration and
security tests run separately in the supplied container.

Use Python 3.14 for the recorded environments. The recorded run used Python 3.14.4, pandas 3.1.1.
`environment-lock.txt` preserves that environment; `requirements.txt` lists the
necessary direct dependencies. Local and Linux validation metadata are in results/.
For exact replay environments, use `python -m pip install -r environment-lock.txt`
on macOS or `python -m pip install -r results/linux_environment_lock.txt` on Linux.
The host lock also includes optional PDF inspection tooling; the minimal direct
dependencies are sufficient to run the benchmark and generate the report.

Portable container smoke test (no API key or benchmark required):

```bash
docker build -t a4-tbt-audit .
docker run --rm --network none --security-opt no-new-privileges --cap-drop ALL a4-tbt-audit python -m pytest -q
```

Place the course benchmark at `benchmarks/smartbuilding-pipelines-v2-split/`
or pass its location with `--benchmark`. It is **not included** in the zip.
For the original local workspace, the benchmark is the parent directory of this
folder, so that location is the default. After extracting elsewhere, supply the
explicit path shown below. Keep course data private.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python configure_api.py
```

The last command prompts for a key without echoing it or recording it in shell
history. It writes a mode-0600 `.env` excluded from submission and version control.
Existing `OPENAI_API_KEY` and `OPENAI_BASE_URL` environment variables take precedence.
Do not put credentials in source, logs, reports, or chat. Rotate any exposed key.

## Reproduce the experiment

Set the benchmark location (replace this path with your local download):

```bash
# Original run's location; replace this with your download path on other machines.
export BENCHMARK_DIR="/Users/adityaprakashsahu/Downloads/smartbuilding-pipelines-v2-split"
python -m pytest -q
python prepare_demos.py --benchmark "$BENCHMARK_DIR"
python run_benchmark.py --strategy s1 --model qwen36-27b --cases all --benchmark "$BENCHMARK_DIR"
python run_benchmark.py --strategy s2 --model qwen36-27b --cases all --benchmark "$BENCHMARK_DIR"
python run_benchmark.py --strategy s4 --model qwen36-27b --cases all --benchmark "$BENCHMARK_DIR"
python run_benchmark.py --strategy s5 --model qwen36-27b --cases all --benchmark "$BENCHMARK_DIR"
python summarize.py
python analyze_results.py
python make_report.py --author "ASURITE: Asahu126"
python package_submission.py --asurite Asahu126
```

The original run initially executed the three strategy commands concurrently,
with one in-flight API request per strategy. After s1/s2 finished, disjoint final
s4 case groups used available slots, with at most three total in-flight requests.
Samples for s4 use one `n=5` request. Sequential reproduction is also supported. Retries apply only to HTTP
429/500/502/503/504 and connection/time-out errors, at most six attempts per
invocation, with exponential backoff capped at 60 s. Transport failures without
a completion are retried on resume; program/extraction failures are not.
The first pass used a 600-second API client timeout. After a five-sample request
timed out, remaining/recovery requests used 3,600 seconds to accommodate gateway
queueing. This is separate from the unchanged 120-second generated-code limit.
The current default is `--api-timeout 3600`; use `--api-timeout 600` for the initial
pass setting. New responses record this transport setting; older responses used 600.
There are no execution-feedback repairs, silent syntax retries, or target-ranked
candidate selections. SDK retries are disabled. A case can be selected with
`--cases length1_4,length2_2`.

The fixed holdout is `length1_1,length1_2,length1_3,length2_1,length3_1`.
Three worked examples (`length1_1,length2_1,length3_1`) appear in every s2 prompt;
the other two cases are reserved and unused as examples. All five are excluded
from the **100-case** denominator for all strategies. `--cases all` also runs
the five demo cases as diagnostics; those records have `is_demo=true`.
The split is by case, not by underlying source table, so related cases may share
source data. Do not interpret this as generalization to unseen buildings.

## Prompts and behavioural voting

`prompting.py` reads **only training_0.csv and target.csv**, never test_0.csv.
The same schema/sample block is used for every strategy: row counts, exact column
names, pandas dtypes, null/distinct counts, up to 12 low-cardinality values, first
and last non-null date/time values, and 12 evenly spaced rows across each table.
The first target column is retained. Full local table profiles are cached under
`.cache/`, which is excluded from the zip. Only small samples enter API prompts.

s4 uses the same demonstrations as s2 and executes candidates on **training_0.csv** in isolated processes. Successful
DataFrames are fingerprinted using lexically ordered column names and sorted row
hashes, retaining row relationships and multiplicities. Different row and column
orders therefore vote together. Column names and exact value representations
remain part of the fingerprint. No tolerance clustering is used. Failures,
constraint rejections, and timeouts do not vote. The largest cluster wins;
ties go to its earliest completion index. No valid candidate means failure.
The selected program is then independently applied to test_0.csv for scoring.

## Execution and validation

The runner gives each generated program a source DataFrame, runs it in a fresh
subprocess, and uses a **120-second** wall limit (the Runner section's stricter
limit; the assignment also mentions a 600-second grader limit). It kills the
process group on timeout. AST checks reject I/O, dynamic execution, private
attributes, unsupported imports, and randomness. The macOS sandbox blocks network access, child processes, benchmark CSV reads,
common credential roots and writes outside scratch. Linux applies seccomp plus
a Python file audit guard; its architecture and installed-filter checks fail closed. This coursework-specific gate can
reject otherwise valid pandas idioms and is not a general hostile-code service.

Only the trusted wrapper reads its scratch input and serializes the result.
Output crosses the subprocess boundary as JSON with dtype metadata; no untrusted
pickle is loaded. Python's float representations preserve tiny values rather than
rounding them to zero. Temporal objects, bytes, Decimal values and infinities are
restored before validation. The scratch source CSV uses round-trip float parsing.
Programs returning datetimes should explicitly format them to target strings.

`validators/autopipeline_match.py` is the supplied file unchanged. The supplied
`hard_match.py` has only package-relative import changes. The two helper functions
it needs are extracted **unchanged** from the supplied `utils-1.py`, avoiding unused
PostgreSQL/scikit-learn dependencies. Originals and SHA-256 hashes are retained
in `validators/originals/` and `validators/provenance.json`.

The supplied code is the scoring authority even where the assignment's prose
differs: hard_match deduplicates rows, includes a legacy half-table comparison,
and has distinct numeric/mixed-string handling. Auto-Pipeline drops NaNs from
each column and permits content-based matches at 10% relative numeric tolerance;
it does not establish row-level equivalence or a one-to-one column assignment.
Both raw validator outputs and exact-schema diagnostics are logged. Do not
describe an accuracy gap as solely naming failures without inspecting the cases.

## Fourth strategy: target-constraint reranking (s5)

This is a custom LLM ensemble/selection strategy, not another self-consistency vote.
The fixed pool contains the five original s4 responses and one s2 response. Exact
API responses are reused when available; a cold run issues the same two requests.
No scored program is edited. All six programs execute on **training_0.csv**.
The same target prompt sample supplies the exact schema and, only when uniquely
identified by at least four distinct dates, a date-to-weekday convention. No test
rows, evaluation results, target row counts or case-specific rules enter selection.

Loss is lexicographic: number of schema differences, then the sum of weekday-rule
violation fractions on at most 128 evenly spaced training-output rows. A strict
loss improvement replaces the original s4 winner. Ties preserve the s4 winner;
remaining ties use pool order (s4 indices 0-4, s2 index 5). This is a deliberately
conservative check: no constraint claims that training and target periods align.

`target_constraints.py`, `strategies/s5.py` and their frozen policy hashes are
recorded in `results/s5_policy.json`. The policy was developed after inspecting
baseline failures, then run unchanged across all 105 cases. This is exploratory
method development, not an independent held-out tuning claim. All four strategies
use the same 100-case evaluation denominator and five demonstration exclusions.

s5 logs both original requests and unmodified raw responses, every candidate,
training diagnostics and selected-code provenance. Its **logical standalone cost**
includes both pool requests and all six samples. Its **additional physical API
requests** are zero when reusing the submitted pool. These costs are reported
separately; shared requests must not be counted twice as new provider usage.

## Resume and rescore

Rerun the same command to skip finished cases and reuse cached completions.
Request hashes include endpoint, model, messages and decoding settings. Changed
settings require a new `--output` directory. There is no need to query the API to
re-evaluate already selected programs:

```bash
python run_benchmark.py --strategy s1 --model qwen36-27b --cases all --benchmark "$BENCHMARK_DIR" --rescore
python summarize.py
```

JSONL is append-only; the summarizer uses the last record for each case, avoiding
double-counting rescoring. Cost comes from the original cached response usage,
including retries and all sampled completions, not from the replay API traffic.
`wall_seconds` retains the maximum recorded per-case time across append-only
records; `replay_wall_seconds` records explicit rescore time. When a resumed or
disjoint-group run finds a cached response without a prior case record in its
process snapshot, it reconstructs case time from original API latency plus local
execution. Such duplicate records are not summed. `api_seconds` preserves the
original request latency. `--reselect`
replays cached candidate extraction and voting as well, with no API requests.
Strategies overlap in real elapsed time;
per-strategy times should not be summed as experiment elapsed time. The final
cached s4 audit used disjoint local case groups, with no API calls. Local platform
and locale details are in `results/runtime_environment.json`.
An overnight sleep and a later shared connection drop left three s4 cases with
interrupted requests (`length9_3`, `length14_2`, `length15_4`). One overlapping
resume attempt for length14_2 was also cancelled before receiving a completion.
Their interruption notes and transport errors are retained in the case logs.
Interrupted requests count toward calls, but their active duration and token usage
were unavailable. Time/token totals cover recorded intervals and received usage;
s4 times are lower bounds. Logged calendar waits are diagnostic bounds, not a
complete elapsed-time measurement. Fresh connections recovered only cases without
responses; no received completion was discarded or replaced. Temporary idle-sleep
assertions protected the resumed jobs and were released on exit.

To reproduce the submitted programs, votes and scores from the archived responses
without a key or any API requests, run:

```bash
python run_benchmark.py --strategy s1 --model qwen36-27b --cases all --benchmark "$BENCHMARK_DIR" --reselect
python run_benchmark.py --strategy s2 --model qwen36-27b --cases all --benchmark "$BENCHMARK_DIR" --reselect
python run_benchmark.py --strategy s4 --model qwen36-27b --cases all --benchmark "$BENCHMARK_DIR" --reselect
python run_benchmark.py --strategy s5 --model qwen36-27b --cases all --benchmark "$BENCHMARK_DIR" --reselect
python summarize.py
python analyze_results.py
python review_programs.py
python verify_artifacts.py --benchmark "$BENCHMARK_DIR"
python make_report.py --author "ASURITE: Asahu126"
```

The submitted run was audited this way after adding type-preserving JSON metadata
to the trusted execution wrapper. Prompts and raw API completions were unchanged.

## Artifacts and review

* `results/s*.jsonl`: scores, similarities, usage, configuration and log paths.
* `summary.csv`, `length_summary.csv`, `figures/`: tables and charts from logs.
* `generated/<strategy>/<case>/transform.py`: selected program; `candidates/`
  retains every extracted sample, including nonwinning samples.
  Cases with no valid emitted candidate retain a logged failure and no final program.
* `logs/<strategy>/<case>/`: prompt, complete API response (including any provider
  reasoning field), raw content, candidate execution outcomes, selection and scoring.
* `demos/`: fixed split, three authored programs and actual demonstration messages.
* `analysis.json`: reviewed failure examples and interpretation used by the report.
* `output/pdf/`: report PDF; main text has six pages, prompt appendix follows.

Review generated code and analyses before submitting; you remain responsible for
the work. AI assistance built this harness and report. Generated scored programs
come only from the recorded API calls. No accuracy numbers are invented.
The submission packager refuses incomplete results or missing analysis and excludes
benchmark CSVs, `.env`, virtual environments, caches, and temporary files.
