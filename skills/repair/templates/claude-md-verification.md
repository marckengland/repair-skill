# CLAUDE.md verification section template

Paste this into a project's `CLAUDE.md` and fill in the commands. The `repair`
and `regression-check` skills read it first when taking a baseline, so they
don't have to guess from CI config or package scripts.

```markdown
## Verification

Run these to check a change. All must pass before a fix is done.

- Tests (fast, for baselines): `npm test -- --run`
- Tests (full, before PR): `npm run test:all`
- Typecheck: `npm run typecheck`
- Lint: `npm run lint`
- Build: `npm run build`

Known pre-existing failures (not regressions):
- `tests/legacy/report.test.ts` (tracked in #123)

Notes:
- Integration tests need `docker compose up -d db` first.
- Snapshot tests: update only with `npm test -- -u` after confirming the
  change is intended.
```

Keep the "known pre-existing failures" list current. It is what lets a
baseline tell "already broken" apart from "you just broke it".
