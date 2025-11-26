#!/usr/bin/env python3
"""
Guardian Suggestion Validator

Cross-checks subagent suggestions against Oracle knowledge before presenting to user.

Key Principle: "Subagent might be missing important codebase context - need validation layer"

This script:
1. Validates suggestions against Oracle patterns
2. Detects contradictions with known good practices
3. Checks rejection history for similar suggestions
4. Calculates confidence scores
5. Flags suggestions that contradict Oracle knowledge

Usage:
    # Validate a single suggestion
    python validator.py --suggestion "Use MD5 for password hashing" --category security

    # Validate multiple suggestions from JSON
    python validator.py --suggestions-file suggestions.json

    # Check rejection history
    python validator.py --check-rejection "Add rate limiting to endpoint"

Environment Variables:
    ORACLE_PATH: Path to Oracle directory [default: .oracle]
    GUARDIAN_PATH: Path to Guardian directory [default: .guardian]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import re
from datetime import datetime, timedelta


def find_oracle_root() -> Optional[Path]:
    """Find the .oracle directory."""
    current = Path.cwd()

    while current != current.parent:
        oracle_path = current / '.oracle'
        if oracle_path.exists():
            return oracle_path
        current = current.parent

    return None


def find_guardian_root() -> Optional[Path]:
    """Find the .guardian directory."""
    current = Path.cwd()

    while current != current.parent:
        guardian_path = current / '.guardian'
        if guardian_path.exists():
            return guardian_path
        current = current.parent

    return None


def load_oracle_knowledge(oracle_path: Path) -> List[Dict[str, Any]]:
    """Load all Oracle knowledge."""
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
                continue

    return all_knowledge


def load_rejection_history(guardian_path: Path) -> List[Dict[str, Any]]:
    """Load rejection history from Guardian."""
    history_file = guardian_path / 'rejection_history.json'

    if not history_file.exists():
        return []

    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
        return []


def save_rejection_history(guardian_path: Path, history: List[Dict[str, Any]]) -> None:
    """Save rejection history to Guardian."""
    history_file = guardian_path / 'rejection_history.json'

    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    except (OSError, IOError) as e:
        print(f"Warning: Failed to save rejection history: {e}", file=sys.stderr)


def load_acceptance_stats(guardian_path: Path) -> Dict[str, Any]:
    """Load acceptance rate statistics."""
    stats_file = guardian_path / 'acceptance_stats.json'

    if not stats_file.exists():
        return {
            'by_category': {},
            'by_type': {},
            'overall': {
                'accepted': 0,
                'rejected': 0,
                'rate': 0.0
            }
        }

    try:
        with open(stats_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
        return {'by_category': {}, 'by_type': {}, 'overall': {'accepted': 0, 'rejected': 0, 'rate': 0.0}}


def check_contradiction_with_patterns(
    suggestion: str,
    oracle_knowledge: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Check if suggestion contradicts known Oracle patterns.

    Args:
        suggestion: Suggestion text
        oracle_knowledge: All Oracle knowledge

    Returns:
        Contradiction details if found, None otherwise
    """
    # Get patterns and gotchas
    patterns = [k for k in oracle_knowledge if k.get('_category') == 'patterns']
    gotchas = [k for k in oracle_knowledge if k.get('_category') == 'gotchas']

    suggestion_lower = suggestion.lower()

    # Check against patterns (high priority ones)
    for pattern in patterns:
        if pattern.get('priority') not in ['critical', 'high']:
            continue

        title = pattern.get('title', '').lower()
        content = pattern.get('content', '').lower()

        # Look for direct contradictions
        # Example: suggestion says "use MD5" but pattern says "never use MD5"
        if 'never' in content or 'don\'t' in content or 'avoid' in content:
            # Extract what not to do
            words = re.findall(r'\b\w+\b', suggestion_lower)
            for word in words:
                if len(word) > 3 and word in content:
                    # Potential contradiction
                    return {
                        'type': 'pattern_contradiction',
                        'pattern': pattern.get('title', 'Unknown pattern'),
                        'pattern_content': pattern.get('content', ''),
                        'priority': pattern.get('priority', 'medium'),
                        'confidence': 0.8
                    }

    # Check against gotchas (critical warnings)
    for gotcha in gotchas:
        title = gotcha.get('title', '').lower()
        content = gotcha.get('content', '').lower()

        # Check if suggestion relates to a known gotcha
        words = re.findall(r'\b\w+\b', suggestion_lower)
        common_words = set(words) & set(re.findall(r'\b\w+\b', content))

        if len(common_words) > 3:
            return {
                'type': 'gotcha_warning',
                'gotcha': gotcha.get('title', 'Unknown gotcha'),
                'gotcha_content': gotcha.get('content', ''),
                'priority': gotcha.get('priority', 'high'),
                'confidence': 0.6
            }

    return None


