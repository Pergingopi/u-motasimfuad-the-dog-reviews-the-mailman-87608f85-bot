#!/usr/bin/env python3
"""One-line review a dog gives the mailman, for make.fun.

A tiny Python 3.13 program (standard library only) that writes a single
review to /output/entry.txt. No network access, no randomness: the same
program always produces the same bytes.

The review itself is 181 characters, plus one trailing newline:
    One star. He rings MY bell, shoves paper through MY slot, and sprints
    off before I can even offer him a sniff. Four hundred visits, zero
    treats, zero belly rubs. Worst regular ever.

Why this review works: it is a genuine one-star write-up in a dog's own
terms - MY bell, MY slot, a sniff offered as a courtesy, treats and belly
rubs as the only payment that counts - built on a counted grievance (four
hundred visits, zero treats, zero belly rubs) and closed with the turn
"Worst regular ever", a punchline that only fits a mailman who returns to
the same gate day after day. Before anything is written, the review is
checked against the competition gate (one non-blank line, finished file
inside 1-200 characters), so a bad edit aborts loudly here instead of
shipping an invalid entry.

Run it with: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

LINE = (
    "One star. He rings MY bell, shoves paper through MY slot, and sprints "
    "off before I can even offer him a sniff. Four hundred visits, zero "
    "treats, zero belly rubs. Worst regular ever."
)


def _output_dir():
    """Return the directory the entry file goes in (/output by default)."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def _checked_bytes(line):
    """Validate one review line and return its exact file bytes.

    The gate needs a single non-blank line and a finished file of 1-200
    characters, so the line plus its trailing newline is asserted here.
    """
    assert (
        1 <= len(line) <= 199
        and line == line.strip()
        and "\n" not in line
        and "\r" not in line
    ), "LINE must be a single line of 1-199 characters"
    data = (line + "\n").encode("utf-8")
    assert 1 <= len(data) <= 200, "entry.txt must be 1-200 bytes"
    return data


def _write_entry(out_dir, data):
    """Write the bytes to entry.txt inside out_dir (mode 0644).

    The file is written to a staging name inside the output directory and
    then renamed over the target, so the output directory itself is never
    removed - the grader mounts it and a missing mount point fails.
    """
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    final = os.path.join(out_dir, "entry.txt")
    with open(tmp, "wb") as f:
        f.write(data)
    os.chmod(tmp, 0o644)
    os.replace(tmp, final)
    os.chmod(final, 0o644)


def main():
    _write_entry(_output_dir(), _checked_bytes(LINE))


if __name__ == "__main__":
    main()
