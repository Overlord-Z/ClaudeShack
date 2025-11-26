#!/usr/bin/env python3
"""
Guardian Context Filter

Extracts MINIMAL context for subagent tasks - following the key principle:
"Caller should only pass exactly what is needed for the task so it can be laser focused."

This script NEVER passes full conversation history. It extracts only:
- Specific files being reviewed
- Relevant Oracle patterns (max 5)
- Recent corrections in the same area (max 3)
- A focused task description

Usage:
    # Extract context for code review
    python context_filter.py --task review --file auth.py --focus security

    # Extract context for planning
    python context_filter.py --task plan --description "Build REST API with auth"

    # Extract context for debugging
    python context_filter.py --task debug --file app.py --error "TypeError: cannot unpack"

Environment Variables:
    ORACLE_PATH: Path to Oracle directory [default: .oracle]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
import re


def find_oracle_root() -> Optional[Path]:
    """Find the .oracle directory."""
    current = Path.cwd()

    while current != current.parent:
        oracle_path = current / '.oracle'
        if oracle_path.exists():
            return oracle_path
        current = current.parent

    return None


def load_oracle_knowledge(oracle_path: Path, categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Load Oracle knowledge from specified categories.

    Args:
        oracle_path: Path to .oracle directory
        categories: List of categories to load (defaults to all)

    Returns:
        List of knowledge entries
    """
    knowledge_dir = oracle_path / 'knowledge'
    all_knowledge: List[Dict[str, Any]] = []

    if categories is None:
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
                continue

    return all_knowledge


def extract_file_patterns(file_path: str) -> List[str]:
    """Extract patterns from a file path for matching Oracle knowledge.

    Args:
        file_path: Path to the file

    Returns:
        List of patterns (extension, directory names, filename)
    """
    patterns = []
    path = Path(file_path)

    # Add file extension
    if path.suffix:
        patterns.append(path.suffix[1:])  # Remove dot

    # Add filename without extension
    if path.stem:
        patterns.append(path.stem)

    # Add directory components
    for part in path.parts[:-1]:
        if part and part != '.' and part != '..':
            patterns.append(part)

    return patterns


