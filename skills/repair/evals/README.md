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
