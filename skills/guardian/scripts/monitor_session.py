#!/usr/bin/env python3
"""
Guardian Session Monitor

Tracks session health metrics and detects when intervention would be helpful.
This script monitors in the background and triggers Guardian when thresholds are crossed.

Key Principle: MINIMAL STORAGE - only tracks metrics, NOT full conversation content.

Usage:
    # Track a code write event
    python monitor_session.py --event code-written --file auth.py --lines 60

    # Track an error
    python monitor_session.py --event error --message "TypeError: cannot unpack non-iterable"

    # Track a user correction
    python monitor_session.py --event correction --message "that's wrong, use bcrypt instead"

    # Check session health
    python monitor_session.py --check-health

    # Reset session metrics
    python monitor_session.py --reset

Environment Variables:
    GUARDIAN_CONFIG_PATH: Path to Guardian config file [default: .guardian/config.json]
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import defaultdict


def parse_timestamp_with_tz(ts_str: str, reference_time: datetime) -> Optional[datetime]:
    """Parse ISO timestamp and make it comparable with reference_time.

    Args:
        ts_str: ISO format timestamp string
        reference_time: Reference datetime to match timezone with

    Returns:
        Parsed datetime that's comparable with reference_time, or None if parsing fails
    """
    try:
        ts = datetime.fromisoformat(ts_str)
        # If timestamp has timezone but reference doesn't, make timestamp naive
        if ts.tzinfo and not reference_time.tzinfo:
            ts = ts.replace(tzinfo=None)
        # If reference has timezone but timestamp doesn't, make timestamp aware
        elif not ts.tzinfo and reference_time.tzinfo:
            ts = ts.replace(tzinfo=reference_time.tzinfo)
        return ts
    except (ValueError, TypeError):
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


def init_guardian_if_needed() -> Path:
    """Initialize .guardian directory if it doesn't exist."""
    guardian_path = Path.cwd() / '.guardian'

    if not guardian_path.exists():
        guardian_path.mkdir(parents=True, exist_ok=True)

        # Create default config
        default_config = {
            "enabled": True,
            "sensitivity": {
                "lines_threshold": 50,
                "error_repeat_threshold": 3,
                "file_churn_threshold": 5,
                "correction_threshold": 3,
                "context_warning_percent": 0.7
            },
            "trigger_phrases": {
                "review_needed": ["can you review", "does this look right"],
                "struggling": ["still not working", "same error"],
                "complexity": ["this is complex", "not sure how to"]
            },
            "auto_review": {
                "enabled": True,
                "always_review": ["auth", "security", "crypto", "payment"],
                "never_review": ["test", "mock", "fixture"]
            },
            "learning": {
                "acceptance_rate_target": 0.7,
                "adjustment_speed": 0.1,
                "memory_window_days": 30
            },
            "model": "haiku"
        }

        config_path = guardian_path / 'config.json'
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)

        # Create session state file
        state_path = guardian_path / 'session_state.json'
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump({
                "session_start": datetime.now().isoformat(),
                "metrics": {},
                "history": []
            }, f, indent=2)

    return guardian_path


def load_config(guardian_path: Path) -> Dict[str, Any]:
    """Load Guardian configuration."""
    config_path = guardian_path / 'config.json'

    if not config_path.exists():
        # Return default config
        return {
            "enabled": True,
            "sensitivity": {
                "lines_threshold": 50,
                "error_repeat_threshold": 3,
                "file_churn_threshold": 5,
                "correction_threshold": 3,
                "context_warning_percent": 0.7
            }
        }

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
        return {"enabled": False}


def load_session_state(guardian_path: Path) -> Dict[str, Any]:
    """Load current session state."""
    state_path = guardian_path / 'session_state.json'

    if not state_path.exists():
        return {
            "session_start": datetime.now().isoformat(),
            "metrics": {},
            "history": []
        }

    try:
        with open(state_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError, IOError):
        return {
            "session_start": datetime.now().isoformat(),
            "metrics": {},
            "history": []
        }


