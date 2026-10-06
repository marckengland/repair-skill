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

(When installed as a plugin, the command is `/repair:repair`.)

## Layout

```
skills/repair/
├── SKILL.md                      # the workflow Claude follows
├── references/
│   ├── five-whys.md              # 5 Whys done right, common mistakes, example
│   └── blast-radius.md           # consumer-finding checklist by change type
└── templates/
    └── repair-report.md          # final report structure
.claude-plugin/                   # plugin + marketplace manifests
```

## Get the most out of it

- **List your verification commands in `CLAUDE.md`** (test, lint, typecheck,
  build). The baseline step finds them faster and more reliably.
- **Keep a fast test subset** for the baseline on large projects, and note the
  full-suite command for the final check.
- **Pair it with CI.** The skill verifies locally; CI catches what your local
  environment can't reproduce.
