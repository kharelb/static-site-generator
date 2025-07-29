import unittest

from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title_valid(self):
        markdown = "# This is a title\nSome content here."
        expected_title = "This is a title"
        self.assertEqual(extract_title(markdown), expected_title)

    def test_extract_title_no_title(self):
        markdown = "No title here.\nSome content."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertTrue("No title found in the first line of the markdown" in str(context.exception))

    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertTrue("The markdown content is empty.")