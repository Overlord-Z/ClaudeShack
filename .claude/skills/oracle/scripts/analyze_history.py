#!/usr/bin/env python3
"""
Oracle Conversation History Analyzer

Analyzes Claude Code conversation history from ~/.claude/projects/ and extracts:
- Patterns and repeated tasks
- Corrections and learnings
- User preferences and gotchas
- Automation opportunities

This script mines existing conversation data without requiring manual capture.

Usage:
    python analyze_history.py [options]
    python analyze_history.py --project-hash abc123 --auto-populate
    python analyze_history.py --all-projects --recent-days 30
    python analyze_history.py --analyze-only

Examples:
    python analyze_history.py --auto-populate
    python analyze_history.py --project-hash abc123def456
    python analyze_history.py --all-projects --min-confidence 0.7
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
import re
import uuid


CLAUDE_PROJECTS_PATH = Path.home() / '.claude' / 'projects'

# Configuration constants
CONFIG = {
    'MAX_TITLE_LENGTH': 200,
    'ACTION_CONTEXT_MIN_LEN': 10,
    'ACTION_CONTEXT_MAX_LEN': 50,
    'TOP_TOOLS_TO_REPORT': 20,
    'TOP_CORRECTIONS_TO_ADD': 10,
    'TOP_GOTCHAS_TO_ADD': 10,
    'TOP_TASKS_TO_ADD': 5,
    'MAX_PREFERENCES_TO_ADD': 10,
    'DEFAULT_MIN_TASK_OCCURRENCES': 3,
    'SNIPPET_LENGTH': 80,
}

# Precompiled regex patterns for performance
CORRECTION_PATTERNS = [
    re.compile(r"(?:that's|thats)\s+(?:wrong|incorrect|not right)", re.IGNORECASE),
    re.compile(r"(?:don't|dont|do not)\s+(?:do|use|implement)", re.IGNORECASE),
    re.compile(r"(?:should|need to)\s+(?:use|do|implement).+(?:instead|not)", re.IGNORECASE),
    re.compile(r"(?:actually|correction|fix)[:,]\s+", re.IGNORECASE),
    re.compile(r"(?:no|nope),?\s+(?:use|do|try|implement)", re.IGNORECASE),
    re.compile(r"(?:wrong|incorrect|mistake)[:,]", re.IGNORECASE),
    re.compile(r"(?:better to|prefer to|should)\s+(?:use|do)", re.IGNORECASE),
]

PREFERENCE_PATTERNS = [
    re.compile(r"(?:i prefer|i'd prefer|prefer to|i like)\s+(.+)", re.IGNORECASE),
    re.compile(r"(?:always|never)\s+(?:use|do|implement)\s+(.+)", re.IGNORECASE),
    re.compile(r"(?:i want|i'd like|i need)\s+(.+)", re.IGNORECASE),
    re.compile(r"(?:make sure|ensure|remember)\s+(?:to|that)?\s+(.+)", re.IGNORECASE),
    re.compile(r"(?:use|implement|do)\s+(.+)\s+(?:instead|not)", re.IGNORECASE),
]

GOTCHA_PATTERNS = [
    re.compile(r"(?:error|issue|problem|bug|failing|broken)[:,]?\s+(.+)", re.IGNORECASE),
    re.compile(r"(?:warning|careful|watch out)[:,]?\s+(.+)", re.IGNORECASE),
    re.compile(r"(?:doesn't work|not working|fails when)\s+(.+)", re.IGNORECASE),
    re.compile(r"(?:remember|don't forget)[:,]?\s+(.+)", re.IGNORECASE),
]


def truncate_text(text, max_length=100, suffix='...'):
    """Truncate text to max_length, breaking at word boundaries."""
    if len(text) <= max_length:
        return text

    truncated = text[:max_length].rsplit(' ', 1)[0]
    return truncated + suffix


def ensure_knowledge_file(file_path, default_content=None):
    """Ensure knowledge file exists, create with default content if missing."""
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_content or [], f, indent=2)

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_oracle_root():
    """Find the .oracle directory."""
    current = Path.cwd()

    while current != current.parent:
        oracle_path = current / '.oracle'
        if oracle_path.exists():
            return oracle_path
        current = current.parent

    return None


def find_project_hash(oracle_path):
    """Try to determine the project hash for current project."""
    # The project hash is based on the project path
    # We'll look for recent activity in claude projects that might match

    if not CLAUDE_PROJECTS_PATH.exists():
        return None

    project_root = oracle_path.parent
    project_name = project_root.name

    # Get all project directories
    project_dirs = [d for d in CLAUDE_PROJECTS_PATH.iterdir() if d.is_dir()]

    # Sort by most recent modification
    project_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    # Return the most recent one (likely current project)
    if project_dirs:
        return project_dirs[0].name

    return None


def load_conversation_history(project_hash, recent_days=None):
    """Load conversation history from JSONL files."""
    project_path = CLAUDE_PROJECTS_PATH / project_hash

    if not project_path.exists():
        print(f"[ERROR] Project path not found: {project_path}")
        return []

    conversations = []
    cutoff_date = None

    if recent_days:
        cutoff_date = datetime.now() - timedelta(days=recent_days)

    # Find all JSONL files
    jsonl_files = list(project_path.glob('*.jsonl'))

    print(f"[INFO] Found {len(jsonl_files)} conversation files in project {project_hash[:8]}...")

    for jsonl_file in jsonl_files:
        # Check modification date
        if cutoff_date:
            mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime)
            if mtime < cutoff_date:
                continue

        try:
            # Use streaming approach for memory efficiency
            session_data = {
                'session_id': jsonl_file.stem,
                'file_path': jsonl_file,
                'messages': [],
                'tools_used': [],
                'created': datetime.fromtimestamp(jsonl_file.stat().st_mtime)
            }

            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:  # Stream line by line - memory efficient
                    if line.strip():
                        try:
                            entry = json.loads(line)
                            session_data['messages'].append(entry)

                            # Extract tool usage
                            if 'message' in entry:
                                content = entry['message'].get('content', [])
                                if isinstance(content, list):
                                    for item in content:
                                        if isinstance(item, dict) and item.get('type') == 'tool_use':
                                            session_data['tools_used'].append(item.get('name'))

                        except json.JSONDecodeError:
                            continue

            conversations.append(session_data)

        except Exception as e:
            print(f"[WARNING] Failed to load {jsonl_file.name}: {e}")
            continue

    print(f"[OK] Loaded {len(conversations)} conversations")
    return conversations


def extract_messages_by_role(conversations, role='user'):
    """Extract messages of specified role from conversations."""
    messages = []

    for session in conversations:
        for msg in session['messages']:
            if 'message' not in msg:
                continue

            message = msg['message']
            if message.get('role') != role:
                continue

            content = message.get('content', '')

            # Handle both string and list content
            if isinstance(content, list):
                text_parts = []
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'text':
                        text_parts.append(item.get('text', ''))
                content = ' '.join(text_parts)

            if content:
                messages.append({
                    'session_id': session['session_id'],
                    'content': content,
                    'timestamp': session['created']
                })

    return messages


def detect_corrections(user_messages):
    """Detect correction patterns in user messages."""
    corrections = []

    for msg in user_messages:
        content = msg['content']

        for pattern in CORRECTION_PATTERNS:
            if pattern.search(content):
                corrections.append({
                    'session_id': msg['session_id'],
                    'content': msg['content'],
                    'timestamp': msg['timestamp'],
                    'pattern_matched': pattern.pattern
                })
                break

    return corrections


def detect_preferences(user_messages):
    """Detect user preferences from messages."""
    preferences = []

    for msg in user_messages:
        content = msg['content']

        for pattern in PREFERENCE_PATTERNS:
            matches = pattern.findall(content)
            if matches:
                for match in matches:
                    match_text = match.strip() if isinstance(match, str) else match
                    # Only capture meaningful preferences
                    if len(match_text) > 5:
                        preferences.append({
                            'session_id': msg['session_id'],
                            'preference': match_text,
                            'full_context': content,
                            'timestamp': msg['timestamp']
                        })

    return preferences


def detect_repeated_tasks(user_messages, min_occurrences=None):
    """Detect repeated tasks that could be automated."""
    if min_occurrences is None:
        min_occurrences = CONFIG['DEFAULT_MIN_TASK_OCCURRENCES']

    # Extract common patterns
    task_patterns = defaultdict(list)

    # Common action verbs
    action_verbs = [
        'create', 'add', 'update', 'delete', 'remove', 'fix', 'refactor',
        'implement', 'write', 'generate', 'build', 'run', 'test', 'deploy'
    ]

    for msg in user_messages:
        content = msg['content'].lower()

        # Extract sentences with action verbs
        for verb in action_verbs:
            # Use word boundaries to capture complete phrases
            pattern = rf'\b{verb}\b\s+([a-zA-Z\s-]{{' + str(CONFIG['ACTION_CONTEXT_MIN_LEN']) + ',' + str(CONFIG['ACTION_CONTEXT_MAX_LEN']) + '}})'
            matches = re.findall(pattern, content)

            for match in matches:
                # Clean up the match
                clean_match = re.sub(r'[^\w\s-]', '', match).strip()
                if len(clean_match) > 5:
                    task_patterns[f"{verb} {clean_match}"].append({
                        'session_id': msg['session_id'],
                        'full_content': msg['content'],
                        'timestamp': msg['timestamp']
                    })

    # Find tasks that occur multiple times
    repeated_tasks = []

    for task, occurrences in task_patterns.items():
        if len(occurrences) >= min_occurrences:
            repeated_tasks.append({
                'task': task,
                'occurrences': len(occurrences),
                'instances': occurrences
            })

    # Sort by frequency
    repeated_tasks.sort(key=lambda x: x['occurrences'], reverse=True)

    return repeated_tasks


def detect_gotchas(user_messages, assistant_messages):
    """Detect gotchas from conversations about problems/errors."""
    gotchas = []

    # Check user messages for problem reports
    for msg in user_messages:
        content = msg['content']

        for pattern in GOTCHA_PATTERNS:
            matches = pattern.findall(content)
            if matches:
                for match in matches:
                    match_text = match.strip() if isinstance(match, str) else match
                    gotchas.append({
                        'session_id': msg['session_id'],
                        'gotcha': match_text,
                        'context': content,
                        'timestamp': msg['timestamp'],
                        'source': 'user'
                    })

    return gotchas


def analyze_tool_usage(conversations):
    """Analyze which tools are used most frequently."""
    tool_counter = Counter()

    for session in conversations:
        for tool in session['tools_used']:
            tool_counter[tool] += 1

    return tool_counter.most_common(CONFIG['TOP_TOOLS_TO_REPORT'])


def create_knowledge_entry(category, title, content, context='', priority='medium',
                           learned_from='conversation_history', tags=None):
    """Create a knowledge entry in Oracle format."""
    return {
        'id': str(uuid.uuid4()),
        'category': category,
        'priority': priority,
        'title': truncate_text(title, CONFIG['MAX_TITLE_LENGTH']),
        'content': content,
        'context': context,
        'examples': [],
        'learned_from': learned_from,
        'created': datetime.now().isoformat(),
        'last_used': datetime.now().isoformat(),
        'use_count': 1,
        'tags': tags or []
    }


def populate_oracle_knowledge(oracle_path, corrections, preferences, gotchas, repeated_tasks):
    """Populate Oracle knowledge base with extracted data."""
    knowledge_dir = oracle_path / 'knowledge'

    # Ensure knowledge directory exists
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    added_counts = {
        'corrections': 0,
        'preferences': 0,
        'gotchas': 0,
        'patterns': 0
    }

    # Add corrections
    if corrections:
        corrections_file = knowledge_dir / 'corrections.json'
        existing_corrections = ensure_knowledge_file(corrections_file, [])

        for correction in corrections[:CONFIG['TOP_CORRECTIONS_TO_ADD']]:
            # Create entry
            entry = create_knowledge_entry(
                category='correction',
                title=f"Correction: {correction['content']}",
                content=correction['content'],
                context='Extracted from conversation history',
                priority='high',
                learned_from='conversation_history_analyzer',
                tags=['auto-extracted', 'correction']
            )

            existing_corrections.append(entry)
            added_counts['corrections'] += 1

        with open(corrections_file, 'w', encoding='utf-8') as f:
            json.dump(existing_corrections, f, indent=2)

    # Add preferences
    if preferences:
        preferences_file = knowledge_dir / 'preferences.json'
        existing_preferences = ensure_knowledge_file(preferences_file, [])

        # Deduplicate preferences
        seen_preferences = set()

        for pref in preferences:
            pref_text = pref['preference'].lower()

            # Skip if too similar to existing
            if pref_text in seen_preferences:
                continue

            seen_preferences.add(pref_text)

            entry = create_knowledge_entry(
                category='preference',
                title=f"Preference: {pref['preference']}",
                content=pref['preference'],
                context=truncate_text(pref['full_context'], 500),
                priority='medium',
                learned_from='conversation_history_analyzer',
                tags=['auto-extracted', 'preference']
            )

            existing_preferences.append(entry)
            added_counts['preferences'] += 1

            if added_counts['preferences'] >= CONFIG['MAX_PREFERENCES_TO_ADD']:
                break

        with open(preferences_file, 'w', encoding='utf-8') as f:
            json.dump(existing_preferences, f, indent=2)

    # Add gotchas
    if gotchas:
        gotchas_file = knowledge_dir / 'gotchas.json'
        existing_gotchas = ensure_knowledge_file(gotchas_file, [])

        for gotcha in gotchas[:CONFIG['TOP_GOTCHAS_TO_ADD']]:
            entry = create_knowledge_entry(
                category='gotcha',
                title=f"Gotcha: {gotcha['gotcha']}",
                content=gotcha['gotcha'],
                context=truncate_text(gotcha['context'], 500),
                priority='high',
                learned_from='conversation_history_analyzer',
                tags=['auto-extracted', 'gotcha']
            )

            existing_gotchas.append(entry)
            added_counts['gotchas'] += 1

        with open(gotchas_file, 'w', encoding='utf-8') as f:
            json.dump(existing_gotchas, f, indent=2)

    # Add repeated tasks as patterns (automation candidates)
    if repeated_tasks:
        patterns_file = knowledge_dir / 'patterns.json'
        existing_patterns = ensure_knowledge_file(patterns_file, [])

        for task in repeated_tasks[:CONFIG['TOP_TASKS_TO_ADD']]:
            entry = create_knowledge_entry(
                category='pattern',
                title=f"Repeated task: {task['task']}",
                content=f"This task has been performed {task['occurrences']} times. Consider automating it.",
                context='Detected from conversation history analysis',
                priority='medium',
                learned_from='conversation_history_analyzer',
                tags=['auto-extracted', 'automation-candidate', 'repeated-task']
            )

            existing_patterns.append(entry)
            added_counts['patterns'] += 1

        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(existing_patterns, f, indent=2)

    return added_counts


def generate_analysis_report(conversations, corrections, preferences, gotchas,
                             repeated_tasks, tool_usage):
    """Generate a comprehensive analysis report."""
    report = []

    report.append("="*70)
    report.append("Oracle Conversation History Analysis Report")
    report.append("="*70)
    report.append("")

    # Summary
    total_messages = sum(len(c['messages']) for c in conversations)

    report.append(f"Analyzed Conversations: {len(conversations)}")
    report.append(f"Total Messages: {total_messages}")
    report.append("")

    # Corrections
    report.append(f"Corrections Detected: {len(corrections)}")
    if corrections:
        report.append("  Top Corrections:")
        for i, corr in enumerate(corrections[:5], 1):
            snippet = truncate_text(corr['content'].replace('\n', ' '), CONFIG['SNIPPET_LENGTH'])
            report.append(f"    {i}. {snippet}")
    report.append("")

    # Preferences
    report.append(f"User Preferences Detected: {len(preferences)}")
    if preferences:
        report.append("  Sample Preferences:")
        for i, pref in enumerate(preferences[:5], 1):
            snippet = truncate_text(pref['preference'], CONFIG['SNIPPET_LENGTH'])
            report.append(f"    {i}. {snippet}")
    report.append("")

    # Gotchas
    report.append(f"Gotchas/Issues Detected: {len(gotchas)}")
    if gotchas:
        report.append("  Sample Gotchas:")
        for i, gotcha in enumerate(gotchas[:5], 1):
            snippet = truncate_text(str(gotcha['gotcha']), CONFIG['SNIPPET_LENGTH'])
            report.append(f"    {i}. {snippet}")
    report.append("")

    # Repeated Tasks
    report.append(f"Repeated Tasks (Automation Candidates): {len(repeated_tasks)}")
    if repeated_tasks:
        report.append("  Top Repeated Tasks:")
        for i, task in enumerate(repeated_tasks[:5], 1):
            report.append(f"    {i}. {task['task']} (x{task['occurrences']})")
    report.append("")

    # Tool Usage
    report.append("Most Used Tools:")
    for i, (tool, count) in enumerate(tool_usage[:10], 1):
        report.append(f"  {i}. {tool}: {count} times")
    report.append("")

    report.append("="*70)

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze Claude Code conversation history',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_history.py --auto-populate
  python analyze_history.py --project-hash abc123def456
  python analyze_history.py --all-projects --recent-days 30
  python analyze_history.py --analyze-only --min-confidence 0.8
        """
    )

    parser.add_argument(
        '--project-hash',
        help='Specific project hash to analyze'
    )

    parser.add_argument(
        '--all-projects',
        action='store_true',
        help='Analyze all projects (not recommended - may be slow)'
    )

    parser.add_argument(
        '--recent-days',
        type=int,
        help='Only analyze conversations from last N days'
    )

    parser.add_argument(
        '--auto-populate',
        action='store_true',
        help='Automatically populate Oracle knowledge base'
    )

    parser.add_argument(
        '--analyze-only',
        action='store_true',
        help='Only analyze and report, do not populate Oracle'
    )

    parser.add_argument(
        '--min-task-occurrences',
        type=int,
        default=CONFIG['DEFAULT_MIN_TASK_OCCURRENCES'],
        help='Minimum occurrences to consider a task as repeated'
    )

    args = parser.parse_args()

    # Find Oracle
    oracle_path = find_oracle_root()

    if not oracle_path and not args.analyze_only:
        print("[ERROR] .oracle directory not found.")
        print("   Run: python .claude/skills/oracle/scripts/init_oracle.py")
        sys.exit(1)

    # Determine project hash
    if args.project_hash:
        project_hash = args.project_hash
    elif oracle_path:
        project_hash = find_project_hash(oracle_path)
        if not project_hash:
            print("[ERROR] Could not determine project hash.")
            print("   Use --project-hash to specify manually")
            sys.exit(1)
    else:
        print("[ERROR] Please specify --project-hash")
        sys.exit(1)

    print(f"\n[INFO] Analyzing project: {project_hash[:8]}...")
    print(f"[INFO] Claude projects path: {CLAUDE_PROJECTS_PATH}\n")

    # Load conversations
    conversations = load_conversation_history(project_hash, args.recent_days)

    if not conversations:
        print("[ERROR] No conversations found.")
        sys.exit(1)  # Exit with error code

    # Extract messages
    print("[INFO] Extracting user and assistant messages...")
    user_messages = extract_messages_by_role(conversations, role='user')
    assistant_messages = extract_messages_by_role(conversations, role='assistant')

    print(f"[OK] Found {len(user_messages)} user messages")
    print(f"[OK] Found {len(assistant_messages)} assistant messages\n")

    # Analyze
    print("[INFO] Detecting corrections...")
    corrections = detect_corrections(user_messages)

    print("[INFO] Detecting preferences...")
    preferences = detect_preferences(user_messages)

    print("[INFO] Detecting gotchas...")
    gotchas = detect_gotchas(user_messages, assistant_messages)

    print("[INFO] Detecting repeated tasks...")
    repeated_tasks = detect_repeated_tasks(user_messages, args.min_task_occurrences)

    print("[INFO] Analyzing tool usage...")
    tool_usage = analyze_tool_usage(conversations)

    print("")

    # Generate report
    report = generate_analysis_report(
        conversations, corrections, preferences, gotchas,
        repeated_tasks, tool_usage
    )

    print(report)

    # Populate Oracle if requested
    if args.auto_populate and oracle_path and not args.analyze_only:
        print("\n[INFO] Populating Oracle knowledge base...")

        added_counts = populate_oracle_knowledge(
            oracle_path, corrections, preferences, gotchas, repeated_tasks
        )

        print("\n[OK] Knowledge base updated:")
        for category, count in added_counts.items():
            if count > 0:
                print(f"   {category.capitalize()}: +{count} entries")

        print("\n[OK] Analysis complete! Knowledge base has been updated.")
        print("   Query knowledge: python .claude/skills/oracle/scripts/query_knowledge.py")

    elif args.analyze_only:
        print("\n[INFO] Analysis complete (no changes made to Oracle)")


if __name__ == '__main__':
    main()
