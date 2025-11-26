#!/usr/bin/env python3
"""
Oracle Knowledge Query Script

Search and retrieve knowledge from the Oracle knowledge base.

Usage:
    python query_knowledge.py "search term"
    python query_knowledge.py --category patterns
    python query_knowledge.py --priority critical
    python query_knowledge.py --tags api,auth
    python query_knowledge.py --recent 5

Examples:
    python query_knowledge.py "authentication"
    python query_knowledge.py --category gotchas --priority high
    python query_knowledge.py --tags database --recent 10
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


def find_oracle_root():
    """Find the .oracle directory by walking up from current directory."""
    current = Path.cwd()

    while current != current.parent:
        oracle_path = current / '.oracle'
        if oracle_path.exists():
            return oracle_path
        current = current.parent

    return None


def load_knowledge(oracle_path, category=None):
    """Load knowledge from specified category or all categories."""
    knowledge_dir = oracle_path / 'knowledge'
    all_knowledge = []

    categories = [category] if category else ['patterns', 'preferences', 'gotchas', 'solutions', 'corrections']

    for cat in categories:
        file_path = knowledge_dir / f'{cat}.json'
        if file_path.exists():
            with open(file_path, 'r') as f:
                entries = json.load(f)
                for entry in entries:
                    entry['_category'] = cat
                    all_knowledge.append(entry)

    return all_knowledge


def search_knowledge(knowledge, query=None, priority=None, tags=None):
    """Filter knowledge based on search criteria."""
    results = knowledge

    # Filter by query (search in title and content)
    if query:
        query_lower = query.lower()
        results = [
            entry for entry in results
            if query_lower in entry.get('title', '').lower()
            or query_lower in entry.get('content', '').lower()
            or query_lower in str(entry.get('context', '')).lower()
        ]

    # Filter by priority
    if priority:
        results = [entry for entry in results if entry.get('priority') == priority]

    # Filter by tags
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]
        results = [
            entry for entry in results
            if any(tag in entry.get('tags', []) for tag in tag_list)
        ]

    return results


def sort_knowledge(knowledge, sort_by='priority'):
    """Sort knowledge by various criteria."""
    priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

    if sort_by == 'priority':
        return sorted(knowledge, key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
    elif sort_by == 'recent':
        return sorted(knowledge, key=lambda x: x.get('created', ''), reverse=True)
    elif sort_by == 'used':
        return sorted(knowledge, key=lambda x: x.get('use_count', 0), reverse=True)
    else:
        return knowledge


def format_entry(entry, compact=False):
    """Format a knowledge entry for display."""
    if compact:
        return f"  [{entry['_category']}] {entry.get('title', 'Untitled')} (Priority: {entry.get('priority', 'N/A')})"

    output = []
    output.append("" * 70)
    output.append(f" {entry.get('title', 'Untitled')}")
    output.append(f"   Category: {entry['_category']} | Priority: {entry.get('priority', 'N/A')}")

    if entry.get('tags'):
        output.append(f"   Tags: {', '.join(entry['tags'])}")

    output.append("")
    output.append(f"   {entry.get('content', 'No content')}")

    if entry.get('context'):
        output.append("")
        output.append(f"   Context: {entry['context']}")

    if entry.get('examples'):
        output.append("")
        output.append("   Examples:")
        for ex in entry['examples']:
            output.append(f"     - {ex}")

    output.append("")
    output.append(f"   Created: {entry.get('created', 'Unknown')}")
    output.append(f"   Used: {entry.get('use_count', 0)} times")

    if entry.get('learned_from'):
        output.append(f"   Source: {entry['learned_from']}")

    return "\n".join(output)


def display_results(results, compact=False, limit=None):
    """Display search results."""
    if not results:
        print("[ERROR] No knowledge found matching your criteria.")
        return

    total = len(results)
    display_count = min(limit, total) if limit else total

    print(f"\n[SEARCH] Found {total} result(s)")
    if limit and total > limit:
        print(f"   Showing first {display_count} results\n")
    else:
        print()

    for i, entry in enumerate(results[:display_count], 1):
        if compact:
            print(format_entry(entry, compact=True))
        else:
            print(format_entry(entry, compact=False))
            if i < display_count:
                print()


def display_summary(oracle_path):
    """Display summary of knowledge base."""
    index_path = oracle_path / 'index.json'

    if not index_path.exists():
        print("[WARNING]  No index found. Knowledge base may be empty.")
        return

    with open(index_path, 'r') as f:
        index = json.load(f)

    print("="*70)
    print("[INFO] Oracle Knowledge Base Summary")
    print("="*70)
    print(f"\nCreated: {index.get('created', 'Unknown')}")
    print(f"Last Updated: {index.get('last_updated', 'Unknown')}")
    print(f"Total Entries: {index.get('total_entries', 0)}")

    print("\nEntries by Category:")
    for category, count in index.get('categories', {}).items():
        print(f"   {category.capitalize()}: {count}")

    print(f"\nSessions Recorded: {len(index.get('sessions', []))}")
    print("="*70)


def main():
    parser = argparse.ArgumentParser(
        description='Query Oracle knowledge base',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python query_knowledge.py "authentication"
  python query_knowledge.py --category patterns
  python query_knowledge.py --priority critical
  python query_knowledge.py --tags api,database
  python query_knowledge.py --recent 5
  python query_knowledge.py --summary
        """
    )

    parser.add_argument(
        'query',
        nargs='?',
        help='Search query (searches title, content, context)'
    )

    parser.add_argument(
        '--category',
        choices=['patterns', 'preferences', 'gotchas', 'solutions', 'corrections'],
        help='Filter by category'
    )

    parser.add_argument(
        '--priority',
        choices=['critical', 'high', 'medium', 'low'],
        help='Filter by priority'
    )

    parser.add_argument(
        '--tags',
        help='Filter by tags (comma-separated)'
    )

    parser.add_argument(
        '--sort',
        choices=['priority', 'recent', 'used'],
        default='priority',
        help='Sort results by (default: priority)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of results'
    )

    parser.add_argument(
        '--recent',
        type=int,
        metavar='N',
        help='Show N most recent entries'
    )

    parser.add_argument(
        '--compact',
        action='store_true',
        help='Display compact results'
    )

    parser.add_argument(
        '--summary',
        action='store_true',
        help='Display knowledge base summary'
    )

    args = parser.parse_args()

    # Find Oracle directory
    oracle_path = find_oracle_root()

    if not oracle_path:
        print("[ERROR] Error: .oracle directory not found.")
        print("   Run: python .claude/skills/oracle/scripts/init_oracle.py")
        sys.exit(1)

    # Display summary if requested
    if args.summary:
        display_summary(oracle_path)
        sys.exit(0)

    # Load knowledge
    knowledge = load_knowledge(oracle_path, args.category)

    if not knowledge:
        print("[ERROR] No knowledge entries found.")
        print("   Start recording sessions to build the knowledge base.")
        sys.exit(0)

    # Search and filter
    results = search_knowledge(knowledge, args.query, args.priority, args.tags)

    # Sort
    if args.recent:
        results = sort_knowledge(results, 'recent')
        limit = args.recent
    else:
        results = sort_knowledge(results, args.sort)
        limit = args.limit

    # Display
    display_results(results, args.compact, limit)


if __name__ == '__main__':
    main()
