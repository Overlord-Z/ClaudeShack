#!/usr/bin/env python3
"""
Oracle Commit Recorder

Record git commits in Oracle timeline (for use in git hooks).

Usage:
    python record_commit.py
    python record_commit.py --message "commit message"

Example (in .oracle/hooks/pre-commit.sh):
    #!/bin/bash
    python .claude/skills/oracle/Scripts/record_commit.py
"""

import sys
import subprocess
from datetime import datetime
from pathlib import Path


def find_oracle_root():
    """Find the .oracle directory."""
    current = Path.cwd()

    while current != current.parent:
        oracle_path = current / '.oracle'
        if oracle_path.exists():
            return oracle_path
        current = current.parent

    return None


def get_commit_info():
    """Get information about the current/last commit."""
    try:
        # Get last commit message
        message = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=%B'],
            text=True
        ).strip()

        # Get changed files
        files = subprocess.check_output(
            ['git', 'diff', '--name-only', 'HEAD~1'],
            text=True
        ).strip().split('\n')

        # Get author
        author = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=%an'],
            text=True
        ).strip()

        # Get hash
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            text=True
        ).strip()

        return {
            'message': message,
            'files': [f for f in files if f],
            'author': author,
            'hash': commit_hash
        }

    except subprocess.CalledProcessError:
        return None


def record_to_timeline(oracle_path, commit_info):
    """Record commit to timeline."""
    timeline_file = oracle_path / 'timeline' / 'project_timeline.md'

    entry = f"""
## {datetime.now().strftime('%Y-%m-%d %H:%M')} - Commit: {commit_info['hash']}

**Author**: {commit_info['author']}

**Message**: {commit_info['message']}

**Files Changed**:
"""

    for file_path in commit_info['files'][:10]:  # Top 10 files
        entry += f"- `{file_path}`\n"

    if len(commit_info['files']) > 10:
        entry += f"- ... and {len(commit_info['files']) - 10} more\n"

    entry += "\n---\n"

    # Append to timeline
    with open(timeline_file, 'a') as f:
        f.write(entry)


def main():
    oracle_path = find_oracle_root()

    if not oracle_path:
        # Silent fail - not all projects will have Oracle
        sys.exit(0)

    commit_info = get_commit_info()

    if commit_info:
        record_to_timeline(oracle_path, commit_info)


if __name__ == '__main__':
    main()