def save_session_state(guardian_path: Path, state: Dict[str, Any]) -> None:
    """Save session state."""
    state_path = guardian_path / 'session_state.json'

    try:
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
    except (OSError, IOError) as e:
        print(f"Warning: Failed to save session state: {e}", file=sys.stderr)


def track_code_written(state: Dict[str, Any], file_path: str, lines: int) -> None:
    """Track code writing event."""
    MAX_EVENTS = 100  # Limit to prevent unbounded memory growth

    if 'code_written' not in state['metrics']:
        state['metrics']['code_written'] = {}

    if file_path not in state['metrics']['code_written']:
        state['metrics']['code_written'][file_path] = {
            'total_lines': 0,
            'events': []
        }

    state['metrics']['code_written'][file_path]['total_lines'] += lines
    state['metrics']['code_written'][file_path]['events'].append({
        'timestamp': datetime.now().isoformat(),
        'lines': lines
    })

    # Keep only recent events
    if len(state['metrics']['code_written'][file_path]['events']) > MAX_EVENTS:
        state['metrics']['code_written'][file_path]['events'] = \
            state['metrics']['code_written'][file_path]['events'][-MAX_EVENTS:]


def track_error(state: Dict[str, Any], error_message: str) -> None:
    """Track error occurrence."""
    MAX_OCCURRENCES = 50  # Limit to prevent unbounded memory growth

    if 'errors' not in state['metrics']:
        state['metrics']['errors'] = {}

    # Normalize error message (first line only)
    error_key = error_message.split('\n')[0].strip()[:200]

    if error_key not in state['metrics']['errors']:
        state['metrics']['errors'][error_key] = {
            'count': 0,
            'first_seen': datetime.now().isoformat(),
            'last_seen': None,
            'occurrences': []
        }

    state['metrics']['errors'][error_key]['count'] += 1
    state['metrics']['errors'][error_key]['last_seen'] = datetime.now().isoformat()
    state['metrics']['errors'][error_key]['occurrences'].append({
        'timestamp': datetime.now().isoformat()
    })

    # Keep only recent occurrences
    if len(state['metrics']['errors'][error_key]['occurrences']) > MAX_OCCURRENCES:
        state['metrics']['errors'][error_key]['occurrences'] = \
            state['metrics']['errors'][error_key]['occurrences'][-MAX_OCCURRENCES:]


def track_file_edit(state: Dict[str, Any], file_path: str) -> None:
    """Track file edit event."""
    MAX_TIMESTAMPS = 100  # Limit to prevent unbounded memory growth

    if 'file_edits' not in state['metrics']:
        state['metrics']['file_edits'] = {}

    if file_path not in state['metrics']['file_edits']:
        state['metrics']['file_edits'][file_path] = {
            'count': 0,
            'timestamps': []
        }

    state['metrics']['file_edits'][file_path]['count'] += 1
    state['metrics']['file_edits'][file_path]['timestamps'].append(
        datetime.now().isoformat()
    )

    # Keep only recent timestamps
    if len(state['metrics']['file_edits'][file_path]['timestamps']) > MAX_TIMESTAMPS:
        state['metrics']['file_edits'][file_path]['timestamps'] = \
            state['metrics']['file_edits'][file_path]['timestamps'][-MAX_TIMESTAMPS:]


def track_correction(state: Dict[str, Any], message: str) -> None:
    """Track user correction event."""
    MAX_CORRECTIONS = 100  # Limit to prevent unbounded memory growth

    if 'corrections' not in state['metrics']:
        state['metrics']['corrections'] = []

    state['metrics']['corrections'].append({
        'timestamp': datetime.now().isoformat(),
        'message': message[:500]  # Truncate to avoid storing too much
    })

    # Keep only recent corrections
    if len(state['metrics']['corrections']) > MAX_CORRECTIONS:
        state['metrics']['corrections'] = state['metrics']['corrections'][-MAX_CORRECTIONS:]


