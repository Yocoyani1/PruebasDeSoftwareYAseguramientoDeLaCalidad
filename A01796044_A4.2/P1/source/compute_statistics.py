#!/usr/bin/env python3
"""
Compute descriptive statistics from a file containing numbers.
Medidas: Media, Moda, Mediana, Desviación Estándar Poblacional, Varianza Poblacional.
Algoritmos básicos (sin librerías de estadística).
"""

import os
import sys

# Add project root to path so utils can be imported when run as script
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from utils.parse_numbers import parse_numbers, read_and_parse_numbers
from utils.run_main import run_timed_main

# Re-export for tests
__all__ = ["parse_numbers", "compute_mean", "compute_median", "compute_mode"]


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
        max_count = max(max_count, count)
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
    numbers, _ = read_and_parse_numbers(input_path)
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
        print(
            "Usage: python compute_statistics.py fileWithData.txt [output_dir]",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else ""
    out_file = "StatisticsResults.txt"
    output_path = os.path.join(output_dir, out_file) if output_dir else out_file

    run_timed_main(run_statistics, input_path, output_path)


if __name__ == "__main__":
    main()
