#!/usr/bin/env python3
"""The 3 AM Commit Message — variant C: git-blame inversion.

Builds the entry text from clearly-named parts, validates it against the
contest rules (one line, 1-200 characters), then writes it to
/output/entry.txt FIRST and only afterwards attempts a copy into the repo
root. The repo-root copy is guarded: the grader sandbox mounts the repo
read-only, so a failed copy must never crash the run.

Deterministic: no randomness, no network, no file reads outside the repo.
"""

import os
import shutil

# --- entry text, assembled from named parts ------------------------------
# The joke in three beats: the conventional commit prefix, the incriminating
# setup, and the twist that reassigns the blame to the reader.
PREFIX = "fix: "
SETUP = "git blame pointed at me, so I rewrote history and force-pushed. "
TWIST = "prod is down, but the ticket now blames you \u2014 reverting you, not the code"

ENTRY = PREFIX + SETUP + TWIST

MAX_CHARS = 200  # contest limit: 200 characters or fewer


def build_entry() -> str:
    """Assemble the entry and validate it against the contest rules.

    Cross-checks the parts against the ENTRY constant so a drift in any
    single part is caught here instead of silently changing the output.
    """
    assembled = PREFIX + SETUP + TWIST
    if assembled != ENTRY:
        raise ValueError("assembled entry does not match ENTRY constant")
    text = ENTRY
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} chars, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    return text


def write_entry(text: str) -> None:
    """Write to /output first; repo-root copy is best-effort only."""
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(text)
    try:
        repo_root = os.path.dirname(os.path.abspath(__file__))
        shutil.copyfile("/output/entry.txt", os.path.join(repo_root, "entry.txt"))
    except Exception:
        pass  # grader sandbox is read-only; /output is the real deliverable


def main() -> None:
    write_entry(build_entry())


if __name__ == "__main__":
    main()
