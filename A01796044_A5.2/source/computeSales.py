#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Compute total cost for all sales using a price catalogue.
Reads price catalogue JSON and sales record JSON, outputs human-readable
results to screen and SalesResults.txt. Handles invalid data gracefully.
"""

import json
import os
import sys
import time


def load_json_file(filepath):
    """
    Load JSON from file. Returns (data, error_message).
    On success: (data, None). On failure: (None, error_msg).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data, None
    except FileNotFoundError:
        return None, f"Error: File not found: {filepath}"
    except json.JSONDecodeError as e:
        return None, f"Error: Invalid JSON in {filepath}: {e}"
    except OSError as e:
        return None, f"Error reading {filepath}: {e}"


def build_price_map(catalogue_data):
    """
    Build mapping of product title -> price from catalogue.
    Handles invalid entries; returns (dict, list_of_errors).
    """
    price_map = {}
    errors = []

    if not isinstance(catalogue_data, list):
        errors.append("Price catalogue must be a JSON array.")
        return price_map, errors

    for idx, item in enumerate(catalogue_data):
        if not isinstance(item, dict):
            errors.append(f"Catalog entry {idx + 1}: expected object, got {type(item).__name__}")
            continue

        title = item.get("title") or item.get("name") or item.get("product")
        price = item.get("price")

        if title is None or title == "":
            errors.append(f"Catalog entry {idx + 1}: missing product title/name")
            continue

        if price is None:
            errors.append(f"Catalog entry {idx + 1} ({title}): missing price")
            continue

        try:
            price_val = float(price)
        except (TypeError, ValueError):
            errors.append(f"Catalog entry {idx + 1} ({title}): invalid price '{price}'")
            continue

        if price_val < 0:
            errors.append(f"Catalog entry {idx + 1} ({title}): negative price {price_val}")
            continue

        price_map[str(title).strip()] = price_val

    return price_map, errors


def compute_sale_total(sale_item, price_map, sale_idx):
    """
    Compute total for one sale. Returns (total, errors).
    """
    errors = []
    total = 0.0

    products = sale_item.get("Products") or sale_item.get("products") or sale_item.get("items")
    if products is None:
        errors.append(f"Sale {sale_idx + 1}: missing Products/products/items array")
        return total, errors

    if not isinstance(products, list):
        errors.append(f"Sale {sale_idx + 1}: Products must be an array")
        return total, errors

    for pidx, prod in enumerate(products):
        if not isinstance(prod, dict):
            errors.append(f"Sale {sale_idx + 1}, item {pidx + 1}: expected object")
            continue

        title = prod.get("title") or prod.get("name") or prod.get("product")
        qty = prod.get("quantity") or prod.get("qty") or prod.get("amount", 1)

        if title is None or title == "":
            errors.append(f"Sale {sale_idx + 1}, item {pidx + 1}: missing product title")
            continue

        try:
            quantity = int(qty) if isinstance(qty, (int, float)) else int(float(qty))
        except (TypeError, ValueError):
            msg = f"Sale {sale_idx + 1}, item {pidx + 1} ({title}): invalid quantity '{qty}'"
            errors.append(msg)
            continue

        if quantity < 0:
            errors.append(f"Sale {sale_idx + 1}, item {pidx + 1} ({title}): negative quantity")
            continue

        title_str = str(title).strip()
        if title_str not in price_map:
            msg = f"Sale {sale_idx + 1}, item {pidx + 1}: product '{title}' not in catalogue"
            errors.append(msg)
            continue

        total += price_map[title_str] * quantity

    return total, errors


def run_compute_sales(catalogue_path, sales_path):
    """
    Load catalogue and sales, compute totals. Returns (results_text, success).
    Elapsed time is appended by the caller.
    """
    # pylint: disable=too-many-locals
    all_errors = []

    catalogue_data, cat_err = load_json_file(catalogue_path)
    if cat_err:
        all_errors.append(cat_err)
        return "\n".join(all_errors) + "\n", False

    price_map, cat_parse_errors = build_price_map(catalogue_data)
    all_errors.extend(cat_parse_errors)

    sales_data, sales_err = load_json_file(sales_path)
    if sales_err:
        all_errors.append(sales_err)
        return "\n".join(all_errors) + "\n", False

    if not isinstance(sales_data, list):
        all_errors.append("Sales record must be a JSON array.")
        return "\n".join(all_errors) + "\n", False

    grand_total = 0.0
    sale_lines = []
    sale_num = 0

    for idx, sale_item in enumerate(sales_data):
        if not isinstance(sale_item, dict):
            all_errors.append(f"Sale record {idx + 1}: expected object, skipped")
            continue

        sale_name = sale_item.get("Sale") or sale_item.get("sale") or f"Sale {idx + 1}"
        sale_total, sale_errors = compute_sale_total(sale_item, price_map, idx)
        all_errors.extend(sale_errors)

        grand_total += sale_total
        sale_num += 1
        sale_lines.append(f"  {sale_num}. {sale_name}: ${sale_total:.2f}")

    lines_out = [
        "Sales Summary",
        "=" * 50,
        "",
        f"Total number of sales: {sale_num}",
        f"Grand total: ${grand_total:.2f}",
        "",
        "Details:",
        *sale_lines,
        "",
    ]

    if all_errors:
        lines_out.extend(["Warnings/Errors (execution continued):", "-" * 40] + all_errors + [""])

    return "\n".join(lines_out), sale_num > 0 or grand_total > 0


def main():
    """Entry point: parse args, run compute sales, write output and time."""
    if len(sys.argv) < 3:
        print(
            "Usage: python computeSales.py priceCatalogue.json salesRecord.json",
            file=sys.stderr,
        )
        sys.exit(1)

    catalogue_path = sys.argv[1]
    sales_path = sys.argv[2]

    if not os.path.isfile(catalogue_path):
        print(f"Error: Catalogue file not found: {catalogue_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(sales_path):
        print(f"Error: Sales file not found: {sales_path}", file=sys.stderr)
        sys.exit(1)

    start = time.perf_counter()
    results_text, success = run_compute_sales(catalogue_path, sales_path)
    elapsed = time.perf_counter() - start

    time_line = f"Time elapsed: {elapsed:.6f} seconds"
    full_output = results_text + time_line + "\n"

    output_path = "SalesResults.txt"
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(full_output)

    print(full_output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
