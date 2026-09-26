#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ "${1:-}" == "--help" ]]; then
  cat <<'EOF'
DXN1-bench quick start
  ./start.sh                 Show setup and run instructions
  ./start.sh run             Run all 200 questions (requires DXN1_API_KEY)
  ./start.sh run --limit 3   Smoke-test a few questions
  ./start.sh score results/run.json

Set DXN1_API_KEY and DXN1_BASE_URL for an OpenAI-compatible endpoint.
The runner submits no tool definitions; disable tools/browsing in your provider UI too.
EOF
  exit 0
fi
if [[ "${1:-}" == "run" ]]; then shift; python3 -m dxn1bench.cli run "$@"; exit; fi
if [[ "${1:-}" == "score" ]]; then shift; python3 -m dxn1bench.cli score "$@"; exit; fi
python3 -m dxn1bench.cli questions
cat <<'EOF'

To run the benchmark, configure DXN1_API_KEY, then:
  ./start.sh run --model MODEL_NAME --base-url https://your-endpoint/v1
Then score the saved responses:
  ./start.sh score results/run.json
EOF
