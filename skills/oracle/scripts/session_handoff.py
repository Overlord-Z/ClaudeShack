#!/usr/bin/env python3
"""
Oracle - Enhanced Session Handoff

Generates comprehensive context for new sessions to prevent degradation from compaction.

This solves the "sessions going insane" problem by preserving critical context
when switching to a fresh session.

Usage:
    # Generate handoff context for new session
    python session_handoff.py --export

    # Import handoff context in new session
    python session_handoff.py --import handoff_context.json

    # Show what would be included (dry run)
    python session_handoff.py --preview

Environment Variables:
    ORACLE_VERBOSE: Set to '1' for detailed output
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


def get_session_context() -> Dict[str, Any]:
    """Extract critical session context for handoff.

    Returns:
        Dictionary with session context for new session
    """
    context = {
        'handoff_timestamp': datetime.now(timezone.utc).isoformat(),
        'handoff_reason': 'session_degradation',
        'oracle_knowledge': {},
        'guardian_health': {},
        'summoner_state': {},
        'active_tasks': [],
        'critical_patterns': [],
        'recent_corrections': [],
        'session_stats': {}
    }

    # Load Oracle knowledge (critical patterns only)
    oracle_dir = Path('.oracle')
    if oracle_dir.exists():
        context['oracle_knowledge'] = load_critical_oracle_knowledge(oracle_dir)

    # Load Guardian session health
    guardian_dir = Path('.guardian')
    if guardian_dir.exists():
        context['guardian_health'] = load_guardian_health(guardian_dir)

    # Load Summoner state (active MCDs)
    summoner_dir = Path('.summoner')
    if summoner_dir.exists():
        context['summoner_state'] = load_summoner_state(summoner_dir)

    # Get active tasks from current session
    context['active_tasks'] = extract_active_tasks()

    # Get session statistics
    context['session_stats'] = get_session_statistics()

    return context


def load_critical_oracle_knowledge(oracle_dir: Path) -> Dict[str, Any]:
    """Load only critical/high-priority Oracle knowledge.

    This is KISS - we don't dump everything, just what matters.

    Args:
        oracle_dir: Path to .oracle directory

    Returns:
        Critical knowledge for handoff
    """
    knowledge = {
        'critical_patterns': [],
        'recent_corrections': [],
        'active_gotchas': [],
        'project_context': ''
    }

    knowledge_dir = oracle_dir / 'knowledge'
    if not knowledge_dir.exists():
        return knowledge

    # Load critical patterns
    patterns_file = knowledge_dir / 'patterns.json'
    if patterns_file.exists():
        try:
            with open(patterns_file, 'r', encoding='utf-8') as f:
                patterns = json.load(f)
                # Only critical/high priority
                knowledge['critical_patterns'] = [
                    p for p in patterns
                    if p.get('priority') in ['critical', 'high']
                ][:10]  # Max 10 patterns
        except (OSError, IOError, json.JSONDecodeError):
            pass

    # Load recent corrections (last 5)
    corrections_file = knowledge_dir / 'corrections.json'
    if corrections_file.exists():
        try:
            with open(corrections_file, 'r', encoding='utf-8') as f:
                corrections = json.load(f)
                # Sort by timestamp, take last 5
                sorted_corrections = sorted(
                    corrections,
                    key=lambda x: x.get('created', ''),
                    reverse=True
                )
                knowledge['recent_corrections'] = sorted_corrections[:5]
        except (OSError, IOError, json.JSONDecodeError):
            pass

    # Load active gotchas
    gotchas_file = knowledge_dir / 'gotchas.json'
    if gotchas_file.exists():
        try:
            with open(gotchas_file, 'r', encoding='utf-8') as f:
                gotchas = json.load(f)
                # Only high priority gotchas
                knowledge['active_gotchas'] = [
                    g for g in gotchas
                    if g.get('priority') == 'high'
                ][:5]  # Max 5 gotchas
        except (OSError, IOError, json.JSONDecodeError):
            pass

    return knowledge


def load_guardian_health(guardian_dir: Path) -> Dict[str, Any]:
    """Load Guardian session health metrics.

    Args:
        guardian_dir: Path to .guardian directory

    Returns:
        Health metrics and degradation signals
    """
    health = {
        'last_health_score': None,
        'degradation_signals': [],
        'handoff_reason': '',
        'session_duration_minutes': 0
    }

    health_file = guardian_dir / 'session_health.json'
    if health_file.exists():
        try:
            with open(health_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                health['last_health_score'] = data.get('health_score')
                health['degradation_signals'] = data.get('degradation_signals', [])
                health['handoff_reason'] = data.get('handoff_reason', '')
                health['session_duration_minutes'] = data.get('duration_minutes', 0)
        except (OSError, IOError, json.JSONDecodeError):
            pass

    return health


def load_summoner_state(summoner_dir: Path) -> Dict[str, Any]:
    """Load Summoner active MCDs and task state.

    Args:
        summoner_dir: Path to .summoner directory

    Returns:
        Active mission state
    """
    state = {
        'active_mcds': [],
        'pending_tasks': [],
        'completed_phases': []
    }

    # Check for active MCDs
    mcds_dir = summoner_dir / 'mcds'
    if mcds_dir.exists():
        for mcd_file in mcds_dir.glob('*.md'):
            try:
                with open(mcd_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract summary and pending tasks
                    state['active_mcds'].append({
                        'name': mcd_file.stem,
                        'file': str(mcd_file),
                        'summary': extract_mcd_summary(content),
                        'pending_tasks': extract_pending_tasks(content)
                    })
            except (OSError, IOError, UnicodeDecodeError):
                continue

    return state


def extract_mcd_summary(mcd_content: str) -> str:
    """Extract executive summary from MCD.

    Args:
        mcd_content: MCD markdown content

    Returns:
        Summary text (max 200 chars)
    """
    lines = mcd_content.split('\n')
    in_summary = False
    summary_lines = []

    for line in lines:
        if '## Executive Summary' in line:
            in_summary = True
            continue
        elif in_summary and line.startswith('##'):
            break
        elif in_summary and line.strip():
            summary_lines.append(line.strip())

    summary = ' '.join(summary_lines)
    return summary[:200] + '...' if len(summary) > 200 else summary


def extract_pending_tasks(mcd_content: str) -> List[str]:
    """Extract uncompleted tasks from MCD.

    Args:
        mcd_content: MCD markdown content

    Returns:
        List of pending task descriptions
    """
    pending = []
    lines = mcd_content.split('\n')

    for line in lines:
        # Look for unchecked checkboxes
        if '- [ ]' in line:
            task = line.replace('- [ ]', '').strip()
            pending.append(task)

    return pending[:10]  # Max 10 pending tasks


def extract_active_tasks() -> List[str]:
    """Extract active tasks from current session.

    Returns:
        List of active task descriptions
    """
    # This would integrate with Claude Code's task system
    # For now, return placeholder
    return []


def get_session_statistics() -> Dict[str, Any]:
    """Get current session statistics.

    Returns:
        Session stats (duration, files modified, etc.)
    """
    stats = {
        'duration_minutes': 0,
        'files_modified': 0,
        'commands_run': 0,
        'errors_encountered': 0
    }

    # Would integrate with Claude Code session tracking
    # For now, return placeholder
    return stats


def generate_handoff_message(context: Dict[str, Any]) -> str:
    """Generate human-readable handoff message for new session.

    Args:
        context: Session context dictionary

    Returns:
        Formatted handoff message
    """
    lines = []

    lines.append("=" * 70)
    lines.append("SESSION HANDOFF CONTEXT")
    lines.append("=" * 70)
    lines.append("")

    # Handoff reason
    health = context.get('guardian_health', {})
    if health.get('handoff_reason'):
        lines.append(f"Handoff Reason: {health['handoff_reason']}")
        lines.append(f"Previous Session Health: {health.get('last_health_score', 'N/A')}/100")
        lines.append(f"Session Duration: {health.get('session_duration_minutes', 0)} minutes")
        lines.append("")

    # Critical Oracle knowledge
    oracle = context.get('oracle_knowledge', {})

    if oracle.get('critical_patterns'):
        lines.append("CRITICAL PATTERNS:")
        lines.append("-" * 70)
        for pattern in oracle['critical_patterns'][:5]:
            lines.append(f"  • {pattern.get('title', 'Unknown')}")
            if pattern.get('content'):
                lines.append(f"    {pattern['content'][:100]}...")
        lines.append("")

    if oracle.get('recent_corrections'):
        lines.append("RECENT CORRECTIONS (Don't repeat these mistakes):")
        lines.append("-" * 70)
        for correction in oracle['recent_corrections']:
            lines.append(f"  • {correction.get('title', 'Unknown')}")
        lines.append("")

    if oracle.get('active_gotchas'):
        lines.append("ACTIVE GOTCHAS:")
        lines.append("-" * 70)
        for gotcha in oracle['active_gotchas']:
            lines.append(f"  • {gotcha.get('title', 'Unknown')}")
        lines.append("")

    # Active Summoner MCDs
    summoner = context.get('summoner_state', {})
    if summoner.get('active_mcds'):
        lines.append("ACTIVE MISSION CONTROL DOCUMENTS:")
        lines.append("-" * 70)
        for mcd in summoner['active_mcds']:
            lines.append(f"  • {mcd['name']}")
            if mcd.get('summary'):
                lines.append(f"    Summary: {mcd['summary']}")
            if mcd.get('pending_tasks'):
                lines.append(f"    Pending tasks: {len(mcd['pending_tasks'])}")
        lines.append("")

    lines.append("=" * 70)
    lines.append("Use '/handoff-continue' to pick up where we left off")
    lines.append("=" * 70)

    return "\n".join(lines)


def export_handoff_context(output_file: str = 'handoff_context.json') -> None:
    """Export session context for handoff.

    Args:
        output_file: Path to output JSON file
    """
    context = get_session_context()

    # Save JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(context, f, indent=2)

    # Print human-readable message
    message = generate_handoff_message(context)
    print(message)
    print(f"\n✅ Handoff context saved to: {output_file}")
    print("\nIn your new session, run:")
    print(f"  python session_handoff.py --import {output_file}")


def import_handoff_context(input_file: str) -> None:
    """Import handoff context in new session.

    Args:
        input_file: Path to handoff JSON file
    """
    if not Path(input_file).exists():
        print(f"❌ Handoff file not found: {input_file}")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        context = json.load(f)

    # Display handoff message
    message = generate_handoff_message(context)
    print(message)

    print("\n✅ Session handoff complete!")
    print("You're now up to speed with critical context from the previous session.")


def preview_handoff() -> None:
    """Preview what would be included in handoff."""
    context = get_session_context()
    message = generate_handoff_message(context)
    print(message)


def main():
    parser = argparse.ArgumentParser(
        description='Enhanced session handoff with Oracle/Guardian/Summoner integration',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--export',
        action='store_true',
        help='Export handoff context for new session'
    )

    parser.add_argument(
        '--import',
        dest='import_file',
        help='Import handoff context from file'
    )

    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview handoff context without exporting'
    )

    parser.add_argument(
        '--output',
        default='handoff_context.json',
        help='Output file for export (default: handoff_context.json)'
    )

    args = parser.parse_args()

    if args.export:
        export_handoff_context(args.output)
    elif args.import_file:
        import_handoff_context(args.import_file)
    elif args.preview:
        preview_handoff()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
