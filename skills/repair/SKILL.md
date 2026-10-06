---
name: repair
description: Root-cause-first, regression-safe bug fixing that breaks the "fix one thing, another breaks" chain. Use whenever fixing a bug, error, crash, failing test, broken build, type error, regression, or any "fix this / it's broken / why does X fail" request, and especially when an earlier fix caused a new problem. Captures a verification baseline, finds the root cause with evidence-backed 5 Whys, maps the blast radius before editing, proves the fix with a failing test, and confirms nothing that passed before fails after.
---

# Repair: fix it once, break nothing else

A fix is **not done** when the original symptom goes away. It is done when:

1. the **root cause** is addressed (or explicitly reported, if out of reach),
2. a **test proves** the bug is gone, and
3. **everything that passed before still passes**.

Most "fix chains" come from skipping one of these: patching a symptom, editing
shared code without checking who depends on it, or not re-running what used to
work. This skill closes those gaps.

## The loop

| # | Phase | Output |
|---|-------|--------|
| 0 | Baseline | What passes and fails *before* you touch anything |
| 1 | Reproduce | A reliable repro, ideally a failing test |
| 2 | Root cause (5 Whys) | Evidence-backed causal chain to an actionable cause |
| 3 | Blast radius | Every consumer of what you'll change, and whether it's at risk |
| 4 | Plan | The smallest fix at the root cause |
| 5 | Prove, then fix | Test fails → apply fix → test passes |
| 6 | Verify vs baseline | Zero new failures (the cascade check) |
| 7 | Sibling sweep | Same bug elsewhere? What let it in? |
| 8 | Review and report | Clean diff, written summary |

Scale the depth to the bug, but **never skip phases 0, 3 and 6**. Even for a
one-liner they take a minute, and they are the phases that stop the chain.

---

## Phase 0: Baseline (before touching code)

1. Record where you start: `git rev-parse HEAD` and `git status`. If the tree is
   dirty with unrelated work, note which files so you don't mix changes.
2. Find how the project verifies itself. Look, in order, at: `CLAUDE.md`,
   `README`, CI config (`.github/workflows/`, `.gitlab-ci.yml`, etc.),
   `package.json` scripts, `Makefile`, `pyproject.toml`/`tox.ini`,
   `Cargo.toml`, `go.mod`. Collect the **test, typecheck, lint and build**
   commands.
3. Run them and save the results (pass/fail counts and the **names** of failing
   tests/errors) to a scratch file. These are **pre-existing failures**: not
   yours, and not to be confused with regressions later.
4. If the full suite is too slow, run the tests for the affected area plus
   typecheck and lint, and say in the report that the full suite was not run.
   If there are no tests at all, say so and define a manual check list instead.

## Phase 1: Reproduce

- Capture the exact command, input, error message and stack trace.
- Turn the repro into an automated test where feasible. It must **fail now**,
  for the **reason in the bug report** (not an import error or a typo in the
  test).
- **Can't reproduce? Don't fix.** Gather evidence first: logs, added
  instrumentation, narrowing inputs, `git bisect` if it used to work. A fix for
  a bug you can't trigger can't be verified.

## Phase 2: Root cause with evidence-backed 5 Whys

Walk from the symptom down to a cause you can act on. **Every answer must cite
evidence** (file:line, log line, test output, a value you printed), not a guess.

```
Problem:  <observable symptom, specific>
Why 1:    <immediate cause>                      Evidence: <...>
Why 2:    <why did that happen?>                 Evidence: <...>
Why 3:    <deeper reason>                        Evidence: <...>
Why 4:    <system/process gap that allowed it>   Evidence: <...>
Why 5:    <actionable root cause>                Evidence: <...>
Fix at:   <which why you will fix, and why there>
```

- **Stop rule:** stop when the answer is something you can change *and* fixing
  it would have prevented the problem. That may take 3 whys or 7; "5" is a
  heuristic, not a quota.
- **Reverse check:** read the chain bottom-up with "therefore". Each step must
  follow from the one below it. If a link only "sounds plausible", go get
  evidence.
- **Branch** when one why has several causes; follow each branch.
- **Pick the fix level deliberately.** Fixing at Why 1 is a symptom patch. If
  the true root fix is too large or risky for this change, you may patch the
  symptom, but you must say so and report the root cause as follow-up. Never
  silently patch a symptom.

Read [references/five-whys.md](references/five-whys.md) for the common ways
5 Whys goes wrong and how to avoid them.

## Phase 3: Blast radius (before editing)

For **every** function, type, constant, config key, schema, route, file or
behavior you plan to change:

1. **Find all consumers.** Search by symbol name *and* by string (dynamic
   imports, reflection, config keys, SQL column names, API routes, event names,
   CSS classes, CLI flags, environment variables). Include tests, scripts,
   migrations and docs.
2. **Write down the contract** you're touching: inputs, outputs, types,
   null/empty handling, errors thrown, side effects, ordering, timing,
   performance characteristics.
