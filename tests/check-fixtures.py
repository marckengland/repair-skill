"""Check that each eval fixture still has its intended starting state:
the baseline test result and a reproducible bug. Run: python3 tests/check-fixtures.py"""
import subprocess
import sys
from pathlib import Path

FILES = Path(__file__).resolve().parent.parent / "skills/repair/evals/files"

# fixture -> (baseline tests should pass?, python snippet that must print the bug)
FIXTURES = {
    "hidden-consumer": (
        True,
        "from datetime import date\nfrom billing.invoice import render_invoice\n"
        "print('Date: 10/06/2026' in render_invoice(1, date(2026, 10, 6), 1))",
    ),
    "symptom-trap": (
        True,
        "from shop.cart import total\nfrom shop.orders import ORDERS\n"
        "print(total(ORDERS[1042]) == 20.0)",
    ),
    "pre-existing-failure": (
        False,
        "from textutils.slug import slugify\nprint(slugify('Hello  World!') == 'hello--world')",
    ),
    "workaround-consumer": (
        True,
        "from catalog.api import list_items_response\n"
        "print(list_items_response(list(range(20)))['pages'] == 3)",
    ),
}

failures = 0
for name, (should_pass, bug) in FIXTURES.items():
    cwd = FILES / name
    env = {"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"}
    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
        cwd=cwd, capture_output=True, text=True, env=env,
    )
    repro = subprocess.run(
        [sys.executable, "-c", bug], cwd=cwd, capture_output=True, text=True, env=env
    )
    ok = (tests.returncode == 0) == should_pass and repro.stdout.strip() == "True"
    print(("ok   " if ok else "FAIL ") + name)
    failures += not ok

print("all fixtures as intended" if not failures else f"{failures} fixture(s) changed")
sys.exit(1 if failures else 0)
