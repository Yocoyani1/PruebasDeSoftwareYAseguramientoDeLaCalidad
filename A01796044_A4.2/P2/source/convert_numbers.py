#!/usr/bin/env python3
"""
Convert numbers from a file to binary and hexadecimal using basic algorithms.
"""

import os
import sys

# Add project root to path so utils can be imported when run as script
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from utils.parse_numbers import read_and_parse_numbers
from utils.run_main import run_timed_main

HEX_DIGITS = "0123456789ABCDEF"


def to_binary(num):
    """Convert integer to binary string using division by 2 (basic algorithm)."""
    if num == 0:
        return "0"
    n = int(num)
    if n < 0:
        n = -n
    digits = []
    while n > 0:
        digits.append(str(n % 2))
        n = n // 2
    digits.reverse()
    return "".join(digits)


def to_hexadecimal(num):
    """Convert integer to hex string using division by 16 (basic algorithm)."""
    if num == 0:
        return "0"
    n = int(num)
    if n < 0:
        n = -n
    digits = []
    while n > 0:
        digits.append(HEX_DIGITS[n % 16])
        n = n // 16
    digits.reverse()
    return "".join(digits)


def run_conversions(input_path):
    """
    Read file, convert each number to binary and hex.
    Return (results_text, success). Caller appends elapsed time.
    """
    numbers, _ = read_and_parse_numbers(input_path)
    if not numbers:
        return "No valid numbers found in file.\n", False

    lines_out = ["Number to Binary and Hexadecimal", "=" * 40]
    for num in numbers:
        bin_str = to_binary(num)
        hex_str = to_hexadecimal(num)
        lines_out.append(f"Number: {num}")
        lines_out.append(f"  Binary: {bin_str}")
        lines_out.append(f"  Hexadecimal: {hex_str}")
        lines_out.append("")

    return "\n".join(lines_out), True


def main():
    """Entry point: parse args, run conversions, write output and time."""
    if len(sys.argv) < 2:
        print(
            "Usage: python convert_numbers.py fileWithData.txt [output_dir]",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else ""
    out_file = "ConvertionResults.txt"
    output_path = os.path.join(output_dir, out_file) if output_dir else out_file

    run_timed_main(run_conversions, input_path, output_path)


if __name__ == "__main__":
    main()
