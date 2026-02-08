#!/usr/bin/env python3
"""Unit tests for convertNumbers module (P2)."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "source"))

import convertNumbers as cn


class TestToBinary(unittest.TestCase):
    """Tests for to_binary."""

    def test_zero(self):
        """0 -> '0'."""
        self.assertEqual(cn.to_binary(0), "0")

    def test_one(self):
        """1 -> '1'."""
        self.assertEqual(cn.to_binary(1), "1")

    def test_ten(self):
        """10 -> '1010'."""
        self.assertEqual(cn.to_binary(10), "1010")

    def test_float_truncated(self):
        """Float is truncated to int."""
        self.assertEqual(cn.to_binary(5.9), "101")


class TestToHexadecimal(unittest.TestCase):
    """Tests for to_hexadecimal."""

    def test_zero(self):
        """0 -> '0'."""
        self.assertEqual(cn.to_hexadecimal(0), "0")

    def test_ten(self):
        """10 -> 'A'."""
        self.assertEqual(cn.to_hexadecimal(10), "A")

    def test_sixteen(self):
        """16 -> '10'."""
        self.assertEqual(cn.to_hexadecimal(16), "10")

    def test_255(self):
        """255 -> 'FF'."""
        self.assertEqual(cn.to_hexadecimal(255), "FF")


class TestParseNumbers(unittest.TestCase):
    """Tests for parse_numbers in convertNumbers."""

    def test_valid(self):
        """Valid numbers are parsed."""
        lines = ["1", "2", "10"]
        numbers, errors = cn.parse_numbers(lines)
        self.assertEqual(numbers, [1.0, 2.0, 10.0])
        self.assertEqual(errors, [])


class TestRunConversions(unittest.TestCase):
    """Integration tests for run_conversions."""

    def test_full_run(self):
        """Run on temp file produces binary and hex."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write("10\n16\n")
            path = f.name
        try:
            text, success = cn.run_conversions(path)
            self.assertTrue(success)
            self.assertIn("Binary: 1010", text)
            self.assertIn("Hexadecimal: A", text)
            self.assertIn("Hexadecimal: 10", text)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
