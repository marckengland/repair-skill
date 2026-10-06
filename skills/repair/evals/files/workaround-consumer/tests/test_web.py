import unittest

from catalog.web import pagination_links


class WebTest(unittest.TestCase):
    def test_exact_multiple(self):
        self.assertEqual(len(pagination_links(20)), 2)

    def test_remainder(self):
        self.assertEqual(len(pagination_links(21)), 3)

    def test_small(self):
        self.assertEqual(len(pagination_links(5)), 1)
