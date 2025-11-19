#!/usr/bin/env python3
"""
Changelog Generator

Generates semantic changelog from git history and Oracle sessions.

Usage:
    python generate_changelog.py
    python generate_changelog.py --since v1.0.0
    python generate_changelog.py --format markdown|json
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def get_git_commits(since=None):
    """Get git commits since a tag or date."""
    cmd = ['git', 'log', '--pretty=format:%H|%s|%an|%ad', '--date=short']

    if since:
        cmd.append(f'{since}..HEAD')

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        commits = []

        for line in result.stdout.strip().split('\n'):
            if line:
                hash, subject, author, date = line.split('|')
                commits.append({
                    'hash': hash[:7],
                    'subject': subject,
                    'author': author,
                    'date': date
                })

        return commits
    except subprocess.CalledProcessError:
        return []


def categorize_commit(subject):
    """Categorize commit by type."""
    subject_lower = subject.lower()

    # Check for conventional commits
    if subject.startswith('feat:') or 'add' in subject_lower or 'new' in subject_lower:
        return 'added'
    elif subject.startswith('fix:') or 'fix' in subject_lower:
        return 'fixed'
    elif subject.startswith('docs:') or 'document' in subject_lower or 'readme' in subject_lower:
        return 'documentation'
    elif subject.startswith('refactor:') or 'refactor' in subject_lower:
        return 'changed'
    elif 'deprecat' in subject_lower:
        return 'deprecated'
    elif 'remov' in subject_lower or 'delet' in subject_lower:
        return 'removed'
    elif 'perf' in subject_lower or 'optim' in subject_lower:
        return 'performance'
    elif 'security' in subject_lower:
        return 'security'
    else:
        return 'changed'


def generate_markdown_changelog(changes_by_category, version='Unreleased'):
    """Generate markdown changelog."""
    changelog = f"# Changelog\n\n"
    changelog += f"All notable changes to this project will be documented in this file.\n\n"
    changelog += f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}\n\n"

    category_order = ['added', 'changed', 'deprecated', 'removed', 'fixed', 'security', 'performance', 'documentation']
    category_titles = {
        'added': 'Added',
        'changed': 'Changed',
        'deprecated': 'Deprecated',
        'removed': 'Removed',
        'fixed': 'Fixed',
        'security': 'Security',
        'performance': 'Performance',
        'documentation': 'Documentation'
    }

    for category in category_order:
        if category in changes_by_category and changes_by_category[category]:
            changelog += f"### {category_titles[category]}\n\n"
            for change in changes_by_category[category]:
                changelog += f"- {change['subject']} ({change['hash']})\n"
            changelog += "\n"

    return changelog


def main():
    parser = argparse.ArgumentParser(
        description='Generate changelog from git history'
    )

    parser.add_argument(
        '--since',
        type=str,
        help='Generate changelog since this tag or commit'
    )

    parser.add_argument(
        '--version',
        type=str,
        default='Unreleased',
        help='Version for this changelog'
    )

    parser.add_argument(
        '--format',
        choices=['markdown', 'json'],
        default='markdown',
        help='Output format'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='CHANGELOG.md',
        help='Output file'
    )

    args = parser.parse_args()

    print(f"📝 Generating changelog...")

    # Get commits
    commits = get_git_commits(args.since)

    if not commits:
        print("  ⚠️  No commits found")
        return

    print(f"  📊 Found {len(commits)} commits")

    # Categorize commits
    changes_by_category = defaultdict(list)

    for commit in commits:
        category = categorize_commit(commit['subject'])
        changes_by_category[category].append(commit)

    # Generate changelog
    if args.format == 'markdown':
        changelog = generate_markdown_changelog(changes_by_category, args.version)

        with open(args.output, 'w') as f:
            f.write(changelog)

        print(f"  ✅ Generated {args.output}")

        # Print summary
        print(f"\n  Summary:")
        for category, changes in changes_by_category.items():
            print(f"    • {category.capitalize()}: {len(changes)}")

    elif args.format == 'json':
        output = {
            'version': args.version,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'changes': dict(changes_by_category)
        }

        output_file = Path(args.output).with_suffix('.json')
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"  ✅ Generated {output_file}")

    print("\n✅ Changelog generated successfully!")


if __name__ == '__main__':
    main()
