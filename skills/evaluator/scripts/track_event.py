#!/usr/bin/env python3
"""
Evaluator Event Tracking

Privacy-first anonymous telemetry for ClaudeShack skills.

Usage:
    # Track a skill invocation
    python track_event.py --skill oracle --event invoked --success true

    # Track a metric
    python track_event.py --skill guardian --metric acceptance_rate --value 0.75

    # Track an error (type only, no message)
    python track_event.py --skill summoner --event error --error-type FileNotFoundError

    # Enable/disable telemetry
    python track_event.py --enable
    python track_event.py --disable

    # View local events
    python track_event.py --show-events
    python track_event.py --summary
"""

import os
import sys
import json
import argparse
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any


def find_evaluator_root() -> Path:
    """Find or create the .evaluator directory."""
    current = Path.cwd()

    while current != current.parent:
        evaluator_path = current / '.evaluator'
        if evaluator_path.exists():
            return evaluator_path
        current = current.parent

    # Not found, create in current project root
    evaluator_path = Path.cwd() / '.evaluator'
    evaluator_path.mkdir(parents=True, exist_ok=True)

    return evaluator_path


def load_config(evaluator_path: Path) -> Dict[str, Any]:
    """Load Evaluator configuration."""
    config_file = evaluator_path / 'config.json'

    if not config_file.exists():
        # Create default config (telemetry DISABLED by default)
        default_config = {
            "enabled": False,
            "anonymous_id": generate_anonymous_id(),
            "send_aggregates": False,
            "retention_days": 30,
            "aggregation_interval_days": 7,
            "collect": {
                "skill_usage": True,
                "performance_metrics": True,
                "error_types": True,
                "success_rates": True
            },
            "exclude_skills": [],
            "github": {
                "repo": "Overlord-Z/ClaudeShack",
                "discussions_category": "Telemetry",
                "issue_labels": ["feedback", "telemetry"]
            }
        }

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)

        return default_config

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError, IOError):
        return {"enabled": False}


def save_config(evaluator_path: Path, config: Dict[str, Any]) -> None:
    """Save Evaluator configuration."""
    config_file = evaluator_path / 'config.json'

    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    except (OSError, IOError) as e:
        print(f"Error: Failed to save config: {e}", file=sys.stderr)
        sys.exit(1)


def generate_anonymous_id() -> str:
    """Generate a daily-rotating anonymous ID.

    Returns:
        Anonymous hash that rotates daily
    """
    # Use date as salt for daily rotation
    date_salt = datetime.now().strftime('%Y-%m-%d')

    # Mix with random system identifier (not personally identifiable)
    # Using just the date makes it truly anonymous - all users on same date have same ID
    combined = f"{date_salt}"

    return hashlib.sha256(combined.encode()).hexdigest()[:16]


def track_event(
    evaluator_path: Path,
    config: Dict[str, Any],
    skill_name: str,
    event_type: str,
    success: Optional[bool] = None,
    error_type: Optional[str] = None,
    duration_ms: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """Track a skill usage event.

    Args:
        evaluator_path: Path to .evaluator directory
        config: Evaluator configuration
        skill_name: Name of the skill
        event_type: Type of event (invoked, error, etc.)
        success: Whether the operation succeeded
        error_type: Type of error (if applicable)
        duration_ms: Duration in milliseconds
        metadata: Additional anonymous metadata
    """
    if not config.get('enabled', False):
        # Telemetry disabled, skip silently
        return

    # Check if skill is excluded
    if skill_name in config.get('exclude_skills', []):
        return

    # Build event
    event = {
        "event_type": f"{skill_name}_{event_type}",
        "skill_name": skill_name,
        "timestamp": datetime.now().isoformat(),
        "session_id": config.get('anonymous_id', 'unknown'),
        "success": success,
        "error_type": error_type,  # Type only, never error message
        "duration_ms": duration_ms
    }

    # Add anonymous metadata if provided
    if metadata:
        event["metadata"] = metadata

    # Append to events file (JSONL format)
    events_file = evaluator_path / 'events.jsonl'

    try:
        with open(events_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event) + '\n')
    except (OSError, IOError) as e:
        # Fail silently - telemetry should never break the workflow
        pass