def check_rejection_history(
    suggestion: str,
    rejection_history: List[Dict[str, Any]],
    similarity_threshold: float = 0.6
) -> Optional[Dict[str, Any]]:
    """Check if similar suggestion was previously rejected.

    Args:
        suggestion: Suggestion text
        rejection_history: List of previously rejected suggestions
        similarity_threshold: Minimum similarity to consider a match

    Returns:
        Rejection details if found, None otherwise
    """
    suggestion_words = set(re.findall(r'\b\w+\b', suggestion.lower()))

    for rejection in rejection_history:
        rejected_text = rejection.get('suggestion', '').lower()
        rejected_words = set(re.findall(r'\b\w+\b', rejected_text))

        # Calculate Jaccard similarity
        if len(suggestion_words) == 0 or len(rejected_words) == 0:
            continue

        intersection = suggestion_words & rejected_words
        union = suggestion_words | rejected_words

        similarity = len(intersection) / len(union) if len(union) > 0 else 0.0

        if similarity >= similarity_threshold:
            return {
                'type': 'previously_rejected',
                'rejected_suggestion': rejection.get('suggestion', ''),
                'rejection_reason': rejection.get('reason', 'No reason provided'),
                'rejected_date': rejection.get('timestamp', 'Unknown'),
                'similarity': similarity,
                'confidence': 0.3  # Low confidence due to previous rejection
            }

    return None


def calculate_acceptance_rate(
    category: str,
    acceptance_stats: Dict[str, Any]
) -> float:
    """Calculate acceptance rate for a category.

    Args:
        category: Suggestion category
        acceptance_stats: Acceptance statistics

    Returns:
        Acceptance rate (0.0 to 1.0)
    """
    by_category = acceptance_stats.get('by_category', {})

    if category not in by_category:
        # No history, return neutral rate
        return 0.5

    stats = by_category[category]
    accepted = stats.get('accepted', 0)
    rejected = stats.get('rejected', 0)
    total = accepted + rejected

    if total == 0:
        return 0.5

    return accepted / total


