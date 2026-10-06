# repair-skill

A [Claude Code](https://claude.com/claude-code) skill for **root-cause-first,
regression-safe bug fixing**. It exists to stop the chain where fixing one
problem creates another, fixing that creates a third, and so on.

## What it does

When Claude fixes a bug with this skill, it:

1. **Takes a baseline:** runs the project's tests, typecheck, lint and build
   *before* changing anything, so pre-existing failures are never mistaken for
   new ones.
2. **Reproduces** the bug, ideally as a failing test.
3. **Finds the root cause** with evidence-backed **5 Whys**, avoiding the usual
   misuses (guessing, stopping at a symptom, blaming "flakiness").
4. **Maps the blast radius:** finds every caller and consumer of what it will
   change, including code that depends on the buggy behavior.
5. **Makes the smallest fix at the root cause**, with no symptom-hiding tricks
   (swallowed errors, skipped tests, type escapes, sleeps).
6. **Proves it:** the test fails before the fix and passes after.
7. **Runs the cascade check:** re-runs the baseline and requires zero
   pass→fail changes.
8. **Trips a circuit breaker** if the fix causes new failures: classify, revert
   instead of patching on top, and after two strikes go back to root-cause
   analysis and tell you what it learned.
9. **Sweeps for siblings** (the same bug elsewhere) and suggests a guard that
   would have caught it.
10. **Reports** root cause, change, blast radius, verification and anything it
    could not verify.

## Install

### As a plugin (recommended)

In Claude Code:

```
/plugin marketplace add marckengland/repair-skill
/plugin install repair@repair-skill
```

### As a plain skill

Copy the skill folder into your personal or project skills directory:

```bash
# all projects
cp -r skills/repair ~/.claude/skills/

# one project (commit it so your team gets it too)
cp -r skills/repair /path/to/project/.claude/skills/
```

## Use

Claude loads the skill automatically when you ask it to fix a bug, error,
failing test, broken build or regression. You can also invoke it directly:

```
/repair the checkout page returns 500 when a discount is removed
```

(When installed as a plugin, the commands are namespaced: `/repair:repair`
and `/repair:regression-check`.)

### `regression-check`: the before/after comparison on its own

For any change, not only bug fixes (features, refactors, dependency upgrades,
merges):

```
/regression-check
```

Claude runs your checks on the base revision (in a separate git worktree, so
your working tree is untouched) and on your current changes, then reports
anything that went from passing to failing, tests that disappeared, and new
warnings.

### Stop hook: checks run before Claude says "done"

A skill is guidance; a hook is enforced. The plugin ships an **opt-in** Stop
hook. To turn it on for a project, add an executable
`.claude/repair-verify.sh` that runs your fast checks (see
[the example](skills/repair/templates/repair-verify.sh)):

```bash
#!/usr/bin/env bash
set -euo pipefail
npm run lint
npm test -- --run
```

Then, whenever Claude tries to finish a turn after changing files, the hook
runs the script. If it fails, Claude gets the output and has to deal with it:
fix a regression, or say plainly that the failure was already there.

The hook:
- does nothing in projects without `.claude/repair-verify.sh`;
- skips re-running when nothing changed since the last passing run;
- blocks at most once per stop, so it can't trap Claude in a loop.

Not using the plugin? Copy `hooks/verify-on-stop.sh` to your project at
`.claude/hooks/verify-on-stop.sh`, make it executable, and
register it in `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify-on-stop.sh", "timeout": 600 }] }
    ]
  }
}
```

## Layout

```
skills/
├── repair/
│   ├── SKILL.md                      # the workflow Claude follows
│   ├── references/
│   │   ├── five-whys.md              # 5 Whys done right, common mistakes, example
│   │   └── blast-radius.md           # consumer-finding checklist by change type
│   ├── templates/
│   │   ├── repair-report.md          # final report structure
│   │   ├── claude-md-verification.md # Verification section for your CLAUDE.md
│   │   └── repair-verify.sh          # example script for the stop hook
│   └── evals/                        # test scenarios for the skill itself
└── regression-check/
    └── SKILL.md                      # before/after comparison for any change
hooks/                                # opt-in Stop hook
tests/                                # tests for this repo (bash tests/run.sh)
.claude-plugin/                       # plugin + marketplace manifests
```

## Get the most out of it

- **Add a `## Verification` section to each project's `CLAUDE.md`** listing
  test, lint, typecheck and build commands, plus any known failing tests.
  The baseline step reads it first. Template:
  [claude-md-verification.md](skills/repair/templates/claude-md-verification.md).
  If it's missing, the skill offers to write one after a fix.
- **Turn on the stop hook** in projects where you want the checks enforced,
  not just requested.
- **Keep a fast test subset** for baselines on large projects, and note the
  full-suite command for the final check.
- **Pair it with CI.** The skill verifies locally; CI catches what your local
  environment can't reproduce.

## Testing the skill

`skills/repair/evals/` has four scenarios, each a small project with a bug
whose obvious fix breaks something else (a shared formatter, a symptom patch,
a pre-existing failure, a workaround that depends on the bug). See
[the evals README](skills/repair/evals/README.md) for how to run them with
and without the skill and compare.

To check this repo itself: `bash tests/run.sh`.

## License

[MIT](LICENSE)
