#!/usr/bin/env python3
"""
Guardian - Main Orchestrator

Coordinates Guardian components to provide automatic quality gates and session health monitoring.

This is the main entry point for Guardian operations. It:
1. Checks session health metrics
2. Determines if intervention is needed
3. Extracts minimal context
4. Spawns Haiku subagent for focused review/planning
5. Validates suggestions against Oracle
6. Presents results to user with confidence scores
7. Learns from user feedback

Usage:
    # Manual code review
    python guardian.py review --file auth.py --focus security

    # Check if Guardian should trigger
    python guardian.py check

    # Plan a complex task
    python guardian.py plan --task "Build REST API with auth and rate limiting"

    # Debug an error
    python guardian.py debug --file app.py --error "TypeError: cannot unpack"

    # Get session health status
    python guardian.py status

Environment Variables:
    GUARDIAN_MODEL: Model to use for subagents [default: haiku]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess


def find_scripts_dir() -> Path:
    """Find the Guardian Scripts directory."""
    return Path(__file__).parent


def run_script(script_name: str, args: List[str]) -> Dict[str, Any]:
    """Run a Guardian script and return JSON output.

    Args:
        script_name: Name of the script (without .py extension)
        args: List of command-line arguments

    Returns:
        Parsed JSON output from the script
    """
    scripts_dir = find_scripts_dir()
    script_path = scripts_dir / f"{script_name}.py"

    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    try:
        result = subprocess.run(
            ['python', str(script_path)] + args,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            # Try to parse error as JSON
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {'error': result.stderr or result.stdout}

        # Parse output as JSON
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {'output': result.stdout}

    except subprocess.TimeoutExpired:
        return {'error': 'Script timeout'}
    except Exception as e:
        return {'error': str(e)}


def check_triggers() -> Dict[str, Any]:
    """Check if any Guardian triggers have fired."""
    return run_script('monitor_session', ['--check-triggers'])


def get_session_health() -> Dict[str, Any]:
    """Get current session health metrics."""
    return run_script('monitor_session', ['--check-health'])


def extract_context(
    task_type: str,
    file_path: Optional[str] = None,
    focus: Optional[str] = None,
    description: Optional[str] = None,
    error_message: Optional[str] = None
) -> str:
    """Extract minimal context for subagent task."""
    args = ['--task', task_type, '--format', 'text']

    if file_path:
        args.extend(['--file', file_path])
    if focus:
        args.extend(['--focus', focus])
    if description:
        args.extend(['--description', description])
    if error_message:
        args.extend(['--error', error_message])

    result = run_script('context_filter', args)

    if 'output' in result:
        return result['output']
    elif 'error' in result:
        return f"Error extracting context: {result['error']}"
    else:
        return str(result)


def validate_suggestions(suggestions: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Validate suggestions against Oracle knowledge.

    Args:
        suggestions: List of suggestion dictionaries with 'text' and 'category' keys

    Returns:
        List of validated suggestions with confidence scores
    """
    # Create temporary file with suggestions
    import tempfile
    suggestions_file = None

    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(suggestions, f)
            suggestions_file = f.name

        result = run_script('validator', ['--suggestions-file', suggestions_file])
        return result if isinstance(result, list) else []
    finally:
        # Clean up temp file
        if suggestions_file:
            try:
                os.unlink(suggestions_file)
            except OSError:
                pass


def format_suggestions_for_user(validated_suggestions: List[Dict[str, Any]]) -> str:
    """Format validated suggestions for user presentation.

    Args:
        validated_suggestions: List of validated suggestions

    Returns:
        Formatted string for user
    """
    lines = []

    # Filter to presentable suggestions
    presentable = [s for s in validated_suggestions if s.get('should_present', True)]

    if not presentable:
        return "Guardian: No suggestions to present (all filtered by validation)"

    lines.append(f"Guardian Review Found {len(presentable)} Suggestions:")
    lines.append("")

    for i, suggestion in enumerate(presentable, 1):
        confidence = suggestion.get('confidence', 0.0)
        text = suggestion.get('suggestion', '')
        category = suggestion.get('category', 'general')
        warnings = suggestion.get('warnings', [])
        notes = suggestion.get('notes', [])

        # Format confidence indicator
        if confidence >= 0.7:
            conf_indicator = f"[{confidence:.2f}]"
        elif confidence >= 0.5:
            conf_indicator = f"?[{confidence:.2f}]"
        else:
            conf_indicator = f"![{confidence:.2f}]"

        lines.append(f"{i}. {conf_indicator} {text}")
        lines.append(f"   Category: {category}")

        # Add warnings
        for warning in warnings:
            severity = warning.get('severity', 'low')
            message = warning.get('message', '')
            if severity == 'high':
                lines.append(f"   WARNING: {message}")
            else:
                lines.append(f"   Note: {message}")

        # Add notes
        for note in notes:
            lines.append(f"   {note}")

        lines.append("")

    # Add command options
    lines.append("Options:")
    lines.append("  a - Accept all high-confidence suggestions (>=0.7)")
    lines.append("  1,3,5 - Accept specific suggestions by number")
    lines.append("  r - Reject all with reason")
    lines.append("  i <reason> - Reject and add to anti-patterns")
    lines.append("  d <num> - Discuss specific suggestion")
    lines.append("  q - Dismiss review")

    return "\n".join(lines)


