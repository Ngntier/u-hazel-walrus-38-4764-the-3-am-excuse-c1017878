"""One-line entry writer for the 3 AM excuse bounty.

The program keeps a single fixed entry string, checks it against a
handful of sanity rules, and then writes it verbatim to entry.txt
inside the output directory chosen by the environment.
"""

import os
import sys

ENTRY = "It's 3 AM \u2014 my job is protecting you from yourself, and yourself is about to buy a coin named after a dog."

MAX_CHARS = 200
MAX_BYTES = 400


def fail(message):
    """Abort with a clear message on stderr and a non-zero status."""
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def check_not_blank(text):
    """Reject an entry that is empty or only whitespace."""
    if not text or not text.strip():
        fail("entry text is empty or only whitespace")


def check_no_edge_space(text):
    """Reject an entry with leading or trailing whitespace."""
    if text != text.strip():
        fail("entry text starts or ends with whitespace")


def check_no_control_chars(text):
    """Reject any control character in the entry."""
    for char in text:
        code = ord(char)
        if code < 0x20 or code == 0x7F:
            fail("entry text contains a control character (U+%04X)" % code)


def check_size_limits(text):
    """Reject an entry that is too long in characters or UTF-8 bytes."""
    if len(text) > MAX_CHARS:
        fail("entry text is %d characters, over the %d limit" % (len(text), MAX_CHARS))
    encoded = text.encode("utf-8")
    if len(encoded) > MAX_BYTES:
        fail("entry text is %d UTF-8 bytes, over the %d limit" % (len(encoded), MAX_BYTES))
    return encoded


def check_entry(text):
    """Run every spec check in turn and return the encoded entry."""
    check_not_blank(text)
    check_no_edge_space(text)
    check_no_control_chars(text)
    return check_size_limits(text)


def output_path():
    """Resolve the destination file from the environment, defaulting to /output."""
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(base, "entry.txt")


def main():
    payload = check_entry(ENTRY)
    target = output_path()
    parent = os.path.dirname(target)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(payload)


if __name__ == "__main__":
    main()
