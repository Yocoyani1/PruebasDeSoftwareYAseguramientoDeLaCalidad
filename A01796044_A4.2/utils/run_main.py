"""Common main flow: validate input file, run with timing, write output."""

import sys
import time


def validate_input_file(input_path):
    """Validate that input file exists and is readable. Exits on error."""
    try:
        with open(input_path, "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    except OSError as err:
        print(f"Error reading file: {err}", file=sys.stderr)
        sys.exit(1)


def run_timed_main(run_func, input_path, output_path):
    """
    Validate input, run run_func(input_path), time it, write results to output_path.
    run_func must return (results_text, success).
    Exits with 0 if success else 1.
    """
    validate_input_file(input_path)

    start = time.perf_counter()
    results_text, success = run_func(input_path)
    elapsed = time.perf_counter() - start

    time_line = f"Time elapsed: {elapsed:.6f} seconds"
    full_output = results_text + time_line + "\n"

    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(full_output)

    print(full_output)
    sys.exit(0 if success else 1)
