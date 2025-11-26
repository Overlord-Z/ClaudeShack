#!/usr/bin/env python3
"""
Guardian Learning System

Adjusts Guardian sensitivity and thresholds based on user feedback.

Key Principle: "Learn from feedback to adjust sensitivity"

This script:
1. Tracks acceptance/rejection rates per category
2. Adjusts thresholds dynamically to maintain target acceptance rate
3. Learns which file types need more/less review
4. Stores anti-patterns based on rejection reasons
5. Adapts to user's working style over time

Usage:
    # Adjust thresholds based on recent feedback
    python learning.py --adjust

    # Get current threshold recommendations
    python learning.py --recommend

    # Manually set acceptance rate target
    python learning.py --set-target 0.75

    # View learning statistics
    python learning.py --stats

Environment Variables:
    GUARDIAN_CONFIG_PATH: Path to Guardian config file [default: .guardian/config.json]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


def find_guardian_root() -> Optional[Path]:
    """Find the .guardian directory."""
    current = Path.cwd()

    while current != current.parent:
        guardian_path = current / '.guardian'
        if guardian_path.exists():
            return guardian_path
        current = current.parent

    return None


def load_config(guardian_path: Path) -> Dict[str, Any]:
    """Load Guardian configuration."""
    config_path = guardian_path / 'config.json'

    if not config_path.exists():
        return {}

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
        return {}


def save_config(guardian_path: Path, config: Dict[str, Any]) -> None:
    """Save Guardian configuration."""
    config_path = guardian_path / 'config.json'

    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    except (OSError, IOError) as e:
        print(f"Error: Failed to save config: {e}", file=sys.stderr)
        sys.exit(1)


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


def load_rejection_history(guardian_path: Path, days: int = 30) -> List[Dict[str, Any]]:
    """Load recent rejection history.

    Args:
        guardian_path: Path to Guardian directory
        days: Number of days to look back

    Returns:
        List of recent rejections
    """
    history_file = guardian_path / 'rejection_history.json'

    if not history_file.exists():
        return []

    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            all_history = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
        return []

    # Filter to recent rejections
    cutoff = datetime.now() - timedelta(days=days)
    recent = []

    for rejection in all_history:
        try:
            ts = datetime.fromisoformat(rejection.get('timestamp', ''))
            # Handle timezone-aware timestamps
            if ts.tzinfo and not cutoff.tzinfo:
                cutoff = cutoff.replace(tzinfo=ts.tzinfo)
            if ts >= cutoff:
                recent.append(rejection)
        except (ValueError, TypeError):
            continue

    return recent


def calculate_threshold_adjustments(
    config: Dict[str, Any],
    acceptance_stats: Dict[str, Any],
    target_rate: float = 0.7,
    adjustment_speed: float = 0.1
) -> Dict[str, int]:
    """Calculate new threshold values based on acceptance rates.

    Args:
        config: Current configuration
        acceptance_stats: Acceptance statistics
        target_rate: Target acceptance rate (0.0 to 1.0)
        adjustment_speed: How fast to adjust (0.0 to 1.0)

    Returns:
        Dictionary of adjusted threshold values
    """
    current_sensitivity = config.get('sensitivity', {})
    overall_rate = acceptance_stats.get('overall', {}).get('rate', 0.5)

    adjustments = {}

    # Lines threshold adjustment
    current_lines = current_sensitivity.get('lines_threshold', 50)

    if overall_rate < target_rate - 0.1:
        # Too many false positives - increase threshold (trigger less often)
        adjustment = int(current_lines * adjustment_speed)
        adjustments['lines_threshold'] = current_lines + max(5, adjustment)
    elif overall_rate > target_rate + 0.1:
        # Too many missed issues - decrease threshold (trigger more often)
        adjustment = int(current_lines * adjustment_speed)
        adjustments['lines_threshold'] = max(20, current_lines - max(5, adjustment))
    else:
        # Well-calibrated
        adjustments['lines_threshold'] = current_lines

    # Error repeat threshold adjustment
    error_stats = acceptance_stats.get('by_category', {}).get('error_analysis', {})
    error_rate = error_stats.get('rate', 0.5)
    current_error_threshold = current_sensitivity.get('error_repeat_threshold', 3)

    if error_rate < target_rate - 0.1:
        adjustments['error_repeat_threshold'] = min(10, current_error_threshold + 1)
    elif error_rate > target_rate + 0.1:
        adjustments['error_repeat_threshold'] = max(2, current_error_threshold - 1)
    else:
        adjustments['error_repeat_threshold'] = current_error_threshold

    # File churn threshold adjustment
    churn_stats = acceptance_stats.get('by_category', {}).get('file_churn', {})
    churn_rate = churn_stats.get('rate', 0.5)
    current_churn_threshold = current_sensitivity.get('file_churn_threshold', 5)

    if churn_rate < target_rate - 0.1:
        adjustments['file_churn_threshold'] = min(15, current_churn_threshold + 1)
    elif churn_rate > target_rate + 0.1:
        adjustments['file_churn_threshold'] = max(3, current_churn_threshold - 1)
    else:
        adjustments['file_churn_threshold'] = current_churn_threshold

    # Correction threshold adjustment
    correction_stats = acceptance_stats.get('by_category', {}).get('corrections', {})
    correction_rate = correction_stats.get('rate', 0.5)
    current_correction_threshold = current_sensitivity.get('correction_threshold', 3)

    if correction_rate < target_rate - 0.1:
        adjustments['correction_threshold'] = min(10, current_correction_threshold + 1)
    elif correction_rate > target_rate + 0.1:
        adjustments['correction_threshold'] = max(2, current_correction_threshold - 1)
    else:
        adjustments['correction_threshold'] = current_correction_threshold

    return adjustments


def learn_from_rejections(
    rejection_history: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Analyze rejection patterns to learn anti-patterns.

    Args:
        rejection_history: List of rejections

    Returns:
        Dictionary of learned anti-patterns and insights
    """
    insights = {
        'common_rejection_reasons': {},
        'frequently_rejected_categories': {},
        'anti_patterns': []
    }

    # Count rejection reasons
    for rejection in rejection_history:
        reason = rejection.get('reason', 'Unknown')
        category = rejection.get('category', 'general')

        # Count by reason
        if reason not in insights['common_rejection_reasons']:
            insights['common_rejection_reasons'][reason] = 0
        insights['common_rejection_reasons'][reason] += 1

        # Count by category
        if category not in insights['frequently_rejected_categories']:
            insights['frequently_rejected_categories'][category] = 0
        insights['frequently_rejected_categories'][category] += 1

    # Identify anti-patterns (highly rejected categories)
    for category, count in insights['frequently_rejected_categories'].items():
        if count >= 5:  # Rejected 5+ times
            rejection_rate = count / len(rejection_history) if len(rejection_history) > 0 else 0
            if rejection_rate > 0.8:  # 80%+ rejection rate
                insights['anti_patterns'].append({
                    'category': category,
                    'rejection_count': count,
                    'rejection_rate': rejection_rate,
                    'recommendation': f"Stop suggesting {category} - rejection rate {rejection_rate:.0%}"
                })

    return insights


