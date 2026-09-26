#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || true)"
if [[ -n "$SCRIPT_DIR" && -f "$SCRIPT_DIR/dxn1bench/cli.py" ]]; then
  cd "$SCRIPT_DIR"
else
  command -v curl >/dev/null || { echo 'curl is required' >&2; exit 1; }
  command -v tar >/dev/null || { echo 'tar is required' >&2; exit 1; }
  DXN1_DIR="${DXN1_BENCH_HOME:-$PWD/.dxn1-bench}"
  mkdir -p "$DXN1_DIR"
  if [[ ! -f "$DXN1_DIR/dxn1bench/cli.py" ]]; then
    curl -fsSL 'https://github.com/dxn111/DXN1-bench/archive/refs/heads/main.tar.gz' | tar -xz --strip-components=1 -C "$DXN1_DIR"
  fi
  cd "$DXN1_DIR"
fi

if [[ "${1:-}" == '--help' || "${1:-}" == '-h' ]]; then
  cat <<'EOF'
DXN1-bench (Python 3.10+, curl, tar; Kilo anonymous free tier; no API key)
  ./start.sh questions
  ./start.sh prepare                  Create the AI respondent answer file
  ./start.sh verify                   Kilo verifies questions using web search
  ./start.sh rate results/run.json    Kilo rates answers and writes category scores
  ./start.sh handoff                  Print AI operator instructions
  ./start.sh all                      Verify, then prepare; AI must answer before rating

AI handoff from any folder:
  curl -fsSL https://raw.githubusercontent.com/dxn111/DXN1-bench/main/start.sh | bash -s -- handoff

The respondent answers without web/tools. Kilo is only the question verifier and rubric rater.
EOF
  exit 0
fi
case "${1:-}" in
  questions) python3 -m dxn1bench.cli questions ;;
  prepare) shift; python3 -m dxn1bench.cli prepare "$@" ;;
  verify) shift; python3 -m dxn1bench.cli verify "$@" ;;
  rate) shift; python3 -m dxn1bench.cli rate "$@" ;;
  handoff) cat AI_RUN.md ;;
  all) python3 -m dxn1bench.cli verify; python3 -m dxn1bench.cli prepare; cat AI_RUN.md ;;
  *)
    python3 -m dxn1bench.cli questions
    cat <<'EOF'

AI operator flow:
  ./start.sh verify
  ./start.sh prepare
  # AI answers every question itself, without tools, and fills results/run.json
  ./start.sh rate results/run.json
EOF
    ;;
esac
