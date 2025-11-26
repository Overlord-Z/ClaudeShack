#!/usr/bin/env python3
"""
Smart Context Generator for Oracle

Enhances context generation by analyzing:
- Current git status (files changed, branch name)
- File patterns and paths in knowledge tags
- Time-decay for older knowledge
- Relevance scoring based on current work

Usage:
    python smart_context.py [--format text|json] [--max-length 5000]

This can be used standalone or integrated into generate_context.py

Examples:
    python smart_context.py
    python smart_context.py --format json --max-length 10000
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
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


def get_git_status() -> Dict[str, Any]:
    """Get current git status information.

    Returns:
        Dictionary with git status information
    """
    git_info = {
        'branch': None,
        'modified_files': [],
        'staged_files': [],
        'untracked_files': [],
        'is_repo': False
    }

    try:
        # Check if we're in a git repo
        subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            check=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        git_info['is_repo'] = True

        # Get current branch
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            check=False,
            timeout=5
        )
        if result.returncode == 0:
            git_info['branch'] = result.stdout.strip()

        # Get modified files
        result = subprocess.run(
            ['git', 'diff', '--name-only'],
            capture_output=True,
            text=True,
            check=False,
            timeout=5
        )
        if result.returncode == 0:
            git_info['modified_files'] = [f.strip() for f in result.stdout.split('\n') if f.strip()]

        # Get staged files
        result = subprocess.run(
            ['git', 'diff', '--staged', '--name-only'],
            capture_output=True,
            text=True,
            check=False,
            timeout=5
        )
        if result.returncode == 0:
            git_info['staged_files'] = [f.strip() for f in result.stdout.split('\n') if f.strip()]

        # Get untracked files
        result = subprocess.run(
            ['git', 'ls-files', '--others', '--exclude-standard'],
            capture_output=True,
            text=True,
            check=False,
            timeout=5
        )
        if result.returncode == 0:
            git_info['untracked_files'] = [f.strip() for f in result.stdout.split('\n') if f.strip()]

    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        # Not a git repo, git not available, or git command timed out
        pass

    return git_info


def extract_file_patterns(files: List[str]) -> List[str]:
    """Extract patterns from file paths for matching knowledge.

    Args:
        files: List of file paths

    Returns:
        List of patterns (file types, directory names, etc.)
    """
    patterns = set()

    for file_path in files:
        path = Path(file_path)

        # Add file extension
        if path.suffix:
            patterns.add(path.suffix[1:])  # Remove the dot

        # Add directory components
        for part in path.parts[:-1]:  # Exclude filename
            if part and part != '.':
                patterns.add(part)

        # Add filename without extension
        stem = path.stem
        if stem:
            patterns.add(stem)

    return list(patterns)


def load_all_knowledge(oracle_path: Path) -> List[Dict[str, Any]]:
    """Load all knowledge from Oracle.

    Args:
        oracle_path: Path to .oracle directory

    Returns:
        List of knowledge entries
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
            except json.JSONDecodeError as e:
                # Log parsing errors for debugging
                print(f"Warning: Failed to parse {file_path}: {e}", file=sys.stderr)
                continue
            except (FileNotFoundError, OSError, IOError) as e:
                # Log file access errors
                print(f"Warning: Cannot read {file_path}: {e}", file=sys.stderr)
                continue

    return all_knowledge


def calculate_time_decay_score(created_date: str, days_half_life: int = 30) -> float:
    """Calculate time decay score for knowledge based on age.

    Args:
        created_date: ISO format date string
        days_half_life: Number of days for score to decay to 0.5 (must be positive)

    Returns:
        Score between 0 and 1 (1 = created today, decays over time)

    Raises:
        ValueError: If days_half_life is not positive
    """
    if days_half_life <= 0:
        raise ValueError(f"days_half_life must be positive, got {days_half_life}")

    try:
        created = datetime.fromisoformat(created_date)
        # Use UTC time if available, otherwise use local time
        now = datetime.now(created.tzinfo) if created.tzinfo else datetime.now()

        # Use total_seconds for precise calculation (includes hours/minutes)
        age_seconds = (now - created).total_seconds()
        age_days = age_seconds / (24 * 3600)  # Convert to days with decimals

        # Exponential decay: score = 0.5 ^ (days_old / half_life)
        score = 0.5 ** (age_days / days_half_life)
        return max(0.0, min(1.0, score))

    except (ValueError, TypeError):
        # If date parsing fails, return neutral score
        return 0.5