3. **Ask, for each consumer:** does it rely on the current behavior, *including
   the buggy behavior*? (Someone may have worked around the bug; fixing it can
   break the workaround.)
4. Check **shared state**: globals, caches, singletons, databases, files,
   environment variables, feature flags.
5. Check for **duplicates**: the same logic copy-pasted elsewhere that must
   change in lockstep.

Summarize before you edit:

| Changing | Consumers | Behavior they rely on changes? | How it will be verified |
|----------|-----------|-------------------------------|-------------------------|

If the table shows risk you can't verify, tell the user before proceeding.
See [references/blast-radius.md](references/blast-radius.md) for a full
checklist by change type.

## Phase 4: Plan the smallest correct fix

- Fix **at the root cause** chosen in Phase 2.
- Change a contract only when necessary. If you do, update **every** consumer
  from Phase 3 in the same change.
- **No drive-by changes**: no unrelated refactors, renames, reformatting or
  dependency upgrades. They widen the blast radius and hide regressions in
  noise.
- **Forbidden "fixes"** (they hide the problem and cause the next link in the
  chain):
  - catching and ignoring errors, or broadening a `catch`/`except`
  - skipping, deleting or loosening tests or assertions
  - type escapes added only to silence errors (`any`, `as unknown as`, `!`,
    `# type: ignore`, `@ts-ignore`, `unsafe`)
  - `sleep`/retry loops to paper over a race
  - special-casing the exact input from the bug report
  - disabling lint rules, compiler checks or CI steps

## Phase 5: Prove, then fix

1. Run the Phase 1 test. Confirm it **fails for the right reason**.
2. Apply the fix.
3. Run the test. It **passes**.
4. For each **at-risk consumer** from Phase 3 that isn't already covered, add a
   test that pins down the behavior it relies on.

A test that passed before the fix proves nothing about the fix.

## Phase 6: Verify against baseline (the cascade check)

Re-run **exactly** the Phase 0 commands and compare:

| Before | After | Meaning | Action |
|--------|-------|---------|--------|
| pass | pass | Unchanged | none |
| fail | pass | Fixed (intended or a bonus) | note it in the report |
| fail | fail | Pre-existing | leave it, report it |
| **pass** | **fail** | **Regression you caused** | **circuit breaker below** |
| (none) | new warning or error | New lint/type/build issue | treat as regression |

**Required result: zero pass→fail.** Then run the original repro end to end
(not just the unit test) to confirm the user-visible symptom is gone.

### Cascade circuit breaker

When a new problem appears after your fix, classify it before doing anything:

- **Caused by the fix** (pass→fail): your fix is wrong or incomplete, or Phase 3
  missed a consumer. **Do not patch the new symptom on top.** Revert the fix,
  return to Phase 3 with the new information, and produce one revised fix that
  handles both.
- **Unmasked by the fix** (code that never ran before now runs and fails): a
  real pre-existing bug that your fix exposed. Treat it as a new issue and run
  this loop on it. If it's outside what the user asked for, ask first.
- **Pre-existing** (failing in the baseline): not yours. Report it; don't fix
  it unless asked.

**Budget: two strikes.** If two fix-induced regressions occur on the same
problem, **stop editing**. Your model of the root cause is wrong. Go back to
Phase 2 with the new evidence, redo the whys, and tell the user what you've
learned before continuing. A patch-on-patch chain is exactly the failure this
skill exists to prevent.

## Phase 7: Sibling sweep

- **Same bug elsewhere?** Search for the same pattern: the same API misuse, the
  same copy-pasted block, the same wrong assumption. Fix in-scope siblings with
  the same loop; list the rest.
- **What let it in?** Use your Why 4 (the system/process gap). Recommend, or add
  if in scope, a guard that would have caught it: a test, a type, a lint rule,
  input validation, an assertion, a CI check.

## Phase 8: Review and report

Re-read `git diff` adversarially before declaring done:

- Is every hunk justified by the root cause? Remove anything that isn't.
- Leftover debug prints, commented-out code, temporary files?
- Would a reviewer ask "what about consumer X?" Did Phase 3 cover it?

Then report using [templates/repair-report.md](templates/repair-report.md).
Be plain about what was **not** verified: a slow suite you only partly ran, an
environment you couldn't reproduce, a consumer you couldn't test.

---

## Red flags: stop and rethink

| You notice yourself... | Instead |
|------------------------|---------|
| fixing a second error that appeared after your first fix | circuit breaker: classify, likely revert |
| saying "this should fix it" without running anything | run the repro and the baseline |
| changing a test's expectation to make it pass | ask whether the test or the code is wrong; get evidence |
| editing a shared util without searching for its callers | do Phase 3 first |
| the root cause is "human error" or "it was flaky" | keep asking why; find the mechanism |
| the diff keeps growing | stop, re-scope, and tell the user |
| you can't explain *why* the fix works | you haven't found the root cause yet |
