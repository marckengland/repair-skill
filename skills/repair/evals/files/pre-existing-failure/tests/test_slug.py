import unittest

from textutils.slug import slugify


class SlugTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_punctuation(self):
        self.assertEqual(slugify("What's new?"), "whats-new")
