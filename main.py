#!/usr/bin/env python3
"""Write and verify the judged one-line excuse at /output/entry.txt.

The artifact is a single UTF-8 line, 1..180 characters, with no trailing
newline.  Writing goes through a temporary file in /output followed by
os.replace, so a reader never sees a half-written artifact.  After the
replace, the bytes on disk are read back and checked against the source.
"""

import hashlib
import os
import tempfile

OUTPUT = "/output/entry.txt"

# The exact judged artifact: one line, UTF-8, no trailing newline.
ENTRY = (
    "Sorry — I marked the deploy low-risk: one character. "
    "It was the 's' in 'https'. "
    "The site has never been safer from visitors."
)


def checked_bytes(text: str) -> bytes:
    """Encode once and enforce every gate rule before touching the output."""
    data = text.encode("utf-8")
    decoded = data.decode("utf-8")  # fail loudly on any encoding surprise
    if decoded != text:
        raise ValueError("entry does not survive a UTF-8 round trip")
    if not (1 <= len(decoded) <= 180):
        raise ValueError("entry must be 1..180 characters")
    if not decoded.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in decoded or "\r" in decoded:
        raise ValueError("entry must be one line with no trailing newline")
    return data


def verify_on_disk(expected: bytes) -> None:
    """Re-read the final artifact and prove the atomic write landed intact."""
    with open(OUTPUT, "rb") as handle:
        actual = handle.read()
    if actual != expected:
        raise ValueError("the bytes at /output/entry.txt differ from the entry")
    text = actual.decode("utf-8")
    if not (1 <= len(text) <= 180) or not text.strip():
        raise ValueError("the written artifact fails the 1..180 character gate")


def main() -> None:
    data = checked_bytes(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    fd, tmp = tempfile.mkstemp(prefix=".entry-", dir=os.path.dirname(OUTPUT))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, OUTPUT)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise

    # Improvement over the first write: prove what is on disk is what we meant.
    verify_on_disk(data)

    print(f"wrote {len(data)} bytes, {len(ENTRY)} chars, sha256 {hashlib.sha256(data).hexdigest()}")
    print("UTF-8: ok | 1..180 chars: ok | non-whitespace: ok | single line, no trailing newline: ok | atomic replace: verified")


if __name__ == "__main__":
    main()
