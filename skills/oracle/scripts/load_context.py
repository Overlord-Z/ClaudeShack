#!/usr/bin/env python3
"""
Oracle Context Loader

Load Oracle context at session start (for use in hooks).
Displays relevant knowledge to Claude at the beginning of a session.

Usage:
    python load_context.py
    python load_context.py --verbose

Example (in .claude/hooks/session-start.sh):
    #!/bin/bash
    python .claude/skills/oracle/scripts/load_context.py
"""

import sys
from pathlib import Path
import subprocess


def find_oracle_root():
    """Find the .oracle directory."""
    current = Path.cwd()

    while current != current.parent:
        oracle_path = current / '.oracle'
        if oracle_path.exists():
            return oracle_path
        current = current.parent

    return None


def main():
    verbose = '--verbose' in sys.argv

    oracle_path = find_oracle_root()

    if not oracle_path:
        if verbose:
            print("Oracle not initialized for this project.")
        return

    # Run generate_context.py with --session-start
    script_path = Path(__file__).parent / 'generate_context.py'

    try:
        result = subprocess.run(
            ['python3', str(script_path), '--session-start'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(result.stdout)
        else:
            if verbose:
                print(f"Warning: Could not load Oracle context: {result.stderr}")

    except Exception as e:
        if verbose:
            print(f"Warning: Error loading Oracle context: {e}")


if __name__ == '__main__':
    main()
