import unittest

from shop.cart import total
from shop.orders import ORDERS
from shop.receipt import render_receipt


class CartTest(unittest.TestCase):
    def test_v1_total(self):
        self.assertEqual(total(ORDERS[1041]), 32.00)

    def test_v1_receipt(self):
        self.assertIn("Mug x1  $12.00", render_receipt(ORDERS[1041]))