def calculate_relevance_score(
    entry: Dict[str, Any],
    file_patterns: List[str],
    branch: Optional[str] = None
) -> float:
    """Calculate relevance score for a knowledge entry.

    Args:
        entry: Knowledge entry dictionary
        file_patterns: List of file patterns from current work
        branch: Current git branch name

    Returns:
        Relevance score (0.0 to 1.0)
    """
    score = 0.0

    # Base score from priority
    priority_scores = {
        'critical': 1.0,
        'high': 0.8,
        'medium': 0.5,
        'low': 0.2
    }
    priority = entry.get('priority', 'medium')
    score += priority_scores.get(priority, 0.5) * 0.3  # 30% weight to priority

    # Score from tag matches - FIXED: protect against empty file_patterns
    tags = entry.get('tags', [])
    if tags and file_patterns:
        # Check how many patterns match tags (using word boundary matching)
        matches = sum(1 for pattern in file_patterns
                     if any(re.search(r'\b' + re.escape(pattern.lower()) + r'\b', tag.lower())
                           for tag in tags))
        tag_score = matches / len(file_patterns)  # Safe: len(file_patterns) > 0
        score += min(1.0, tag_score) * 0.4  # 40% weight to tag matching

    # Score from content/title keyword matching - FIXED: protect against empty file_patterns
    if file_patterns:
        content = f"{entry.get('title', '')} {entry.get('content', '')} {entry.get('context', '')}".lower()
        # Use word boundary matching to avoid false positives
        keyword_matches = sum(1 for pattern in file_patterns
                            if re.search(r'\b' + re.escape(pattern.lower()) + r'\b', content))
        keyword_score = keyword_matches / len(file_patterns)  # Safe: len(file_patterns) > 0
        score += min(1.0, keyword_score) * 0.2  # 20% weight to keyword matching

    # Score from time decay
    created = entry.get('created', '')
    time_score = calculate_time_decay_score(created)
    score += time_score * 0.1  # 10% weight to recency

    return min(1.0, score)


def score_and_rank_knowledge(
    knowledge: List[Dict[str, Any]],
    git_info: Dict[str, Any]
) -> List[Tuple[Dict[str, Any], float]]:
    """Score and rank knowledge entries by relevance.

    Args:
        knowledge: List of knowledge entries
        git_info: Git status information

    Returns:
        List of tuples (entry, score) sorted by score descending
    """
    # Extract file patterns from all changed files
    all_files = (
        git_info['modified_files'] +
        git_info['staged_files'] +
        git_info['untracked_files']
    )
    file_patterns = extract_file_patterns(all_files)

    # Score each entry
    scored_entries = []
    for entry in knowledge:
        score = calculate_relevance_score(entry, file_patterns, git_info.get('branch'))
        scored_entries.append((entry, score))

    # Sort by score descending
    scored_entries.sort(key=lambda x: x[1], reverse=True)

    return scored_entries


