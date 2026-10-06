#!/usr/bin/env bash
# Verify this repo: manifests parse, the stop hook behaves, eval fixtures are intact.
set -euo pipefail
cd "$(dirname "$0")/.."

for f in .claude-plugin/plugin.json .claude-plugin/marketplace.json hooks/hooks.json skills/repair/evals/evals.json; do
  python3 -m json.tool "$f" >/dev/null && echo "ok   $f parses"
done
bash tests/test-hook.sh
python3 tests/check-fixtures.py
