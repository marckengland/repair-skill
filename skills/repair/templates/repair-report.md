# Repair report template

Use this structure for the final summary. Keep each section short; drop a
section only when it truly doesn't apply, and say "none" rather than omitting
risks.

```markdown
## Fix: <one-line description>

**Symptom:** <what the user saw, with the exact error if any>

**Root cause:** <one or two sentences>

<details><summary>5 Whys</summary>

1. <why 1>, evidence: <file:line / log / output>
2. <why 2>, evidence: <...>
3. ...
Fixed at: why <n>, because <reason>.
</details>

**Change:** <what changed and where, file:line>

**Blast radius checked:**
| Changed | Consumers | At risk? | Verified by |
|---------|-----------|----------|-------------|

**Verification:**
- Repro test: failed before the fix, passes after: `<test name>`
- Baseline: <N> passed / <M> failed before → <N'> passed / <M'> failed after
- New failures: none  (or: list them and explain)
- Pre-existing failures (not touched): <list or "none">
- Commands run: `<test>`, `<lint>`, `<typecheck>`, `<build>`

**Not verified:** <anything you couldn't run or check, or "none">

**Follow-ups:** <deeper root cause not fixed here, sibling bugs found,
suggested guards (test, type, lint rule, CI check)>
```
