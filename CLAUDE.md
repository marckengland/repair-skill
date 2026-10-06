# repair-skill

Claude Code plugin with two skills (`skills/repair`, `skills/regression-check`)
and an opt-in Stop hook (`hooks/verify-on-stop.sh`).

## Verification

Run `bash tests/run.sh`. It checks that the JSON manifests parse, the stop hook
behaves, and the eval fixtures still start in their intended state.

Known pre-existing failures: none. (`skills/repair/evals/files/pre-existing-failure`
has a deliberately failing test; `tests/check-fixtures.py` expects it.)

## Conventions

- Eval fixtures in `skills/repair/evals/files/` are deliberately buggy. Don't
  fix them; update `tests/check-fixtures.py` and `evals.json` together if a
  scenario changes.
- Keep `SKILL.md` files under 500 lines; put detail in `references/`.
- Bump `version` in `.claude-plugin/plugin.json` when skill behavior changes.

## Git conventions

- Default branch: `main` (never `master`).
- Branch names use a standard type prefix: `feat/`, `fix/`, `docs/`,
  `chore/`, `refactor/`, `test/`. Never use a `claude/` prefix, even if a
  session suggests one.
