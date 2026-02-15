#!/usr/bin/env python3
# pylint: disable=invalid-name,wrong-import-position
"""Unit tests for computeSales module."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "source"))

import computeSales as cs  # noqa: E402


class TestLoadJsonFile(unittest.TestCase):
    """Tests for load_json_file."""

    def test_valid_json(self):
        """Load valid JSON returns data and None error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump([{"title": "A", "price": 10}], f)
            path = f.name
        try:
            data, err = cs.load_json_file(path)
            self.assertIsNone(err)
            self.assertEqual(data, [{"title": "A", "price": 10}])
        finally:
            os.unlink(path)

    def test_file_not_found(self):
        """Non-existent file returns error."""
        _, err = cs.load_json_file("/nonexistent/path.json")
        self.assertIsNotNone(err)
        self.assertIn("not found", err)

    def test_invalid_json(self):
        """Invalid JSON returns error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{ invalid json }")
            path = f.name
        try:
            _, err = cs.load_json_file(path)
            self.assertIsNotNone(err)
            self.assertIn("Invalid JSON", err)
        finally:
            os.unlink(path)


class TestBuildPriceMap(unittest.TestCase):
    """Tests for build_price_map."""

    def test_valid_catalogue(self):
        """Build price map from valid catalogue."""
        catalogue = [
            {"title": "Product A", "price": 10.5},
            {"title": "Product B", "price": 25.0},
        ]
        price_map, errors = cs.build_price_map(catalogue)
        self.assertEqual(errors, [])
        self.assertEqual(price_map["Product A"], 10.5)
        self.assertEqual(price_map["Product B"], 25.0)

    def test_invalid_catalogue_not_list(self):
        """Catalogue must be a list."""
        _, errors = cs.build_price_map({"title": "A", "price": 10})
        self.assertNotEqual(errors, [])
        self.assertIn("JSON array", errors[0])

    def test_catalogue_invalid_entry_skipped(self):
        """Invalid entries are reported but valid ones added."""
        catalogue = [
            {"title": "Product A", "price": 10},
            {"title": "", "price": 5},
            {"title": "Product B", "price": 25},
        ]
        price_map, errors = cs.build_price_map(catalogue)
        self.assertEqual(len(errors), 1)
        self.assertIn("Product A", price_map)
        self.assertIn("Product B", price_map)


class TestComputeSaleTotal(unittest.TestCase):
    """Tests for compute_sale_total."""

    def test_valid_sale(self):
        """Compute total for valid sale."""
        price_map = {"Product A": 10.0, "Product B": 25.0}
        sale = {
            "Sale": "Sale 1",
            "Products": [
                {"title": "Product A", "quantity": 2},
                {"title": "Product B", "quantity": 1},
            ],
        }
        total, errors = cs.compute_sale_total(sale, price_map, 0)
        self.assertEqual(errors, [])
        self.assertEqual(total, 45.0)

    def test_missing_products(self):
        """Sale without Products returns error."""
        total, errors = cs.compute_sale_total({"Sale": "S1"}, {}, 0)
        self.assertNotEqual(errors, [])
        self.assertEqual(total, 0.0)


class TestRunComputeSales(unittest.TestCase):
    """Integration tests for run_compute_sales."""

    def test_full_run_valid_data(self):
        """Full run with valid catalogue and sales produces correct output."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as cat_file:
            json.dump(
                [
                    {"title": "Product A", "price": 10.50},
                    {"title": "Product B", "price": 25.00},
                ],
                cat_file,
            )
            cat_path = cat_file.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as sales_file:
            json.dump(
                [
                    {
                        "Sale": "Sale 001",
                        "Products": [
                            {"title": "Product A", "quantity": 2},
                            {"title": "Product B", "quantity": 1},
                        ],
                    },
                ],
                sales_file,
            )
            sales_path = sales_file.name

        try:
            text, success = cs.run_compute_sales(cat_path, sales_path)
            self.assertTrue(success)
            self.assertIn("Grand total: $46.00", text)
            self.assertIn("Sale 001", text)
            self.assertIn("$46.00", text)
        finally:
            os.unlink(cat_path)
            os.unlink(sales_path)


if __name__ == "__main__":
    unittest.main()