def generate_smart_context(
    oracle_path: Path,
    max_length: int = 5000,
    min_score: float = 0.3
) -> str:
    """Generate smart context based on current git status.

    Args:
        oracle_path: Path to .oracle directory
        max_length: Maximum context length (must be > 0)
        min_score: Minimum relevance score to include (0.0-1.0)

    Returns:
        Formatted context string

    Raises:
        ValueError: If parameters are invalid
    """
    # Validate parameters
    if not 0.0 <= min_score <= 1.0:
        raise ValueError(f"min_score must be in [0.0, 1.0], got {min_score}")
    if max_length <= 0:
        raise ValueError(f"max_length must be positive, got {max_length}")
    # Get git status
    git_info = get_git_status()

    # Load all knowledge
    knowledge = load_all_knowledge(oracle_path)

    if not knowledge:
        return "Oracle: No knowledge base found."

    # Score and rank knowledge
    scored_knowledge = score_and_rank_knowledge(knowledge, git_info)

    # Filter by minimum score
    relevant_knowledge = [(entry, score) for entry, score in scored_knowledge if score >= min_score]

    # Build context
    lines = []

    lines.append("# Oracle Smart Context")
    lines.append("")

    # Add git status if available
    if git_info['is_repo']:
        lines.append("## Current Work Context")
        if git_info['branch']:
            lines.append(f"Branch: `{git_info['branch']}`")

        total_files = len(git_info['modified_files']) + len(git_info['staged_files'])
        if total_files > 0:
            lines.append(f"Files being worked on: {total_files}")

        lines.append("")

    # Add relevant knowledge
    if relevant_knowledge:
        lines.append("## Relevant Knowledge")
        lines.append("")

        # Group by category
        by_category: Dict[str, List[Tuple[Dict[str, Any], float]]] = {}
        for entry, score in relevant_knowledge[:20]:  # Top 20
            category = entry['_category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append((entry, score))

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

            for entry, score in items[:10]:  # Top 10 per category
                priority = entry.get('priority', 'medium')
                title = entry.get('title', 'Untitled')
                content = entry.get('content', '')

                # Format based on priority and score
                if priority == 'critical' or score >= 0.8:
                    lines.append(f"- **[{score:.1f}] {title}**")
                else:
                    lines.append(f"- [{score:.1f}] {title}")

                # Add content if it's brief
                if content and len(content) < 200:
                    lines.append(f"  {content}")

                # Add tags if they matched
                tags = entry.get('tags', [])
                if tags:
                    lines.append(f"  *Tags: {', '.join(tags[:5])}*")

                lines.append("")

    else:
        lines.append("No highly relevant knowledge found for current work.")
        lines.append("")
        lines.append("Showing high-priority items:")
        lines.append("")

        # Fall back to high-priority items
        high_priority = [e for e in knowledge if e.get('priority') in ['critical', 'high']]
        for entry in high_priority[:10]:
            title = entry.get('title', 'Untitled')
            lines.append(f"- {title}")

        lines.append("")

    # Combine and truncate if needed
    full_context = "\n".join(lines)

    if len(full_context) > max_length:
        truncated = full_context[:max_length]
        # Find last newline to avoid breaking mid-line
        last_newline = truncated.rfind('\n')
        if last_newline != -1:
            truncated = truncated[:last_newline]
        truncated += f"\n\n*[Context truncated to {max_length} chars]*"
        return truncated

    return full_context


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate smart context from Oracle knowledge',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (text or json)'
    )

    parser.add_argument(
        '--max-length',
        type=int,
        default=5000,
        help='Maximum context length'
    )

    parser.add_argument(
        '--min-score',
        type=float,
        default=0.3,
        help='Minimum relevance score (0.0-1.0)'
    )

    args = parser.parse_args()

    # Find Oracle
    oracle_path = find_oracle_root()

    if not oracle_path:
        if args.format == 'json':
            print(json.dumps({'error': 'Oracle not initialized'}))
        else:
            print("[ERROR] .oracle directory not found.")
        sys.exit(1)

    # Generate context
    try:
        context = generate_smart_context(oracle_path, args.max_length, args.min_score)

        if args.format == 'json':
            output = {
                'context': context,
                'git_status': get_git_status()
            }
            print(json.dumps(output, indent=2))
        else:
            print(context)

    except Exception as e:
        if args.format == 'json':
            print(json.dumps({'error': str(e)}))
        else:
            print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
