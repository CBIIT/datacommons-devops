#!/usr/bin/python
"""
Shared text-parsing helpers used by the Endpoint_Query / Browser_Query
regex-based script parsers in this package.
"""


def extract_balanced_braces(text, open_brace_index):
    """Return the substring from open_brace_index through its matching '}'."""
    depth = 0
    for i in range(open_brace_index, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[open_brace_index : i + 1]
    return None
