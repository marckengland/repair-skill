# repair skill evals

Each scenario is a small Python project (standard library only) with a bug and
a trap that catches the "fix one thing, break another" pattern:

| Eval | Bug | Trap |
|------|-----|------|
| `hidden-consumer` | Invoice dates should be ISO | `format_date` is shared with a bank export that must stay MM/DD/YYYY |
| `symptom-trap` | Cart total too low for order 1042 | Root cause is a v1/v2 field mismatch that also breaks receipts; patching `total()` only hides it |
| `pre-existing-failure` | `slugify` emits double dashes | An unrelated test already fails; it must be reported, not "fixed" or blamed on the change |
| `workaround-consumer` | `page_count` overshoots on exact multiples | `web.py` compensates for the bug; fixing it without removing the workaround breaks the web pages |

Run the fixture tests with `python3 -m unittest discover -s tests -t .` from a
fixture folder.

## Running the evals

With the `skill-creator` skill in Claude Code, ask:

> Run the evals in skills/repair/evals/evals.json for the repair skill, with and
> without the skill, and show me the benchmark.

Copy each fixture to a scratch directory before a run so the originals stay
untouched. `tests/check-fixtures.py` at the repo root confirms the fixtures
still start in their intended state.

## Results so far

**Iteration 1 (2026-10-06):** each scenario ran once with the skill and once
without.

- **Fixes:** all 8 runs fixed the bug and avoided the trap. The scenarios are
  too easy: comments and docstrings point straight at the hidden consumer, so
  even a run without the skill finds it.
- **Reports:** runs with the skill gave before/after test counts,
  blast-radius tables and a "not verified" section. Runs without the skill
  usually left these out.
- **Behavior and scope:** runs with the skill kept existing behavior where
  the request didn't ask to change it, for example `page_count(0)` stays 1.
  They listed nearby bugs as follow-ups instead of fixing them unasked.
- **Cost:** about 25% more tokens and roughly twice the time.

**Next:** harder scenarios. Hide consumers behind dynamic lookups with no
hinting comments, use larger codebases, and add a case where the first
plausible fix causes a second failure, to exercise the circuit breaker.
