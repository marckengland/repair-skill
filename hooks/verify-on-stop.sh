#!/usr/bin/env bash
# Stop hook: before Claude finishes a turn, run the project's verification
# script and send any failure back to Claude so it can't end on a red build.
#
# Opt-in per project: does nothing unless .claude/repair-verify.sh exists.
# Loop-safe: skips when Claude is already continuing because of a stop hook,
# and skips when nothing changed since the last passing run.

set -u

input="$(cat)"
project_dir="${CLAUDE_PROJECT_DIR:-$PWD}"
verify="$project_dir/.claude/repair-verify.sh"

[ -f "$verify" ] || exit 0

# One forced re-check per stop chain. If Claude stops again after being
# blocked, let it: it has seen the failures and must report them.
if printf '%s' "$input" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

session_id="$(printf '%s' "$input" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
state_dir="${TMPDIR:-/tmp}/repair-verify"
mkdir -p "$state_dir" 2>/dev/null
state_file="$state_dir/${session_id:-default}.pass"

# Fingerprint the working tree so an unchanged tree isn't re-verified.
fingerprint=""
if git -C "$project_dir" rev-parse --git-dir >/dev/null 2>&1; then
  fingerprint="$(
    {
      git -C "$project_dir" rev-parse HEAD 2>/dev/null
      git -C "$project_dir" diff HEAD 2>/dev/null
      git -C "$project_dir" ls-files --others --exclude-standard 2>/dev/null
      (cd "$project_dir" && git ls-files -z --others --exclude-standard | xargs -0 cat) 2>/dev/null
    } | cksum
  )"
  if [ -f "$state_file" ] && [ "$(cat "$state_file")" = "$fingerprint" ]; then
    exit 0
  fi
fi

log="$(mktemp)"
trap 'rm -f "$log"' EXIT

if (cd "$project_dir" && bash "$verify") >"$log" 2>&1; then
  [ -n "$fingerprint" ] && printf '%s' "$fingerprint" >"$state_file"
  exit 0
fi

{
  echo "repair: .claude/repair-verify.sh failed. Last 60 lines of output:"
  echo
  tail -n 60 "$log"
  echo
  echo "Compare against your baseline before finishing:"
  echo "- pass -> fail: a regression from this session's changes. Fix it (repair skill, circuit breaker)."
  echo "- already failing before your changes: say so in your report; don't hide it."
} >&2
exit 2