def update_auto_review_rules(
    config: Dict[str, Any],
    acceptance_stats: Dict[str, Any],
    insights: Dict[str, Any]
) -> Dict[str, Any]:
    """Update auto-review rules based on learning.

    Args:
        config: Current configuration
        acceptance_stats: Acceptance statistics
        insights: Learned insights from rejections

    Returns:
        Updated auto_review configuration
    """
    auto_review = config.get('auto_review', {
        'enabled': True,
        'always_review': ['auth', 'security', 'crypto', 'payment'],
        'never_review': ['test', 'mock', 'fixture']
    })

    # Add anti-patterns to never_review
    for anti_pattern in insights.get('anti_patterns', []):
        category = anti_pattern['category']
        if category not in auto_review['never_review']:
            auto_review['never_review'].append(category)

    # Check which categories have high acceptance rates
    by_category = acceptance_stats.get('by_category', {})

    for category, stats in by_category.items():
        rate = stats.get('rate', 0.0)
        total = stats.get('accepted', 0) + stats.get('rejected', 0)

        # If category has >90% acceptance and >10 samples, add to always_review
        if rate > 0.9 and total > 10:
            if category not in auto_review['always_review']:
                auto_review['always_review'].append(category)

        # If category has <20% acceptance and >10 samples, add to never_review
        if rate < 0.2 and total > 10:
            if category not in auto_review['never_review']:
                auto_review['never_review'].append(category)

    return auto_review