def check_code_volume_threshold(state: Dict[str, Any], config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Check if code volume threshold is crossed."""
    threshold = config.get('sensitivity', {}).get('lines_threshold', 50)

    code_written = state['metrics'].get('code_written', {})

    for file_path, data in code_written.items():
        if data['total_lines'] >= threshold:
            # Check if this file is in auto_review categories
            auto_review = config.get('auto_review', {})
            always_review = auto_review.get('always_review', [])
            never_review = auto_review.get('never_review', [])

            # Check never_review first
            if any(keyword in file_path.lower() for keyword in never_review):
                continue

            # Check always_review or threshold
            should_review = any(keyword in file_path.lower() for keyword in always_review)

            if should_review or data['total_lines'] >= threshold:
                return {
                    'trigger': 'code_volume',
                    'file': file_path,
                    'lines': data['total_lines'],
                    'threshold': threshold,
                    'priority': 'high' if should_review else 'medium'
                }

    return None


def check_repeated_errors(state: Dict[str, Any], config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Check if same error is repeated."""
    threshold = config.get('sensitivity', {}).get('error_repeat_threshold', 3)

    errors = state['metrics'].get('errors', {})

    for error_key, data in errors.items():
        if data['count'] >= threshold:
            return {
                'trigger': 'repeated_errors',
                'error': error_key,
                'count': data['count'],
                'threshold': threshold,
                'priority': 'critical'
            }

    return None


def check_file_churn(state: Dict[str, Any], config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Check if a file is being edited too frequently."""
    threshold = config.get('sensitivity', {}).get('file_churn_threshold', 5)
    time_window_minutes = 10

    file_edits = state['metrics'].get('file_edits', {})

    for file_path, data in file_edits.items():
        timestamps = data['timestamps']

        # Count edits in last 10 minutes
        cutoff = datetime.now() - timedelta(minutes=time_window_minutes)
        recent_edits = []

        for ts_str in timestamps:
            ts = parse_timestamp_with_tz(ts_str, cutoff)
            if ts and ts >= cutoff:
                recent_edits.append(ts_str)

        if len(recent_edits) >= threshold:
            return {
                'trigger': 'file_churn',
                'file': file_path,
                'edits': len(recent_edits),
                'time_window_minutes': time_window_minutes,
                'threshold': threshold,
                'priority': 'high'
            }

    return None


def check_repeated_corrections(state: Dict[str, Any], config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Check if user is making repeated corrections."""
    threshold = config.get('sensitivity', {}).get('correction_threshold', 3)
    time_window_minutes = 30

    corrections = state['metrics'].get('corrections', [])

    # Count corrections in last 30 minutes
    cutoff = datetime.now() - timedelta(minutes=time_window_minutes)
    recent_corrections = []

    for correction in corrections:
        try:
            ts = parse_timestamp_with_tz(correction['timestamp'], cutoff)
            if ts and ts >= cutoff:
                recent_corrections.append(correction)
        except KeyError:
            continue

    if len(recent_corrections) >= threshold:
        return {
            'trigger': 'repeated_corrections',
            'count': len(recent_corrections),
            'time_window_minutes': time_window_minutes,
            'threshold': threshold,
            'priority': 'critical'
        }

    return None


def calculate_session_health(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate overall session health score."""
    health_score = 100
    recommendations = []

    # Check error rate
    errors = state['metrics'].get('errors', {})
    total_errors = sum(data['count'] for data in errors.values())

    try:
        session_start = datetime.fromisoformat(state['session_start'])
        now = datetime.now(session_start.tzinfo) if session_start.tzinfo else datetime.now()
        session_duration_minutes = max(1, (now - session_start).total_seconds() / 60)
        error_rate = total_errors / session_duration_minutes
    except (ValueError, TypeError):
        error_rate = 0
        session_duration_minutes = 0

    if error_rate > 0.5:  # More than 1 error per 2 minutes
        health_score -= 20
        recommendations.append("High error rate - consider taking a break or reassessing approach")

    # Check correction rate
    corrections = state['metrics'].get('corrections', [])
    correction_rate = len(corrections) / max(1, session_duration_minutes)

    if correction_rate > 0.1:  # More than 1 correction per 10 minutes
        health_score -= 15
        recommendations.append("Frequent corrections - session may be going off track")

    # Check file churn
    file_edits = state['metrics'].get('file_edits', {})
    for file_path, data in file_edits.items():
        if data['count'] > 5:
            health_score -= 10
            recommendations.append(f"High churn on {file_path} - consider taking a break from this file")
            break

    # Check repeated errors
    for error_key, data in errors.items():
        if data['count'] >= 3:
            health_score -= 20
            recommendations.append(f"Repeated error: {error_key[:50]}... - approach may be fundamentally wrong")
            break

    return {
        'score': max(0, health_score),
        'session_duration_minutes': int(session_duration_minutes),
        'total_errors': total_errors,
        'total_corrections': len(corrections),
        'recommendations': recommendations
    }


def check_triggers(state: Dict[str, Any], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check all triggers and return those that fired."""
    triggered = []

    # Check each trigger
    trigger = check_code_volume_threshold(state, config)
    if trigger:
        triggered.append(trigger)

    trigger = check_repeated_errors(state, config)
    if trigger:
        triggered.append(trigger)

    trigger = check_file_churn(state, config)
    if trigger:
        triggered.append(trigger)

    trigger = check_repeated_corrections(state, config)
    if trigger:
        triggered.append(trigger)

    return triggered


def main():
    parser = argparse.ArgumentParser(
        description='Guardian session health monitor',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--event',
        choices=['code-written', 'error', 'file-edit', 'correction'],
        help='Type of event to track'
    )

    parser.add_argument(
        '--file',
        help='File path (for code-written and file-edit events)'
    )

    parser.add_argument(
        '--lines',
        type=int,
        help='Number of lines written (for code-written events)'
    )

    parser.add_argument(
        '--message',
        help='Error or correction message'
    )

    parser.add_argument(
        '--check-health',
        action='store_true',
        help='Check current session health'
    )

    parser.add_argument(
        '--check-triggers',
        action='store_true',
        help='Check if any triggers have fired'
    )

    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset session metrics'
    )

    parser.add_argument(
        '--init',
        action='store_true',
        help='Initialize Guardian for this project'
    )

    args = parser.parse_args()

    # Initialize Guardian if requested
    if args.init:
        guardian_path = init_guardian_if_needed()
        print(f"Guardian initialized at {guardian_path}")
        sys.exit(0)

    # Find or create Guardian directory
    guardian_path = find_guardian_root()
    if not guardian_path:
        guardian_path = init_guardian_if_needed()

    # Load config and state
    config = load_config(guardian_path)

    if not config.get('enabled', False):
        print("Guardian is disabled in config", file=sys.stderr)
        sys.exit(0)

    state = load_session_state(guardian_path)

    # Handle reset
    if args.reset:
        state = {
            "session_start": datetime.now().isoformat(),
            "metrics": {},
            "history": []
        }
        save_session_state(guardian_path, state)
        print("Session metrics reset")
        sys.exit(0)

    # Handle health check
    if args.check_health:
        health = calculate_session_health(state, config)
        print(json.dumps(health, indent=2))
        sys.exit(0)

    # Handle trigger check
    if args.check_triggers:
        triggers = check_triggers(state, config)
        print(json.dumps(triggers, indent=2))
        sys.exit(0)

    # Handle event tracking
    if args.event:
        if args.event == 'code-written':
            if not args.file or args.lines is None:
                print("Error: --file and --lines required for code-written event", file=sys.stderr)
                sys.exit(1)
            track_code_written(state, args.file, args.lines)

        elif args.event == 'error':
            if not args.message:
                print("Error: --message required for error event", file=sys.stderr)
                sys.exit(1)
            track_error(state, args.message)

        elif args.event == 'file-edit':
            if not args.file:
                print("Error: --file required for file-edit event", file=sys.stderr)
                sys.exit(1)
            track_file_edit(state, args.file)

        elif args.event == 'correction':
            if not args.message:
                print("Error: --message required for correction event", file=sys.stderr)
                sys.exit(1)
            track_correction(state, args.message)

        # Save updated state
        save_session_state(guardian_path, state)

        # Check if any triggers fired
        triggers = check_triggers(state, config)
        if triggers:
            print(json.dumps({'event_recorded': True, 'triggers': triggers}, indent=2))
        else:
            print(json.dumps({'event_recorded': True}, indent=2))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
