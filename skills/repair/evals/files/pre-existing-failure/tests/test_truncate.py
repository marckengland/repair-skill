import unittest

from textutils.truncate import truncate


class TruncateTest(unittest.TestCase):
    def test_short_unchanged(self):
        self.assertEqual(truncate("hi", 10), "hi")

    def test_respects_width(self):
        self.assertLessEqual(len(truncate("abcdefghijkl", 8)), 8)
