import unittest

from catalog.api import list_items_response


class ApiTest(unittest.TestCase):
    def test_count(self):
        self.assertEqual(list_items_response(list(range(7)))["count"], 7)
