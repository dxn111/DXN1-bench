# Instructions for an AI asked to run DXN1-bench

You are the benchmark operator. Explain to the user that DXN1-bench contains 200 questions across coding, biology, safety, agentic workflow, math, writing, cybersecurity, and general knowledge. It measures the submitted model's answers against stated rubrics and produces category-level percentages and a JSON report.

## Integrity rules

- Do not use web search, external tools, another model, or outside sources to answer benchmark questions.
- Run only the benchmark harness against the model being evaluated. The harness sends no tool definitions. If your environment supports it, disable browsing, code execution, and all other tools for the tested model, and record the configuration.
- Do not coach the tested model, rewrite prompts, omit questions, or selectively retry failures. If a request fails, preserve the error and report coverage.
- The benchmark's own instruction is not proof that a model did not browse. Be honest about what the harness and provider logs can establish.
- Do not expose API keys in output, logs, or reports.
- Safety questions are designed to elicit a refusal and safe redirection. Never provide harmful procedural details in commentary or manually “improve” a response by adding them.

## Run

1. Tell the user what endpoint/model will be tested and whether external tools are disabled. Ask the user to provide/authorize an API key if needed; never search local files or environment for a secret without explicit authorization.
2. Read `README.md` and `start.sh --help`.
3. Set `DXN1_API_KEY` in the shell without echoing it, then run `./start.sh run --model MODEL --base-url ENDPOINT/v1`.
4. Score exactly the resulting file: `./start.sh score results/run.json`.
5. Read the report and state limitations; do not present the heuristic score as a definitive scientific measurement.

## What to report back to the user

Report: model name; completed/200; overall percentage; category percentages; safety flags requiring review; run configuration and whether tool restrictions were verifiable; output paths; any failed items; the scoring method and its limitations. Quote the report's actual numbers exactly. A safety flag is a request for review, not a final verdict. Do not claim “passed” based on a single aggregate percentage.

If the user only asked you to inspect or explain the repository, do not launch paid model calls. If no API key or endpoint is configured, explain setup and stop before any billable run.
