#!/usr/bin/env python3
"""One-line dad joke: check the fixed entry, then write it out.

The Wi-Fi password is "incorrect", so the router agrees with every
mistake. This program never accepts outside text: it holds exactly one
joke, proves that joke is well formed, and saves it to a file. There
is no input, no network access, no clock, and no randomness anywhere
in here.
"""

import sys

ENTRY = "I told my son the Wi-Fi password is 'incorrect'. Now every time he mistypes it, the router just agrees with him."
CHAR_LIMIT = 140
DESTINATION = "/output/entry.txt"
ENDERS = (".", "!", "?")
FILLER = set(".,!?;:'\"-() ")


def fail(problem):
    """Print why the entry was refused and stop without writing."""
    print(f"refused: {problem}", file=sys.stderr)
    raise SystemExit(1)


def guard_nonempty(text):
    return bool(text and text.strip())


def guard_short_enough(text):
    return len(text) <= CHAR_LIMIT


def guard_no_controls(text):
    return all(ord(letter) >= 32 for letter in text)


def guard_tidy_spacing(text):
    stripped = text.strip()
    return text == stripped and "  " not in text and "\t" not in text


def guard_has_letters(text):
    return any(letter.isalpha() for letter in text)


def guard_not_only_marks(text):
    return not all(letter in FILLER for letter in text)


def guard_not_only_digits(text):
    return not text.strip().isdigit()


def guard_ends_with_mark(text):
    return text.rstrip().endswith(ENDERS)


def guard_names_password(text):
    return "password" in text.lower()


def guard_digit_free(text):
    # A dad joke has no business carrying numbers.
    return not any(letter.isdigit() for letter in text)


def guard_no_doubled_mark(text):
    # Two sentence marks back to back is a typo, not emphasis.
    marks = set(".,!?;:")
    return all(not (a in marks and b in marks) for a, b in zip(text, text[1:]))


# Every guard is listed with the complaint shown when it trips. The
# checker runs them in this order and stops at the first failure, so a
# bad entry never reaches the file.
RULES = [
    ("entry must mention the password", guard_names_password),
    ("entry must not contain digits", guard_digit_free),
    ("entry must not run two sentence marks together", guard_no_doubled_mark),
    ("entry is empty", guard_nonempty),
    ("entry is longer than the 140 character limit", guard_short_enough),
    ("entry contains control characters", guard_no_controls),
    ("entry has ragged spacing or a tab", guard_tidy_spacing),
    ("entry contains no letters", guard_has_letters),
    ("entry is punctuation only", guard_not_only_marks),
    ("entry is digits only", guard_not_only_digits),
    ("entry does not end with punctuation", guard_ends_with_mark),
]


def check_entry(text):
    for problem, guard in RULES:
        if not guard(text):
            fail(problem)


def main():
    check_entry(ENTRY)
    with open(DESTINATION, "w", encoding="utf-8") as out:
        out.write(ENTRY + "\n")


if __name__ == "__main__":
    main()
