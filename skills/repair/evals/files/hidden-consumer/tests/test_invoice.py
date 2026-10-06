import unittest
from datetime import date

from billing.invoice import render_invoice


class InvoiceTest(unittest.TestCase):
    def test_amount(self):
        self.assertIn("Amount due: $12.50", render_invoice(7, date(2026, 10, 6), 12.5))

    def test_number(self):
        self.assertIn("Invoice #7", render_invoice(7, date(2026, 10, 6), 12.5))
