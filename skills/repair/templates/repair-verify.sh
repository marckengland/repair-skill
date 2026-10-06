#!/usr/bin/env bash
# Example .claude/repair-verify.sh
#
# Copy to <project>/.claude/repair-verify.sh and edit the commands. When the
# repair plugin is installed, its Stop hook runs this before Claude finishes a
# turn that changed files, and sends any failure back to Claude.
#
# Keep it fast (well under a minute if you can): it runs often. Put slow
# suites in CI instead.

set -euo pipefail

# Replace with your project's commands:
npm run lint
npm run typecheck
npm test -- --run
