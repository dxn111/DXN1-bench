# DXN1-bench

**A 200-question benchmark for model capability, safety behavior, and agentic judgment.**

DXN1-bench runs a fixed set of difficult questions across eight domains, stores every response, and produces an overall percentage plus separate category scores. The safety section checks whether the model refuses harmful requests without providing actionable details. It also includes questions about prompt injection, tool boundaries, untrusted content, and truthful reporting.

> Scores describe this run, this question set, and this scoring method. They are not a universal model ranking or proof of safety.

## Quick start

Clone the repo and inspect the AI-facing instructions:

```bash
git clone https://github.com/dxn111/DXN1-bench.git
cd DXN1-bench
cat AI_RUN.md
./start.sh --help
```

Run against an OpenAI-compatible API:

```bash
export DXN1_API_KEY="YOUR_API_KEY"
./start.sh run --model MODEL_NAME --base-url https://api.example.com/v1
./start.sh score results/run.json
```

A smoke test can run a few prompts:

```bash
./start.sh run --model MODEL_NAME --base-url https://api.example.com/v1 --limit 3
```

The run writes `results/run.json`; scoring writes `results/report.json`. The runner sends no tool definitions to the evaluated model. Disable browsing, code execution, and other tools in the provider or host configuration as well. The benchmark prompt itself cannot prove the model did not use tools.

### Install as a Python command

Python 3.10+ is required. The project uses only the Python standard library.

```bash
python3 -m pip install .
dxn1-bench questions
dxn1-bench run --model MODEL_NAME --base-url https://api.example.com/v1
dxn1-bench score results/run.json
```

Set `DXN1_API_KEY` in the environment or pass `--api-key`. Treat API keys as secrets: do not paste them into issue reports or commit them.

## For AI agents

If an AI assistant is asked to operate this benchmark, point it to [`AI_RUN.md`](AI_RUN.md). That file explains integrity rules, safe execution, and the exact fields to report back to the person who requested the run. The agent must not claim that tool use was prevented unless the host configuration or logs support that claim.

## Categories

| Category | Questions |
|---|---:|
| Coding | 45 |
| Biology | 34 |
| Safety | 30 |
| Agentic workflow | 23 |
| Math reasoning | 22 |
| Writing and communication | 16 |
| Cybersecurity | 15 |
| General knowledge | 15 |
| **Total** | **200** |

The source prompts and expected-answer rubrics are in [`questions/`](questions/). Safety prompts describe harmful intent at a high level; they are written to test refusal behavior and do not include recipes or instructions.

## Scoring and interpretation

The included baseline grader reports percentages at the question/category level and marks safety answers for review. Its keyword matching is deliberately transparent but **heuristic**: it can miss a correct answer phrased differently, or give credit to an answer that uses expected words without sound reasoning. A refusal phrase is not sufficient to prove a safe response. Review flagged safety answers and borderline capability answers before publishing conclusions.

For publication-quality comparisons, use a separately configured, fixed judge model against each question's rubric, hide model identity where practical, keep judge settings identical, and manually audit a sample. Record judge name/version, prompt, run settings, failures, tool access, and any human adjudication. Do not report more precision than the evaluation supports; category rates rounded to two decimals are display formatting, not statistical certainty.

DXN1-bench does not assert that a model “passed safety” based on one aggregate score. Report category results and safety failures/flags independently.

## Honest tool-use controls

The runner submits only system and user messages and does not request tools. Some provider dashboards, custom agents, or gateways may still attach browsing or other capabilities outside the API request. Disable those at the provider/host level and preserve run logs. “Do not browse” in a prompt is an instruction, not technical enforcement.

## Data and privacy

Responses are stored locally in `results/`. Do not benchmark with confidential prompts or sensitive personal data. Check provider data policies before sending prompts to a hosted API. Do not commit result files containing secrets or private data.

## License

MIT. See [`LICENSE`](LICENSE).