def find_relevant_patterns(
    oracle_knowledge: List[Dict[str, Any]],
    file_patterns: List[str],
    focus_keywords: Optional[List[str]] = None,
    max_patterns: int = 5
) -> List[Dict[str, Any]]:
    """Find relevant Oracle patterns for the context.

    Args:
        oracle_knowledge: All Oracle knowledge
        file_patterns: Patterns extracted from file path
        focus_keywords: Optional focus keywords (e.g., "security", "performance")
        max_patterns: Maximum number of patterns to return

    Returns:
        List of relevant pattern entries
    """
    # Filter to patterns category only
    patterns = [k for k in oracle_knowledge if k.get('_category') == 'patterns']

    scored_patterns = []

    for pattern in patterns:
        score = 0.0

        # Priority scoring
        priority = pattern.get('priority', 'medium')
        if priority == 'critical':
            score += 1.0
        elif priority == 'high':
            score += 0.7
        elif priority == 'medium':
            score += 0.4

        # Tag matching
        tags = pattern.get('tags', [])
        if tags and file_patterns:
            matches = sum(1 for fp in file_patterns
                         if any(re.search(r'\b' + re.escape(fp.lower()) + r'\b', tag.lower())
                               for tag in tags))
            score += matches * 0.3

        # Focus keyword matching
        if focus_keywords:
            content = f"{pattern.get('title', '')} {pattern.get('content', '')}".lower()
            keyword_matches = sum(1 for keyword in focus_keywords
                                 if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', content))
            score += keyword_matches * 0.5

        scored_patterns.append((pattern, score))

    # Sort by score descending
    scored_patterns.sort(key=lambda x: x[1], reverse=True)

    # Return top N
    return [pattern for pattern, score in scored_patterns[:max_patterns]]


def find_relevant_gotchas(
    oracle_knowledge: List[Dict[str, Any]],
    file_patterns: List[str],
    focus_keywords: Optional[List[str]] = None,
    max_gotchas: int = 5
) -> List[Dict[str, Any]]:
    """Find relevant Oracle gotchas for the context."""
    gotchas = [k for k in oracle_knowledge if k.get('_category') == 'gotchas']

    scored_gotchas = []

    for gotcha in gotchas:
        score = 0.0

        # Priority scoring (gotchas are critical by nature)
        priority = gotcha.get('priority', 'high')
        if priority == 'critical':
            score += 1.0
        elif priority == 'high':
            score += 0.8

        # Tag matching
        tags = gotcha.get('tags', [])
        if tags and file_patterns:
            matches = sum(1 for fp in file_patterns
                         if any(re.search(r'\b' + re.escape(fp.lower()) + r'\b', tag.lower())
                               for tag in tags))
            score += matches * 0.4

        # Focus keyword matching
        if focus_keywords:
            content = f"{gotcha.get('title', '')} {gotcha.get('content', '')}".lower()
            keyword_matches = sum(1 for keyword in focus_keywords
                                 if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', content))
            score += keyword_matches * 0.6

        scored_gotchas.append((gotcha, score))

    scored_gotchas.sort(key=lambda x: x[1], reverse=True)

    return [gotcha for gotcha, score in scored_gotchas[:max_gotchas]]


def find_recent_corrections(
    oracle_knowledge: List[Dict[str, Any]],
    file_patterns: List[str],
    max_corrections: int = 3
) -> List[Dict[str, Any]]:
    """Find recent relevant corrections from Oracle.

    Args:
        oracle_knowledge: All Oracle knowledge
        file_patterns: Patterns from file path
        max_corrections: Maximum corrections to return

    Returns:
        List of recent relevant corrections
    """
    corrections = [k for k in oracle_knowledge if k.get('_category') == 'corrections']

    # Sort by creation date (most recent first)
    sorted_corrections = sorted(
        corrections,
        key=lambda x: x.get('created', ''),
        reverse=True
    )

    # Filter for relevance
    relevant = []
    for correction in sorted_corrections:
        tags = correction.get('tags', [])
        content = f"{correction.get('title', '')} {correction.get('content', '')}".lower()

        # Check if relevant to current file patterns
        is_relevant = False

        if tags and file_patterns:
            if any(fp.lower() in tag.lower() for fp in file_patterns for tag in tags):
                is_relevant = True

        if file_patterns:
            if any(re.search(r'\b' + re.escape(fp.lower()) + r'\b', content) for fp in file_patterns):
                is_relevant = True

        if is_relevant:
            relevant.append(correction)

        if len(relevant) >= max_corrections:
            break

    return relevant


def build_minimal_context(
    task_type: str,
    file_path: Optional[str] = None,
    focus: Optional[str] = None,
    description: Optional[str] = None,
    error_message: Optional[str] = None,
    oracle_path: Optional[Path] = None
) -> Dict[str, Any]:
    """Build minimal context for subagent task.

    Args:
        task_type: Type of task (review, plan, debug)
        file_path: Optional file path to review
        focus: Optional focus keywords (e.g., "security performance")
        description: Optional task description
        error_message: Optional error message for debugging
        oracle_path: Optional path to Oracle directory

    Returns:
        Minimal context dictionary
    """
    context: Dict[str, Any] = {
        'task': task_type,
        'files': {},
        'oracle_patterns': [],
        'oracle_gotchas': [],
        'recent_corrections': [],
        'focus': ''
    }

    # Parse focus keywords
    focus_keywords = focus.split() if focus else []

    # Extract file patterns
    file_patterns = extract_file_patterns(file_path) if file_path else []

    # Load file content if provided (with size limit to avoid memory exhaustion)
    MAX_FILE_SIZE = 1024 * 1024  # 1MB limit
    if file_path:
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                file_size = path.stat().st_size
                if file_size > MAX_FILE_SIZE:
                    context['files'][file_path] = f"[File too large: {file_size} bytes. Showing first 1MB only]\n"
                    with open(path, 'r', encoding='utf-8') as f:
                        # Read only first 1MB
                        context['files'][file_path] += f.read(MAX_FILE_SIZE)
                else:
                    with open(path, 'r', encoding='utf-8') as f:
                        context['files'][file_path] = f.read()
        except (OSError, IOError, UnicodeDecodeError) as e:
            context['files'][file_path] = "[Error: Could not read file]"

    # Load Oracle knowledge if available
    if oracle_path:
        oracle_knowledge = load_oracle_knowledge(oracle_path)

        # Find relevant patterns
        context['oracle_patterns'] = find_relevant_patterns(
            oracle_knowledge,
            file_patterns,
            focus_keywords,
            max_patterns=5
        )

        # Find relevant gotchas
        context['oracle_gotchas'] = find_relevant_gotchas(
            oracle_knowledge,
            file_patterns,
            focus_keywords,
            max_gotchas=5
        )

        # Find recent corrections
        context['recent_corrections'] = find_recent_corrections(
            oracle_knowledge,
            file_patterns,
            max_corrections=3
        )

    # Build focus description
    if task_type == 'review':
        if focus:
            context['focus'] = f"Review {file_path or 'code'} for {focus} issues"
        else:
            context['focus'] = f"Review {file_path or 'code'} for potential issues"

    elif task_type == 'plan':
        context['focus'] = f"Break down this task into subtasks: {description or 'Complex task'}"

    elif task_type == 'debug':
        context['focus'] = f"Debug error in {file_path or 'code'}: {error_message or 'Unknown error'}"
        if error_message:
            context['error'] = error_message

    return context


def format_context_for_agent(context: Dict[str, Any], format_type: str = 'text') -> str:
    """Format context for subagent consumption.

    Args:
        context: Minimal context dictionary
        format_type: Output format (text or json)

    Returns:
        Formatted context string
    """
    if format_type == 'json':
        return json.dumps(context, indent=2)

    # Text format
    lines = []

    lines.append(f"# Task: {context['task'].capitalize()}")
    lines.append("")
    lines.append(f"**Focus**: {context['focus']}")
    lines.append("")

    # Files
    if context['files']:
        lines.append("## Files to Review")
        lines.append("")
        for file_path, content in context['files'].items():
            lines.append(f"### {file_path}")
            lines.append("")
            lines.append("```")
            lines.append(content[:5000])  # Limit file size
            if len(content) > 5000:
                lines.append("... [truncated]")
            lines.append("```")
            lines.append("")

    # Oracle patterns
    if context['oracle_patterns']:
        lines.append("## Relevant Patterns (from Oracle)")
        lines.append("")
        for pattern in context['oracle_patterns']:
            title = pattern.get('title', 'Untitled')
            content = pattern.get('content', '')
            lines.append(f"- **{title}**")
            if content:
                lines.append(f"  {content[:200]}")
        lines.append("")

    # Oracle gotchas
    if context['oracle_gotchas']:
        lines.append("## Gotchas to Watch For (from Oracle)")
        lines.append("")
        for gotcha in context['oracle_gotchas']:
            title = gotcha.get('title', 'Untitled')
            content = gotcha.get('content', '')
            priority = gotcha.get('priority', 'medium')
            if priority == 'critical':
                lines.append(f"- **[CRITICAL]** {title}")
            else:
                lines.append(f"- {title}")
            if content:
                lines.append(f"  {content[:200]}")
        lines.append("")

    # Recent corrections
    if context['recent_corrections']:
        lines.append("## Recent Corrections (from Oracle)")
        lines.append("")
        for correction in context['recent_corrections']:
            content = correction.get('content', '')
            title = correction.get('title', 'Correction')

            # Try to extract the "Right:" part
            if 'Right:' in content:
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

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Extract minimal context for Guardian subagent tasks',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--task',
        required=True,
        choices=['review', 'plan', 'debug'],
        help='Type of task'
    )

    parser.add_argument(
        '--file',
        help='File path to review/debug'
    )

    parser.add_argument(
        '--focus',
        help='Focus keywords (e.g., "security performance")'
    )

    parser.add_argument(
        '--description',
        help='Task description (for planning tasks)'
    )

    parser.add_argument(
        '--error',
        help='Error message (for debugging tasks)'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format'
    )

    parser.add_argument(
        '--no-oracle',
        action='store_true',
        help='Skip Oracle knowledge loading'
    )

    args = parser.parse_args()

    # Validate arguments based on task type
    if args.task == 'review' and not args.file:
        print("Error: --file required for review tasks", file=sys.stderr)
        sys.exit(1)

    if args.task == 'plan' and not args.description:
        print("Error: --description required for planning tasks", file=sys.stderr)
        sys.exit(1)

    if args.task == 'debug' and not args.file:
        print("Error: --file required for debug tasks", file=sys.stderr)
        sys.exit(1)

    # Find Oracle
    oracle_path = None
    if not args.no_oracle:
        oracle_path = find_oracle_root()

    # Build minimal context
    context = build_minimal_context(
        task_type=args.task,
        file_path=args.file,
        focus=args.focus,
        description=args.description,
        error_message=args.error,
        oracle_path=oracle_path
    )

    # Format and output
    output = format_context_for_agent(context, args.format)
    print(output)


if __name__ == '__main__':
    main()
