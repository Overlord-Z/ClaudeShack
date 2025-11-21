#!/usr/bin/env python3
"""
Oracle SessionStart Hook

Automatically loads Oracle context when a Claude Code session starts or resumes.
This script is designed to be called by Claude Code's SessionStart hook system.

The script outputs JSON with hookSpecificOutput.additionalContext containing
relevant Oracle knowledge for the session.

Usage:
    python session_start_hook.py [--session-id SESSION_ID] [--source SOURCE]

Hook Configuration (add to Claude Code settings):
    {
      "hooks": {
        "SessionStart": [
          {
            "matcher": "startup",
            "hooks": [
              {
                "type": "command",
                "command": "python /path/to/oracle/Scripts/session_start_hook.py"
              }
            ]
          }
        ]
      }
    }

Environment Variables:
    ORACLE_CONTEXT_TIER: Context tier level (1=critical, 2=medium, 3=all) [default: 1]
    ORACLE_MAX_CONTEXT_LENGTH: Maximum context length in characters [default: 5000]
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any


def find_oracle_root() -> Optional[Path]:
    """Find the .oracle directory by walking up from current directory."""
    current = Path.cwd()

    while current != current.parent:
        oracle_path = current / '.oracle'
        if oracle_path.exists():
            return oracle_path
        current = current.parent

    return None


def load_all_knowledge(oracle_path: Path) -> List[Dict[str, Any]]:
    """Load all knowledge from Oracle.

    Args:
        oracle_path: Path to the .oracle directory

    Returns:
        List of knowledge entries with _category field added
    """
    knowledge_dir = oracle_path / 'knowledge'
    all_knowledge: List[Dict[str, Any]] = []

    categories = ['patterns', 'preferences', 'gotchas', 'solutions', 'corrections']

    for category in categories:
        file_path = knowledge_dir / f'{category}.json'
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    entries = json.load(f)
                    for entry in entries:
                        if isinstance(entry, dict):
                            entry['_category'] = category
                            all_knowledge.append(entry)
            except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
                # Skip corrupted or inaccessible files
                continue

    return all_knowledge


def filter_by_tier(knowledge: List[Dict[str, Any]], tier: int = 1) -> List[Dict[str, Any]]:
    """Filter knowledge by tier level.

    Args:
        knowledge: List of knowledge entries
        tier: Tier level (1=critical/high, 2=include medium, 3=all)

    Returns:
        Filtered knowledge entries
    """
    if tier == 1:
        # Critical and high priority - always load
        return [k for k in knowledge if k.get('priority') in ['critical', 'high']]
    elif tier == 2:
        # Include medium priority
        return [k for k in knowledge if k.get('priority') in ['critical', 'high', 'medium']]
    else:
        # All knowledge
        return knowledge


def get_recent_corrections(oracle_path: Path, limit: int = 5) -> List[Dict[str, Any]]:
    """Get most recent corrections.

    Args:
        oracle_path: Path to the .oracle directory
        limit: Maximum number of corrections to return

    Returns:
        List of recent correction entries
    """
    knowledge_dir = oracle_path / 'knowledge'
    corrections_file = knowledge_dir / 'corrections.json'

    if not corrections_file.exists():
        return []

    try:
        with open(corrections_file, 'r', encoding='utf-8') as f:
            corrections = json.load(f)

        # Sort by creation date (safely handle missing 'created' field)
        sorted_corrections = sorted(
            corrections,
            key=lambda x: x.get('created', ''),
            reverse=True
        )

        return sorted_corrections[:limit]
    except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
        return []


def get_project_stats(oracle_path: Path) -> Optional[Dict[str, Any]]:
    """Get project statistics from index.

    Args:
        oracle_path: Path to the .oracle directory

    Returns:
        Index data dictionary or None if unavailable
    """
    index_file = oracle_path / 'index.json'

    if not index_file.exists():
        return None

    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
        return index
    except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
        return None


# Configuration constants
MAX_KEY_KNOWLEDGE_ITEMS = 15  # Limit before truncation
MAX_ITEMS_PER_CATEGORY = 5    # How many to show per category
RECENT_CORRECTIONS_LIMIT = 3  # How many recent corrections to show
CONTENT_LENGTH_THRESHOLD = 200  # Min content length to display


def generate_context(oracle_path: Path, tier: int = 1, max_length: int = 5000) -> str:
    """Generate context summary for session start.

    Args:
        oracle_path: Path to the .oracle directory
        tier: Context tier level (1=critical, 2=medium, 3=all)
        max_length: Maximum context length in characters

    Returns:
        Formatted context string ready for injection
    """
    knowledge = load_all_knowledge(oracle_path)

    if not knowledge:
        return "Oracle: No knowledge base found. Start recording sessions to build project knowledge."

    # Filter by tier
    relevant_knowledge = filter_by_tier(knowledge, tier)

    # Get recent corrections
    recent_corrections = get_recent_corrections(oracle_path, limit=RECENT_CORRECTIONS_LIMIT)

    # Get stats
    stats = get_project_stats(oracle_path)

    # Build context
    lines = []

    lines.append("# Oracle Project Knowledge")
    lines.append("")

    # Add stats if available
    if stats:
        total_entries = stats.get('total_entries', 0)
        sessions = len(stats.get('sessions', []))
        if total_entries > 0 or sessions > 0:
            lines.append(f"Knowledge Base: {total_entries} entries | {sessions} sessions recorded")
            lines.append("")

    # Add critical/high priority knowledge
    if relevant_knowledge:
        lines.append("## Key Knowledge")
        lines.append("")

        # Group by category
        by_category: Dict[str, List[Dict[str, Any]]] = {}
        for item in relevant_knowledge[:MAX_KEY_KNOWLEDGE_ITEMS]:
            category = item['_category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(item)

        # Category labels
        category_labels = {
            'patterns': 'Patterns',
            'preferences': 'Preferences',
            'gotchas': 'Gotchas (Watch Out!)',
            'solutions': 'Solutions',
            'corrections': 'Corrections'
        }

        for category, items in by_category.items():
            label = category_labels.get(category, category.capitalize())
            lines.append(f"### {label}")
            lines.append("")

            for item in items[:MAX_ITEMS_PER_CATEGORY]:
                priority = item.get('priority', 'medium')
                title = item.get('title', 'Untitled')
                content = item.get('content', '')

                # Compact format
                if priority == 'critical':
                    lines.append(f"- **[CRITICAL]** {title}")
                elif priority == 'high':
                    lines.append(f"- **{title}**")
                else:
                    lines.append(f"- {title}")

                # Add brief content if it fits
                if content and len(content) < CONTENT_LENGTH_THRESHOLD:
                    lines.append(f"  {content}")

                lines.append("")

    # Add recent corrections
    if recent_corrections:
        lines.append("## Recent Corrections")
        lines.append("")

        for correction in recent_corrections:
            content = correction.get('content', '')
            title = correction.get('title', 'Correction')

            # Try to extract the "right" part if available
            if content and 'Right:' in content:
                try:
                    right_part = content.split('Right:', 1)[1].split('\n', 1)[0].strip()
                    if right_part:
                        lines.append(f"- {right_part}")
                    else:
                        lines.append(f"- {title}")
                except (IndexError, ValueError, AttributeError):
                    lines.append(f"- {title}")
            else:
                lines.append(f"- {title}")

        lines.append("")

    # Combine and truncate if needed
    full_context = "\n".join(lines)

    if len(full_context) > max_length:
        # Truncate and add note
        truncated = full_context[:max_length].rsplit('\n', 1)[0]
        truncated += f"\n\n*[Context truncated to {max_length} chars. Use /oracle skill for full knowledge base]*"
        return truncated

    return full_context


def output_hook_result(context: str, session_id: Optional[str] = None, source: Optional[str] = None) -> None:
    """Output result in Claude Code hook format.

    Args:
        context: Context string to inject
        session_id: Optional session ID
        source: Optional session source (startup/resume/clear)
    """
    result = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context
        }
    }

    # Add metadata if available
    if session_id:
        result["hookSpecificOutput"]["sessionId"] = session_id
    if source:
        result["hookSpecificOutput"]["source"] = source

    # Output as JSON
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description='Oracle SessionStart hook for Claude Code',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--session-id',
        help='Session ID (passed by Claude Code)'
    )

    parser.add_argument(
        '--source',
        help='Session source: startup, resume, or clear'
    )

    parser.add_argument(
        '--tier',
        type=int,
        choices=[1, 2, 3],
        help='Context tier level (1=critical, 2=medium, 3=all)'
    )

    parser.add_argument(
        '--max-length',
        type=int,
        help='Maximum context length in characters'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Debug mode - output to stderr instead of JSON'
    )

    args = parser.parse_args()

    # Find Oracle
    oracle_path = find_oracle_root()

    if not oracle_path:
        # No Oracle found - output minimal context
        if args.debug:
            print("Oracle not initialized for this project", file=sys.stderr)
        else:
            # Get path to init script relative to this script
            script_dir = Path(__file__).parent
            init_script_path = script_dir / 'init_oracle.py'

            output_hook_result(
                f"Oracle: Not initialized. Run `python {init_script_path}` to set up project knowledge tracking.",
                args.session_id,
                args.source
            )
        sys.exit(0)

    # Get configuration from environment or arguments
    tier = args.tier or int(os.getenv('ORACLE_CONTEXT_TIER', '1'))
    max_length = args.max_length or int(os.getenv('ORACLE_MAX_CONTEXT_LENGTH', '5000'))

    # Generate context
    try:
        context = generate_context(oracle_path, tier, max_length)

        if args.debug:
            print(context, file=sys.stderr)
        else:
            output_hook_result(context, args.session_id, args.source)

    except Exception as e:
        if args.debug:
            print(f"Error generating context: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
        else:
            # Don't expose internal error details to user
            output_hook_result(
                "Oracle: Error loading context. Use /oracle skill to query knowledge manually.",
                args.session_id,
                args.source
            )
        sys.exit(1)


if __name__ == '__main__':
    main()
