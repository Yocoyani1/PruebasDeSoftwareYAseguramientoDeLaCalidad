#!/usr/bin/env python3
"""
Compute descriptive statistics from a file containing numbers.
Medidas: Media, Moda, Mediana, Desviación Estándar Poblacional, Varianza Poblacional.
Algoritmos básicos (sin librerías de estadística).
"""

import os
import sys
import time


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


def compute_mean(numbers):
    """Compute mean using sum/count (basic algorithm)."""
    if not numbers:
        return None
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)


def compute_median(numbers):
    """Compute median by sorting and taking middle (basic algorithm)."""
    if not numbers:
        return None
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 1:
        return sorted_nums[mid]
    return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2


def compute_mode(numbers):
    """Compute mode by counting frequency (basic algorithm)."""
    if not numbers:
        return None
    freq = {}
    for num in numbers:
        freq[num] = freq.get(num, 0) + 1
    max_count = 0
    for count in freq.values():
        if count > max_count:
            max_count = count
    modes = [num for num, count in freq.items() if count == max_count]
    modes.sort()
    return modes[0] if len(modes) == 1 else modes


def compute_variance(numbers, mean_val):
    """Varianza poblacional: suma (x - media)^2 / n (algoritmo básico)."""
    if not numbers or mean_val is None:
        return None
    n = len(numbers)
    total = 0
    for num in numbers:
        diff = num - mean_val
        total += diff * diff
    return total / n


def compute_std_dev(variance_val):
    """Desviación estándar poblacional: raíz cuadrada de la varianza poblacional."""
    if variance_val is None or variance_val < 0:
        return None
    # Newton's method for sqrt (basic algorithm, no math.sqrt)
    if variance_val == 0:
        return 0.0
    x = variance_val
    for _ in range(20):
        x = (x + variance_val / x) / 2
    return x


def run_statistics(input_path):
    """
    Read file, compute statistics, return (results_text, success).
    Elapsed time is appended to results_text by the caller.
    """
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    numbers, _ = parse_numbers(lines)

    if not numbers:
        return "No valid numbers found in file.\n", False

    mean_val = compute_mean(numbers)
    median_val = compute_median(numbers)
    mode_val = compute_mode(numbers)
    variance_val = compute_variance(numbers, mean_val)
    std_val = compute_std_dev(variance_val)

    mode_str = mode_val
    if isinstance(mode_val, list):
        mode_str = ", ".join(str(m) for m in mode_val)

    lines_out = [
        "Descriptive Statistics (Medidas solicitadas)",
        "=" * 40,
        f"Count: {len(numbers)}",
        f"Media: {mean_val}",
        f"Mediana: {median_val}",
        f"Moda: {mode_str}",
        f"Varianza Poblacional: {variance_val}",
        f"Desviacion Estandar Poblacional: {std_val}",
        "",
    ]
    return "\n".join(lines_out), True


def main():
    """Entry point: parse args, run statistics, write output and time."""
    if len(sys.argv) < 2:
        print("Usage: python computeStatistics.py fileWithData.txt [output_dir]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else ""
    output_path = os.path.join(output_dir, "StatisticsResults.txt") if output_dir else "StatisticsResults.txt"

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
    results_text, success = run_statistics(input_path)
    elapsed = time.perf_counter() - start

    time_line = f"Time elapsed: {elapsed:.6f} seconds"
    full_output = results_text + time_line + "\n"

    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(full_output)

    print(full_output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
