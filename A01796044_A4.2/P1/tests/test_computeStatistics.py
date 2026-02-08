#!/usr/bin/env python3
"""Unit tests for computeStatistics module (P1)."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "source"))

import computeStatistics as cs


class TestParseNumbers(unittest.TestCase):
    """Tests for parse_numbers."""

    def test_valid_numbers(self):
        """Parse only valid numbers."""
        lines = ["1", "2", "3.5", "10"]
        numbers, errors = cs.parse_numbers(lines)
        self.assertEqual(numbers, [1.0, 2.0, 3.5, 10.0])
        self.assertEqual(errors, [])

    def test_invalid_data(self):
        """Invalid lines produce errors and are skipped."""
        lines = ["1", "abc", "2", "3.5"]
        numbers, errors = cs.parse_numbers(lines)
        self.assertEqual(numbers, [1.0, 2.0, 3.5])
        self.assertEqual(len(errors), 1)
        self.assertIn("line 2", errors[0])
        self.assertIn("abc", errors[0])

    def test_empty_lines_ignored(self):
        """Empty lines are ignored."""
        lines = ["1", "", "2", "   ", "3"]
        numbers, _ = cs.parse_numbers(lines)
        self.assertEqual(numbers, [1.0, 2.0, 3.0])


class TestComputeMean(unittest.TestCase):
    """Tests for compute_mean."""

    def test_basic(self):
        """Mean of 10, 20, 30, 40, 50 is 30."""
        self.assertEqual(cs.compute_mean([10, 20, 30, 40, 50]), 30.0)

    def test_single(self):
        """Mean of one number is that number."""
        self.assertEqual(cs.compute_mean([7]), 7.0)

    def test_empty(self):
        """Empty list returns None."""
        self.assertIsNone(cs.compute_mean([]))


class TestComputeMedian(unittest.TestCase):
    """Tests for compute_median."""

    def test_odd_count(self):
        """Median of 1,3,5,7,9 is 5."""
        self.assertEqual(cs.compute_median([1, 3, 5, 7, 9]), 5.0)

    def test_even_count(self):
        """Median of 1,2,3,4 is 2.5."""
        self.assertEqual(cs.compute_median([1, 2, 3, 4]), 2.5)

    def test_empty(self):
        """Empty list returns None."""
        self.assertIsNone(cs.compute_median([]))


class TestComputeMode(unittest.TestCase):
    """Tests for compute_mode."""

    def test_single_mode(self):
        """Mode of 1,2,2,3 is 2."""
        self.assertEqual(cs.compute_mode([1, 2, 2, 3]), 2.0)

    def test_multiple_modes(self):
        """Multiple modes return list (smallest first)."""
        result = cs.compute_mode([1, 1, 2, 2])
        self.assertIsInstance(result, list)
        self.assertEqual(sorted(result), [1.0, 2.0])


class TestVarianceAndStdDev(unittest.TestCase):
    """Tests for variance and standard deviation (poblacional)."""

    def test_variance_zero_spread(self):
        """Variance of [5,5,5] is 0."""
        mean_val = cs.compute_mean([5, 5, 5])
        var = cs.compute_variance([5, 5, 5], mean_val)
        self.assertEqual(var, 0.0)

    def test_std_dev_zero(self):
        """Std dev of 0 variance is 0."""
        self.assertEqual(cs.compute_std_dev(0), 0.0)


class TestRunStatistics(unittest.TestCase):
    """Integration tests for run_statistics."""

    def test_full_run(self):
        """Run on temp file produces correct stats."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write("10\n20\n30\n40\n50\n")
            path = f.name
        try:
            text, success = cs.run_statistics(path)
            self.assertTrue(success)
            self.assertIn("Media: 30.0", text)
            self.assertIn("Mediana: 30.0", text)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
