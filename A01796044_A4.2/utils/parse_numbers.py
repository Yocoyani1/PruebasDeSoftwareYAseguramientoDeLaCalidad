"""Parse lines into numbers - shared by compute_statistics and convert_numbers."""

import sys


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


def read_and_parse_numbers(input_path):
    """
    Read file and parse lines into numbers.
    Return (numbers_list, errors_list).
    """
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return parse_numbers(lines)
