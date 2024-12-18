#!/usr/bin/env python3
import sys
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

bad_keywords = os.environ['DEV_BAD_KEYWORDS'].split(";")

def check_files():
    staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only']).decode('utf-8').splitlines()
    issues = []
    for file in staged_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    for bad_keyword in bad_keywords:
                        if bad_keyword in line:
                            issues.append(f"Found '{bad_keyword}' in '{file}':\n    {line.lstrip()}")
        except Exception as e:
            print(f"Error checking {file}: {e}")
            return 1
    if len(issues) != 0:
        for issue in issues:
            print(issue)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(check_files())