def track_metric(
    evaluator_path: Path,
    config: Dict[str, Any],
    skill_name: str,
    metric_name: str,
    value: float,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """Track a skill metric.

    Args:
        evaluator_path: Path to .evaluator directory
        config: Evaluator configuration
        skill_name: Name of the skill
        metric_name: Name of the metric
        value: Metric value
        metadata: Additional anonymous metadata
    """
    track_event(
        evaluator_path,
        config,
        skill_name,
        "metric",
        metadata={
            "metric_name": metric_name,
            "value": value,
            **(metadata or {})
        }
    )


def load_events(evaluator_path: Path, days: Optional[int] = None) -> List[Dict[str, Any]]:
    """Load events from local storage.

    Args:
        evaluator_path: Path to .evaluator directory
        days: Optional number of days to look back

    Returns:
        List of events
    """
    events_file = evaluator_path / 'events.jsonl'

    if not events_file.exists():
        return []

    events = []
    cutoff = None

    if days:
        cutoff = datetime.now() - timedelta(days=days)

    try:
        with open(events_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())

                    # Filter by date if cutoff specified
                    if cutoff:
                        event_time = datetime.fromisoformat(event['timestamp'])
                        if event_time < cutoff:
                            continue

                    events.append(event)
                except json.JSONDecodeError:
                    continue
    except (OSError, IOError):
        return []

    return events


def show_summary(events: List[Dict[str, Any]]) -> None:
    """Show summary of local events.

    Args:
        events: List of events
    """
    if not events:
        print("No telemetry events recorded")
        return

    print("=" * 60)
    print("LOCAL TELEMETRY SUMMARY (Never Sent Anywhere)")
    print("=" * 60)
    print()

    # Count by skill
    by_skill = {}
    for event in events:
        skill = event.get('skill_name', 'unknown')
        if skill not in by_skill:
            by_skill[skill] = {'total': 0, 'success': 0, 'errors': 0}

        by_skill[skill]['total'] += 1

        if event.get('success') is True:
            by_skill[skill]['success'] += 1
        elif event.get('error_type'):
            by_skill[skill]['errors'] += 1

    # Print summary
    for skill, stats in sorted(by_skill.items()):
        print(f"{skill}:")
        print(f"  Total events: {stats['total']}")
        print(f"  Successes: {stats['success']}")
        print(f"  Errors: {stats['errors']}")

        if stats['total'] > 0:
            success_rate = (stats['success'] / stats['total']) * 100
            print(f"  Success rate: {success_rate:.1f}%")

        print()

    print("=" * 60)
    print(f"Total events: {len(events)}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Privacy-first anonymous telemetry for ClaudeShack',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--skill', help='Skill name')
    parser.add_argument('--event', help='Event type (invoked, error, etc.)')
    parser.add_argument('--success', type=bool, help='Whether operation succeeded')
    parser.add_argument('--error-type', help='Error type (not message)')
    parser.add_argument('--duration', type=int, help='Duration in milliseconds')

    parser.add_argument('--metric', help='Metric name')
    parser.add_argument('--value', type=float, help='Metric value')

    parser.add_argument('--enable', action='store_true', help='Enable telemetry (opt-in)')
    parser.add_argument('--disable', action='store_true', help='Disable telemetry')
    parser.add_argument('--status', action='store_true', help='Show telemetry status')

    parser.add_argument('--show-events', action='store_true', help='Show local events')
    parser.add_argument('--summary', action='store_true', help='Show event summary')
    parser.add_argument('--days', type=int, help='Days to look back (default: all)')

    parser.add_argument('--purge', action='store_true', help='Delete all local telemetry data')

    args = parser.parse_args()

    # Find evaluator directory
    evaluator_path = find_evaluator_root()
    config = load_config(evaluator_path)

    # Handle enable/disable
    if args.enable:
        config['enabled'] = True
        config['anonymous_id'] = generate_anonymous_id()
        save_config(evaluator_path, config)
        print("✓ Telemetry enabled (anonymous, opt-in)")
        print(f"  Anonymous ID: {config['anonymous_id']}")
        print("  No personally identifiable information is collected")
        print("  You can disable anytime with: --disable")
        sys.exit(0)

    if args.disable:
        config['enabled'] = False
        save_config(evaluator_path, config)
        print("✓ Telemetry disabled")
        print("  Run with --purge to delete all local data")
        sys.exit(0)

    # Handle status
    if args.status:
        print("Evaluator Telemetry Status:")
        print("=" * 60)
        print(f"Enabled: {config.get('enabled', False)}")
        print(f"Anonymous ID: {config.get('anonymous_id', 'Not set')}")
        print(f"Send aggregates: {config.get('send_aggregates', False)}")
        print(f"Retention: {config.get('retention_days', 30)} days")

        # Count events
        events = load_events(evaluator_path)
        print(f"Local events: {len(events)}")
        print("=" * 60)
        sys.exit(0)

    # Handle purge
    if args.purge:
        events_file = evaluator_path / 'events.jsonl'
        if events_file.exists():
            events_file.unlink()
            print("✓ All local telemetry data deleted")
        else:
            print("No telemetry data to delete")
        sys.exit(0)

    # Handle show events
    if args.show_events:
        events = load_events(evaluator_path, args.days)
        print(json.dumps(events, indent=2))
        sys.exit(0)

    # Handle summary
    if args.summary:
        events = load_events(evaluator_path, args.days)
        show_summary(events)
        sys.exit(0)

    # Track event
    if args.skill and args.event:
        track_event(
            evaluator_path,
            config,
            args.skill,
            args.event,
            args.success,
            args.error_type,
            args.duration
        )
        # Silent success (telemetry should be invisible)
        sys.exit(0)

    # Track metric
    if args.skill and args.metric and args.value is not None:
        track_metric(
            evaluator_path,
            config,
            args.skill,
            args.metric,
            args.value
        )
        # Silent success
        sys.exit(0)

    parser.print_help()
    sys.exit(1)


if __name__ == '__main__':
    main()
