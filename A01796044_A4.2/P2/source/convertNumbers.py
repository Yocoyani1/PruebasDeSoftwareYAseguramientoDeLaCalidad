#!/usr/bin/env python3
"""
Convert numbers from a file to binary and hexadecimal using basic algorithms.
"""

import os
import sys
import time

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


def parse_numbers(lines):
    """Parse lines into valid numbers, return (numbers_list, errors_list)."""
    numbers = []
    errors = []
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            value = float(line)
            numbers.append(value)
        except ValueError:
            msg = f"Error in line {line_num}: invalid data '{line}'"
            errors.append(msg)
            print(msg, file=sys.stderr)
    return numbers, errors


def run_conversions(input_path):
    """
    Read file, convert each number to binary and hex.
    Return (results_text, success). Caller appends elapsed time.
    """
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    numbers, _ = parse_numbers(lines)

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
        print("Usage: python convertNumbers.py fileWithData.txt [output_dir]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else ""
    output_path = os.path.join(output_dir, "ConvertionResults.txt") if output_dir else "ConvertionResults.txt"

    try:
        with open(input_path, "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    except OSError as err:
        print(f"Error reading file: {err}", file=sys.stderr)
        sys.exit(1)

    start = time.perf_counter()
    results_text, success = run_conversions(input_path)
    elapsed = time.perf_counter() - start

    time_line = f"Time elapsed: {elapsed:.6f} seconds"
    full_output = results_text + time_line + "\n"

    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(full_output)

    print(full_output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
