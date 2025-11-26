#!/usr/bin/env python3
"""
Documentation Synchronization Script

Syncs documentation from Oracle knowledge, Summoner MCDs, and Style Master guides.

Usage:
    python sync_docs.py --source oracle
    python sync_docs.py --source summoner
    python sync_docs.py --source style-master
    python sync_docs.py --source all
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


def find_oracle_root():
    """Find .oracle directory."""
    current = Path.cwd()
    while current != current.parent:
        oracle_path = current / '.oracle'
        if oracle_path.exists():
            return oracle_path
        current = current.parent
    return None


def sync_from_oracle(oracle_path, output_dir):
    """Sync documentation from Oracle knowledge base."""
    print(" Syncing from Oracle knowledge base...")

    knowledge_dir = oracle_path / 'knowledge'
    if not knowledge_dir.exists():
        print("  [WARNING]  No Oracle knowledge found")
        return

    patterns_file = knowledge_dir / 'patterns.json'
    gotchas_file = knowledge_dir / 'gotchas.json'

    sections = []

    # Load patterns
    if patterns_file.exists():
        with open(patterns_file, 'r') as f:
            patterns = json.load(f)

        if patterns:
            sections.append("## Architecture Patterns\n")
            sections.append("*From Oracle knowledge base*\n\n")

            for pattern in patterns[:10]:  # Top 10
                title = pattern.get('title', 'Untitled')
                content = pattern.get('content', '')
                sections.append(f"### {title}\n\n{content}\n\n")

    # Load gotchas
    if gotchas_file.exists():
        with open(gotchas_file, 'r') as f:
            gotchas = json.load(f)

        if gotchas:
            sections.append("## Known Issues & Gotchas\n")
            sections.append("*From Oracle knowledge base*\n\n")

            for gotcha in gotchas[:10]:
                title = gotcha.get('title', 'Untitled')
                content = gotcha.get('content', '')
                priority = gotcha.get('priority', 'medium')
                emoji = {'critical': '', 'high': '', 'medium': '', 'low': ''}.get(priority, '')
                sections.append(f"### {emoji} {title}\n\n{content}\n\n")

    if sections:
        # Write to ARCHITECTURE.md
        output_file = output_dir / 'ARCHITECTURE.md'
        with open(output_file, 'w') as f:
            f.write(f"# Architecture Documentation\n\n")
            f.write(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
            f.write(''.join(sections))

        print(f"  [OK] Created {output_file}")
        print(f"  [NOTE] Synced {len(patterns if patterns_file.exists() else [])} patterns, {len(gotchas if gotchas_file.exists() else [])} gotchas")
    else:
        print("  [WARNING]  No patterns or gotchas to sync")


def sync_from_style_master(project_path, output_dir):
    """Sync from Style Master style guide."""
    print(" Syncing from Style Master...")

    style_guide = project_path / 'STYLEGUIDE.md'
    if style_guide.exists():
        # Copy style guide to docs
        output_file = output_dir / 'STYLEGUIDE.md'
        with open(style_guide, 'r') as f:
            content = f.read()

        with open(output_file, 'w') as f:
            f.write(content)

        print(f"  [OK] Synced {output_file}")
    else:
        print("  [WARNING]  No STYLEGUIDE.md found")


def sync_from_summoner(project_path, output_dir):
    """Sync from Summoner Mission Control Documents."""
    print(" Syncing from Summoner MCDs...")

    # Look for mission-*.md files
    mcds = list(project_path.glob('mission-*.md'))

    if not mcds:
        print("  [WARNING]  No Summoner MCDs found")
        return

    adr_dir = output_dir / 'adr'
    adr_dir.mkdir(exist_ok=True)

    for mcd in mcds:
        print(f"   Processing {mcd.name}")

        with open(mcd, 'r') as f:
            content = f.read()

        # Extract decisions from MCD
        if '## Decisions' in content:
            decisions_section = content.split('## Decisions')[1].split('\n\n')[0]

            # Create ADR
            adr_num = len(list(adr_dir.glob('*.md'))) + 1
            adr_file = adr_dir / f'{adr_num:03d}-from-{mcd.stem}.md'

            adr_content = f"""# ADR-{adr_num:03d}: Decisions from {mcd.stem}

Date: {datetime.now().strftime('%Y-%m-%d')}
Status: Accepted
Source: Summoner MCD {mcd.name}

## Context

From Mission Control Document: {mcd.name}

## Decisions

{decisions_section}

## Links

- Source MCD: {mcd.name}
"""

            with open(adr_file, 'w') as f:
                f.write(adr_content)

            print(f"    [OK] Created ADR: {adr_file.name}")


def main():
    parser = argparse.ArgumentParser(
        description='Sync documentation from various sources'
    )

    parser.add_argument(
        '--source',
        choices=['oracle', 'summoner', 'style-master', 'all'],
        default='all',
        help='Source to sync from'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='docs',
        help='Output directory (default: docs/)'
    )

    args = parser.parse_args()

    project_path = Path.cwd()
    output_dir = project_path / args.output
    output_dir.mkdir(exist_ok=True)

    print(f" Syncing documentation to {output_dir}\n")

    if args.source in ['oracle', 'all']:
        oracle_path = find_oracle_root()
        if oracle_path:
            sync_from_oracle(oracle_path, output_dir)
        else:
            print("[WARNING]  Oracle not initialized for this project")
        print()

    if args.source in ['style-master', 'all']:
        sync_from_style_master(project_path, output_dir)
        print()

    if args.source in ['summoner', 'all']:
        sync_from_summoner(project_path, output_dir)
        print()

    print("[OK] Documentation sync complete!")


if __name__ == '__main__':
    main()
