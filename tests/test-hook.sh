#!/usr/bin/env bash
# Tests for hooks/verify-on-stop.sh. Run: bash tests/test-hook.sh
set -u

hook="$(cd "$(dirname "$0")/.." && pwd)/hooks/verify-on-stop.sh"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
failures=0

proj="$work/proj"
mkdir -p "$proj/.claude"
git -C "$proj" init -q
echo ok >"$proj/a.txt"
git -C "$proj" add a.txt
git -C "$proj" -c user.name=t -c user.email=t@example.com commit -qm init

run_hook() {
  printf '%s' "$1" | CLAUDE_PROJECT_DIR="$proj" TMPDIR="$work" bash "$hook" >/dev/null 2>&1
  echo $?
}

check() {
  if [ "$2" = "$3" ]; then echo "ok   $1"; else echo "FAIL $1 (expected $3, got $2)"; failures=$((failures + 1)); fi
}

input='{"session_id":"t1","stop_hook_active":false}'

check "no verify script: allows stop" "$(run_hook "$input")" 0

printf 'echo ran >>"%s/count"\ngrep -q ok a.txt\n' "$work" >"$proj/.claude/repair-verify.sh"
check "passing verify: allows stop" "$(run_hook "$input")" 0
check "unchanged tree: allows stop" "$(run_hook "$input")" 0
check "unchanged tree: verify not re-run" "$(wc -l <"$work/count" | tr -d ' ')" 1

echo bad >"$proj/a.txt"
check "failing verify: blocks stop" "$(run_hook "$input")" 2
check "stop_hook_active: allows stop" "$(run_hook '{"session_id":"t1", "stop_hook_active": true}')" 0

echo ok >"$proj/a.txt"
echo note >"$proj/notes.txt"
before="$(wc -l <"$work/count" | tr -d ' ')"
run_hook "$input" >/dev/null
echo changed >"$proj/notes.txt"
run_hook "$input" >/dev/null
check "untracked file edit: verify re-runs" "$(( $(wc -l <"$work/count" | tr -d ' ') - before ))" 2

[ "$failures" -eq 0 ] && echo "all hook tests passed" || { echo "$failures hook test(s) failed"; exit 1; }
