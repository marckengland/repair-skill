import unittest
from datetime import date

from billing.bank_export import export_payments


class BankExportTest(unittest.TestCase):
    def test_bank_requires_us_dates(self):
        out = export_payments([{"date": date(2026, 10, 6), "payee": "ACME", "amount": 99}])
        self.assertEqual(out.splitlines()[1], "10/06/2026,ACME,99.00")
