#!/usr/bin/env python3
"""
Count distinct words and their frequency from a file using basic algorithms.
"""

import os
import sys

# Add project root to path so utils can be imported when run as script
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from utils.run_main import run_timed_main


def split_into_words(text):
    """Split text by whitespace (basic algorithm, no regex)."""
    words = []
    current = []
    for char in text:
        if char in " \t\n\r":
            if current:
                words.append("".join(current))
                current = []
        else:
            current.append(char)
    if current:
        words.append("".join(current))
    return words


def count_words(words):
    """Build frequency map: word -> count (basic algorithm)."""
    freq = {}
    for word in words:
        word_lower = word.lower()
        freq[word_lower] = freq.get(word_lower, 0) + 1
    return freq


def run_word_count(input_path):
    """
    Read file, count distinct words and frequency.
    Return (results_text, success). Caller appends elapsed time.
    """
    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    words = split_into_words(content)

    if not words:
        return "No words found in file.\n", False

    freq = count_words(words)
    sorted_words = sorted(freq.keys())

    lines_out = ["Word Count Results", "=" * 40]
    for word in sorted_words:
        lines_out.append(f"{word}: {freq[word]}")
    lines_out.append("")
    lines_out.append(f"Total distinct words: {len(freq)}")
    lines_out.append(f"Total words: {len(words)}")
    lines_out.append("")

    return "\n".join(lines_out), True


def main():
    """Entry point: parse args, run word count, write output and time."""
    if len(sys.argv) < 2:
        print(
            "Usage: python word_count.py fileWithData.txt [output_dir]",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else ""
    out_file = "WordCountResults.txt"
    output_path = os.path.join(output_dir, out_file) if output_dir else out_file

    run_timed_main(run_word_count, input_path, output_path)


if __name__ == "__main__":
    main()
