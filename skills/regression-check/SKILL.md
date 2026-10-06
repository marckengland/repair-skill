---
name: regression-check
description: Compare the project's tests, typecheck, lint and build before and after a change and report anything that went from passing to failing. Use after any non-trivial change (a feature, refactor, dependency upgrade, merge, or bug fix) and before committing or opening a PR, or whenever the user asks "did I break anything?", "check for regressions", or "is it safe to merge?". Also use when the user wants a before/after comparison of test results.
---

# Regression check: did this change break anything?

The question is never "do the tests pass?" but "does anything fail **now** that
**passed before**?" A suite that was already red still hides real regressions,
and a suite that is green now may have lost tests. So compare, don't just run.

## 1. Find the verification commands

Look, in order, at: a `## Verification` section in `CLAUDE.md`, CI config
(`.github/workflows/` and similar), `package.json` scripts, `Makefile`,
`pyproject.toml`/`tox.ini`, `Cargo.toml`, `go.mod`, and `README`. Collect the
test, typecheck, lint and build commands. If the project has
`.claude/repair-verify.sh`, it is the project's own definition of "verified":
use it.

## 2. Get the "before" results

Pick the first option that applies:

1. **A baseline was already captured in this session** (for example by the
   `repair` skill's Phase 0) and nothing outside your change has moved since.
   Use it.
2. **Run the checks on the base revision in a separate worktree.** This never
   touches the user's working tree.
   - Base is `HEAD` for uncommitted changes, or
     `git merge-base HEAD <default-branch>` for a branch.
   - `git worktree add <scratch-dir>/regression-base <base>`
   - Install dependencies there the way the project normally does (lockfile
     install). If that is too slow or needs secrets, use option 3 instead.
   - Run the commands there, save results, then
     `git worktree remove <scratch-dir>/regression-base`.
3. **Stash as a last resort**, only when the change is entirely uncommitted:
   - `git stash push --include-untracked -m regression-check`
   - Run the commands and save results.
   - `git stash pop`, then confirm with `git status` and `git stash list` that
     the user's changes are back exactly as they were. If the pop conflicts
     (for example the checks generated files), stop and tell the user; never
     drop the stash.

Record per command: exit code, pass/fail counts and the **names** of failing
tests, errors and warnings.

## 3. Get the "after" results

Run exactly the same commands, the same way, on the current tree.

## 4. Compare

| Before | After | Meaning |
|--------|-------|---------|
| pass | pass | unchanged |
| fail | pass | fixed |
| fail | fail | pre-existing (not caused by this change) |
| **pass** | **fail** | **regression** |
| present | missing | **test disappeared**: deleted, renamed, skipped, or no longer collected |
| (none) | new warning/error | **new lint/type/build issue** |

Compare by test and error **names**, not just totals: "3 failed before, 3
failed after" can hide one fixed and one newly broken. Also compare test
**counts**: fewer tests collected after the change is a red flag.

Flaky tests: if a test flips without a plausible link to the change, re-run it
once on both sides. If it still differs, treat it as a regression. Don't
dismiss a failure as "flaky" without that evidence.

## 5. Explain each regression

For every regression, find the change that caused it: read the failure, look
at `git diff <base>` for the code it touches, and narrow by file if needed.
Then hand each one to the `repair` skill (or fix it with the same discipline:
root cause, blast radius, test, re-verify). Don't stack quick patches.

## 6. Report

```markdown
## Regression check: <base> → <current>

Commands: `<test>`, `<lint>`, `<typecheck>`, `<build>`
Baseline from: <session baseline | worktree at <sha> | stash>

| Check | Before | After |
|-------|--------|-------|
| tests | 210 pass / 2 fail | 211 pass / 2 fail |
| lint  | 0 errors | 0 errors |

**Regressions:** none  (or: list with cause and file:line)
**Fixed:** <list or none>
**Pre-existing failures:** <list or none>
**Disappeared tests / new warnings:** <list or none>
**Not run:** <anything skipped, and why>
```

If the project has no verification commands written down, offer to add a
`## Verification` section to `CLAUDE.md` listing what you found, so the next
check is faster and more reliable.
