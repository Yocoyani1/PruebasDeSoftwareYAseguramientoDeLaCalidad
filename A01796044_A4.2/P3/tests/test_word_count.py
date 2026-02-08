#!/usr/bin/env python3
"""Unit tests for wordCount module (P3)."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "source"))

import word_count as wc


class TestSplitIntoWords(unittest.TestCase):
    """Tests for split_into_words."""

    def test_simple(self):
        """Split by spaces."""
        self.assertEqual(
            wc.split_into_words("hello world"),
            ["hello", "world"]
        )

    def test_multiple_spaces(self):
        """Multiple spaces between words."""
        self.assertEqual(
            wc.split_into_words("a   b   c"),
            ["a", "b", "c"]
        )

    def test_newlines(self):
        """Newlines act as separators."""
        self.assertEqual(
            wc.split_into_words("one\ntwo\nthree"),
            ["one", "two", "three"]
        )


class TestCountWords(unittest.TestCase):
    """Tests for count_words."""

    def test_frequency(self):
        """Count frequency (case insensitive)."""
        words = ["hello", "Hello", "world", "hello"]
        freq = wc.count_words(words)
        self.assertEqual(freq["hello"], 3)
        self.assertEqual(freq["world"], 1)


class TestRunWordCount(unittest.TestCase):
    """Integration tests for run_word_count."""

    def test_full_run(self):
        """Run on temp file produces word counts."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write("hello world hello")
            path = f.name
        try:
            text, success = wc.run_word_count(path)
            self.assertTrue(success)
            self.assertIn("hello: 2", text)
            self.assertIn("world: 1", text)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
