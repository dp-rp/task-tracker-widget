#!/usr/bin/env python3
import sys
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

bad_keywords = os.environ["DEV_BAD_KEYWORDS"].split(";")

# Add any .env values where the key is prefixed with `SECRET_` to the bad_keywords list
for key, value in dotenv_values().items():
    # HACK: quick and dirty split
    if key.split("_")[0] == "SECRET":
        bad_keywords.append(value)


bad_keywords_casefolded = [kw.casefold() for kw in bad_keywords]


def check_files():
    filepaths_to_check = sys.argv[1:]
    issues = []
    for filepath in filepaths_to_check:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    # if line without leading whitespace is empty, skip it
                    if line.lstrip() == "":
                        continue
                    # casefold for case-insensitive string comparison
                    line_casefolded = line.casefold()
                    for bad_kw_idx in range(len(bad_keywords)):
                        if bad_keywords_casefolded[bad_kw_idx] in line_casefolded:
                            issues.append(
                                f"Found '{bad_keywords[bad_kw_idx]}' in '{filepath}':\n    {line.lstrip()}"
                            )
        except Exception as e:
            print(f"Error checking {filepath}: {e}")
            return 1
    if len(issues) != 0:
        for issue in issues:
            print(issue)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(check_files())