def validate_suggestion(
    suggestion: str,
    category: str,
    oracle_knowledge: List[Dict[str, Any]],
    rejection_history: List[Dict[str, Any]],
    acceptance_stats: Dict[str, Any]
) -> Dict[str, Any]:
    """Validate a suggestion against Oracle knowledge.

    Args:
        suggestion: Suggestion text
        category: Suggestion category (security, performance, etc.)
        oracle_knowledge: All Oracle knowledge
        rejection_history: Previous rejections
        acceptance_stats: Acceptance rate statistics

    Returns:
        Validation result with confidence score and warnings
    """
    result = {
        'suggestion': suggestion,
        'category': category,
        'confidence': 0.5,  # Start neutral
        'warnings': [],
        'should_present': True,
        'notes': []
    }

    # Check for contradictions with Oracle patterns
    contradiction = check_contradiction_with_patterns(suggestion, oracle_knowledge)
    if contradiction:
        result['confidence'] = contradiction['confidence']
        result['warnings'].append({
            'severity': 'high',
            'type': contradiction['type'],
            'message': f"Contradicts Oracle {contradiction['type']}: {contradiction.get('pattern', contradiction.get('gotcha', 'Unknown'))}",
            'details': contradiction
        })

        if contradiction.get('priority') == 'critical':
            result['should_present'] = False
            result['notes'].append("BLOCKED: Contradicts critical Oracle pattern")

    # Check rejection history
    previous_rejection = check_rejection_history(suggestion, rejection_history)
    if previous_rejection:
        result['confidence'] = min(result['confidence'], previous_rejection['confidence'])
        result['warnings'].append({
            'severity': 'medium',
            'type': 'previously_rejected',
            'message': f"Similar suggestion rejected before ({previous_rejection['similarity']:.0%} similar)",
            'details': previous_rejection
        })
        result['notes'].append(f"Previous rejection reason: {previous_rejection['rejection_reason']}")

    # Calculate confidence from acceptance rate
    acceptance_rate = calculate_acceptance_rate(category, acceptance_stats)

    # Adjust confidence based on historical acceptance
    if not result['warnings']:
        # No warnings, use acceptance rate
        result['confidence'] = acceptance_rate
    else:
        # Has warnings, blend with acceptance rate (60% warning, 40% acceptance)
        result['confidence'] = result['confidence'] * 0.6 + acceptance_rate * 0.4

    # Add acceptance rate note
    result['notes'].append(f"Historical acceptance rate for {category}: {acceptance_rate:.0%}")

    # Final decision on whether to present
    if result['confidence'] < 0.3:
        result['should_present'] = False
        result['notes'].append("Confidence too low - suggestion blocked")

    return result