def apply_adjustments(
    guardian_path: Path,
    dry_run: bool = False
) -> Dict[str, Any]:
    """Apply learned adjustments to configuration.

    Args:
        guardian_path: Path to Guardian directory
        dry_run: If True, don't save changes (just return recommendations)

    Returns:
        Dictionary with adjustment details
    """
    config = load_config(guardian_path)
    acceptance_stats = load_acceptance_stats(guardian_path)
    rejection_history = load_rejection_history(guardian_path)

    # Get learning parameters
    learning_config = config.get('learning', {})
    target_rate = learning_config.get('acceptance_rate_target', 0.7)
    adjustment_speed = learning_config.get('adjustment_speed', 0.1)

    # Calculate threshold adjustments
    threshold_adjustments = calculate_threshold_adjustments(
        config,
        acceptance_stats,
        target_rate,
        adjustment_speed
    )

    # Learn from rejections
    insights = learn_from_rejections(rejection_history)

    # Update auto-review rules
    updated_auto_review = update_auto_review_rules(config, acceptance_stats, insights)

    # Prepare result
    result = {
        'current_acceptance_rate': acceptance_stats.get('overall', {}).get('rate', 0.0),
        'target_acceptance_rate': target_rate,
        'threshold_adjustments': threshold_adjustments,
        'auto_review_updates': updated_auto_review,
        'insights': insights,
        'applied': not dry_run
    }

    # Apply changes if not dry run
    if not dry_run:
        # Update sensitivity thresholds
        if 'sensitivity' not in config:
            config['sensitivity'] = {}
        config['sensitivity'].update(threshold_adjustments)

        # Update auto_review
        config['auto_review'] = updated_auto_review

        # Save updated config
        save_config(guardian_path, config)

    return result


def get_statistics(guardian_path: Path) -> Dict[str, Any]:
    """Get learning statistics.

    Args:
        guardian_path: Path to Guardian directory

    Returns:
        Statistics dictionary
    """
    config = load_config(guardian_path)
    acceptance_stats = load_acceptance_stats(guardian_path)
    rejection_history = load_rejection_history(guardian_path, days=30)

    overall = acceptance_stats.get('overall', {})
    by_category = acceptance_stats.get('by_category', {})

    stats = {
        'overall': {
            'accepted': overall.get('accepted', 0),
            'rejected': overall.get('rejected', 0),
            'acceptance_rate': overall.get('rate', 0.0)
        },
        'by_category': {},
        'current_thresholds': config.get('sensitivity', {}),
        'target_acceptance_rate': config.get('learning', {}).get('acceptance_rate_target', 0.7),
        'recent_rejections_30d': len(rejection_history),
        'auto_review_rules': config.get('auto_review', {})
    }

    # Add category breakdown
    for category, cat_stats in by_category.items():
        stats['by_category'][category] = {
            'accepted': cat_stats.get('accepted', 0),
            'rejected': cat_stats.get('rejected', 0),
            'rate': cat_stats.get('rate', 0.0)
        }

    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Guardian learning system - adjust thresholds based on feedback',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--adjust',
        action='store_true',
        help='Apply threshold adjustments based on recent feedback'
    )

    parser.add_argument(
        '--recommend',
        action='store_true',
        help='Show recommended adjustments without applying (dry run)'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show learning statistics'
    )

    parser.add_argument(
        '--set-target',
        type=float,
        help='Set target acceptance rate (0.0 to 1.0)'
    )

    parser.add_argument(
        '--set-speed',
        type=float,
        help='Set adjustment speed (0.0 to 1.0)'
    )

    args = parser.parse_args()

    # Find Guardian
    guardian_path = find_guardian_root()

    if not guardian_path:
        print("Error: Guardian not initialized (.guardian directory not found)", file=sys.stderr)
        sys.exit(1)

    # Handle set target
    if args.set_target is not None:
        if not 0.0 <= args.set_target <= 1.0:
            print("Error: Target acceptance rate must be between 0.0 and 1.0", file=sys.stderr)
            sys.exit(1)

        config = load_config(guardian_path)
        if 'learning' not in config:
            config['learning'] = {}
        config['learning']['acceptance_rate_target'] = args.set_target
        save_config(guardian_path, config)

        print(json.dumps({'target_set': args.set_target}))
        sys.exit(0)

    # Handle set speed
    if args.set_speed is not None:
        if not 0.0 <= args.set_speed <= 1.0:
            print("Error: Adjustment speed must be between 0.0 and 1.0", file=sys.stderr)
            sys.exit(1)

        config = load_config(guardian_path)
        if 'learning' not in config:
            config['learning'] = {}
        config['learning']['adjustment_speed'] = args.set_speed
        save_config(guardian_path, config)

        print(json.dumps({'speed_set': args.set_speed}))
        sys.exit(0)

    # Handle stats
    if args.stats:
        stats = get_statistics(guardian_path)
        print(json.dumps(stats, indent=2))
        sys.exit(0)

    # Handle recommend (dry run)
    if args.recommend:
        result = apply_adjustments(guardian_path, dry_run=True)
        print(json.dumps(result, indent=2))
        sys.exit(0)

    # Handle adjust
    if args.adjust:
        result = apply_adjustments(guardian_path, dry_run=False)
        print(json.dumps(result, indent=2))
        sys.exit(0)

    parser.print_help()
    sys.exit(1)


if __name__ == '__main__':
    main()