def perform_review(
    file_path: str,
    focus: Optional[str] = None
) -> None:
    """Perform code review using Guardian.

    Args:
        file_path: Path to file to review
        focus: Optional focus keywords (e.g., "security performance")
    """
    print(f"Guardian: Reviewing {file_path}...")
    print()

    # Extract minimal context
    context = extract_context('review', file_path=file_path, focus=focus)

    # TODO: This is where we would spawn a Haiku subagent via the Task tool
    # For now, we'll output the context that would be passed
    print("=" * 60)
    print("MINIMAL CONTEXT EXTRACTED (would be passed to Haiku agent):")
    print("=" * 60)
    print(context)
    print("=" * 60)
    print()

    # TODO: Parse subagent response and extract suggestions
    # For now, create a mock suggestion for testing
    mock_suggestions = [
        {
            'text': 'Consider using bcrypt for password hashing instead of MD5',
            'category': 'security'
        }
    ]

    # Validate suggestions
    validated = validate_suggestions(mock_suggestions)

    # Format and present to user
    presentation = format_suggestions_for_user(validated)
    print(presentation)


def perform_planning(task_description: str) -> None:
    """Break down a complex task using Guardian planning.

    Args:
        task_description: Description of the task to break down
    """
    print("Guardian: Breaking down complex task...")
    print()

    # Extract minimal context
    context = extract_context('plan', description=task_description)

    print("=" * 60)
    print("MINIMAL CONTEXT EXTRACTED (would be passed to Haiku agent):")
    print("=" * 60)
    print(context)
    print("=" * 60)
    print()

    print("TODO: Spawn Haiku planning agent and present breakdown")


def perform_debug(file_path: str, error_message: str) -> None:
    """Debug an error using Guardian.

    Args:
        file_path: Path to file with error
        error_message: Error message to debug
    """
    print(f"Guardian: Debugging error in {file_path}...")
    print()

    # Extract minimal context
    context = extract_context('debug', file_path=file_path, error_message=error_message)

    print("=" * 60)
    print("MINIMAL CONTEXT EXTRACTED (would be passed to Haiku agent):")
    print("=" * 60)
    print(context)
    print("=" * 60)
    print()

    print("TODO: Spawn Haiku debug agent and present analysis")


def check_if_should_trigger() -> bool:
    """Check if Guardian should automatically trigger.

    Returns:
        True if Guardian should trigger, False otherwise
    """
    triggers = check_triggers()

    if isinstance(triggers, list) and len(triggers) > 0:
        print("Guardian: Detected triggers:")
        print(json.dumps(triggers, indent=2))
        return True

    return False


def show_status() -> None:
    """Show current session health status."""
    health = get_session_health()

    print("Guardian Session Health Status:")
    print("=" * 60)
    print(json.dumps(health, indent=2))
    print("=" * 60)

    # Check triggers
    triggers = check_triggers()
    if isinstance(triggers, list) and len(triggers) > 0:
        print()
        print("Active Triggers:")
        for trigger in triggers:
            trigger_type = trigger.get('trigger', 'unknown')
            priority = trigger.get('priority', 'medium')
            print(f"  - [{priority.upper()}] {trigger_type}")
            for key, value in trigger.items():
                if key not in ['trigger', 'priority']:
                    print(f"    {key}: {value}")


def main():
    parser = argparse.ArgumentParser(
        description='Guardian - Quality gate and session health monitor',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Guardian commands')

    # Review command
    review_parser = subparsers.add_parser('review', help='Review code for issues')
    review_parser.add_argument('--file', required=True, help='File to review')
    review_parser.add_argument('--focus', help='Focus keywords (e.g., "security performance")')

    # Plan command
    plan_parser = subparsers.add_parser('plan', help='Break down complex task')
    plan_parser.add_argument('--task', required=True, help='Task description')

    # Debug command
    debug_parser = subparsers.add_parser('debug', help='Debug an error')
    debug_parser.add_argument('--file', required=True, help='File with error')
    debug_parser.add_argument('--error', required=True, help='Error message')

    # Check command
    subparsers.add_parser('check', help='Check if Guardian should trigger')

    # Status command
    subparsers.add_parser('status', help='Show session health status')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == 'review':
        perform_review(args.file, args.focus)

    elif args.command == 'plan':
        perform_planning(args.task)

    elif args.command == 'debug':
        perform_debug(args.file, args.error)

    elif args.command == 'check':
        if check_if_should_trigger():
            sys.exit(0)  # Should trigger
        else:
            print("Guardian: No triggers detected")
            sys.exit(1)  # Should not trigger

    elif args.command == 'status':
        show_status()


if __name__ == '__main__':
    main()
