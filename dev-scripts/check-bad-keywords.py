#!/usr/bin/env python3
import sys
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

bad_keywords = (kw.casefold() for kw in os.environ["DEV_BAD_KEYWORDS"].split(";"))

# badKEYword


def check_files():
    filepaths_to_check = sys.argv[1:]
    issues = []
    for filepath in filepaths_to_check:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in (l.casefold() for l in f):
                    for bad_keyword in bad_keywords:
                        if bad_keyword in line:
                            issues.append(
                                f"Found '{bad_keyword}' in '{filepath}':\n    {line.lstrip()}"
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