def validate_multiple_suggestions(
    suggestions: List[Dict[str, str]],
    oracle_path: Optional[Path] = None,
    guardian_path: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """Validate multiple suggestions.

    Args:
        suggestions: List of suggestion dictionaries with 'text' and 'category' keys
        oracle_path: Path to Oracle directory
        guardian_path: Path to Guardian directory

    Returns:
        List of validation results
    """
    # Load Oracle knowledge
    oracle_knowledge = []
    if oracle_path:
        oracle_knowledge = load_oracle_knowledge(oracle_path)

    # Load Guardian data
    rejection_history = []
    acceptance_stats = {'by_category': {}, 'by_type': {}, 'overall': {'accepted': 0, 'rejected': 0, 'rate': 0.0}}

    if guardian_path:
        rejection_history = load_rejection_history(guardian_path)
        acceptance_stats = load_acceptance_stats(guardian_path)

    # Validate each suggestion
    results = []
    for suggestion_dict in suggestions:
        suggestion_text = suggestion_dict.get('text', '')
        category = suggestion_dict.get('category', 'general')

        result = validate_suggestion(
            suggestion_text,
            category,
            oracle_knowledge,
            rejection_history,
            acceptance_stats
        )

        results.append(result)

    return results


def record_rejection(
    guardian_path: Path,
    suggestion: str,
    reason: str,
    category: str
) -> None:
    """Record a rejected suggestion for future reference.

    Args:
        guardian_path: Path to Guardian directory
        suggestion: Rejected suggestion text
        reason: Reason for rejection
        category: Suggestion category
    """
    rejection_history = load_rejection_history(guardian_path)

    rejection_history.append({
        'suggestion': suggestion,
        'reason': reason,
        'category': category,
        'timestamp': datetime.now().isoformat()
    })

    # Keep only last 100 rejections
    if len(rejection_history) > 100:
        rejection_history = rejection_history[-100:]

    save_rejection_history(guardian_path, rejection_history)


def update_acceptance_stats(
    guardian_path: Path,
    category: str,
    accepted: bool
) -> None:
    """Update acceptance rate statistics.

    Args:
        guardian_path: Path to Guardian directory
        category: Suggestion category
        accepted: Whether the suggestion was accepted
    """
    stats_file = guardian_path / 'acceptance_stats.json'
    stats = load_acceptance_stats(guardian_path)

    # Update category stats
    if category not in stats['by_category']:
        stats['by_category'][category] = {'accepted': 0, 'rejected': 0}

    if accepted:
        stats['by_category'][category]['accepted'] += 1
        stats['overall']['accepted'] += 1
    else:
        stats['by_category'][category]['rejected'] += 1
        stats['overall']['rejected'] += 1

    # Recalculate overall rate
    total = stats['overall']['accepted'] + stats['overall']['rejected']
    stats['overall']['rate'] = stats['overall']['accepted'] / total if total > 0 else 0.0

    # Recalculate category rates
    for cat, cat_stats in stats['by_category'].items():
        cat_total = cat_stats['accepted'] + cat_stats['rejected']
        cat_stats['rate'] = cat_stats['accepted'] / cat_total if cat_total > 0 else 0.0

    try:
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
    except (OSError, IOError) as e:
        print(f"Warning: Failed to save acceptance stats: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='Validate Guardian suggestions against Oracle knowledge',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--suggestion',
        help='Single suggestion to validate'
    )

    parser.add_argument(
        '--category',
        default='general',
        help='Suggestion category (security, performance, style, etc.)'
    )

    parser.add_argument(
        '--suggestions-file',
        help='JSON file with multiple suggestions to validate'
    )

    parser.add_argument(
        '--record-rejection',
        help='Record a rejected suggestion'
    )

    parser.add_argument(
        '--rejection-reason',
        help='Reason for rejection (used with --record-rejection)'
    )

    parser.add_argument(
        '--update-stats',
        choices=['accept', 'reject'],
        help='Update acceptance statistics'
    )

    parser.add_argument(
        '--check-rejection',
        help='Check if a suggestion was previously rejected'
    )

    args = parser.parse_args()

    # Find Oracle and Guardian
    oracle_path = find_oracle_root()
    guardian_path = find_guardian_root()

    if not oracle_path and not guardian_path:
        print("Warning: Neither Oracle nor Guardian initialized", file=sys.stderr)

    # Handle check rejection
    if args.check_rejection:
        if not guardian_path:
            print(json.dumps({'found': False, 'message': 'Guardian not initialized'}))
            sys.exit(0)

        rejection_history = load_rejection_history(guardian_path)
        result = check_rejection_history(args.check_rejection, rejection_history)

        if result:
            print(json.dumps({'found': True, 'details': result}, indent=2))
        else:
            print(json.dumps({'found': False}))
        sys.exit(0)

    # Handle record rejection
    if args.record_rejection:
        if not guardian_path:
            print("Error: Guardian not initialized", file=sys.stderr)
            sys.exit(1)

        if not args.rejection_reason:
            print("Error: --rejection-reason required", file=sys.stderr)
            sys.exit(1)

        record_rejection(guardian_path, args.record_rejection, args.rejection_reason, args.category)
        print(json.dumps({'recorded': True}))
        sys.exit(0)

    # Handle update stats
    if args.update_stats:
        if not guardian_path:
            print("Error: Guardian not initialized", file=sys.stderr)
            sys.exit(1)

        update_acceptance_stats(guardian_path, args.category, args.update_stats == 'accept')
        print(json.dumps({'updated': True}))
        sys.exit(0)

    # Handle single suggestion validation
    if args.suggestion:
        suggestions = [{'text': args.suggestion, 'category': args.category}]
        results = validate_multiple_suggestions(suggestions, oracle_path, guardian_path)
        print(json.dumps(results[0], indent=2))
        sys.exit(0)

    # Handle suggestions file
    if args.suggestions_file:
        try:
            with open(args.suggestions_file, 'r', encoding='utf-8') as f:
                suggestions = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, OSError, IOError) as e:
            print(f"Error: Failed to load suggestions file: {e}", file=sys.stderr)
            sys.exit(1)

        results = validate_multiple_suggestions(suggestions, oracle_path, guardian_path)
        print(json.dumps(results, indent=2))
        sys.exit(0)

    parser.print_help()
    sys.exit(1)


if __name__ == '__main__':
    main()
