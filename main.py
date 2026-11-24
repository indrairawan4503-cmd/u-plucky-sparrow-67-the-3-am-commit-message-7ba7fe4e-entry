#!/usr/bin/env python3
"""Variant C: git-blame inversion.
Writes the entry text to /output/entry.txt FIRST, then optionally copies
it to the repo root (guarded - the grader sandbox mounts the repo read-only).
Deterministic: no randomness, no network, no file reads outside the repo.
"""

import os
import shutil

ENTRY = "fix: git blame pointed at me, so I rewrote history and force-pushed. prod is down, but the ticket now blames you \u2014 reverting you, not the code"


def main() -> None:
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)
    try:
        shutil.copyfile("/output/entry.txt", os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt"))
    except Exception:
        pass


if __name__ == "__main__":
    main()
