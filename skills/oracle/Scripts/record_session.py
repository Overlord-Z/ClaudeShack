#!/usr/bin/env python3
"""
Oracle Session Recording Script

Record a session's activities, learnings, and corrections to the Oracle knowledge base.

Usage:
    python record_session.py [options]
    python record_session.py --interactive
    python record_session.py --summary "Implemented auth" --learnings "Use bcrypt"

Examples:
    python record_session.py --interactive
    python record_session.py --summary "Fixed bug in API" --corrections "Use async/await not callbacks"
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
import uuid


def find_oracle_root():
    """Find the .oracle directory."""
    current = Path.cwd()

    while current != current.parent:
        oracle_path = current / '.oracle'
        if oracle_path.exists():
            return oracle_path
        current = current.parent

    return None


def generate_session_id():
    """Generate a unique session ID."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    short_uuid = str(uuid.uuid4())[:8]
    return f"{timestamp}_{short_uuid}"


def interactive_session_record():
    """Interactive mode for recording a session."""
    print("="*70)
    print("📝 Oracle Session Recording (Interactive Mode)")
    print("="*70)
    print("\nPress Enter to skip any field.\n")

    session = {}

    # Summary
    session['summary'] = input("Summary of this session:\n> ").strip()

    # Activities
    print("\nActivities (one per line, empty line to finish):")
    activities = []
    while True:
        activity = input("> ").strip()
        if not activity:
            break
        activities.append(activity)
    session['activities'] = activities

    # Changes
    print("\nFiles changed (format: path/to/file.ts, empty line to finish):")
    changes = []
    while True:
        file_path = input("File: ").strip()
        if not file_path:
            break
        change_desc = input("  Change: ").strip()
        reason = input("  Reason: ").strip()
        changes.append({
            'file': file_path,
            'change': change_desc,
            'reason': reason
        })
    session['changes'] = changes

    # Decisions
    print("\nDecisions made (empty line to finish):")
    decisions = []
    while True:
        decision = input("Decision: ").strip()
        if not decision:
            break
        rationale = input("  Rationale: ").strip()
        decisions.append({
            'decision': decision,
            'rationale': rationale
        })
    session['decisions'] = decisions

    # Learnings
    print("\nLearnings (empty line to finish):")
    learnings = []
    while True:
        learning = input("Learning: ").strip()
        if not learning:
            break

        print("  Priority? [critical/high/medium/low]")
        priority = input("  > ").strip() or 'medium'

        learnings.append({
            'content': learning,
            'priority': priority
        })
    session['learnings'] = learnings

    # Corrections
    print("\nCorrections (what was wrong → what's right, empty line to finish):")
    corrections = []
    while True:
        wrong = input("❌ What was wrong: ").strip()
        if not wrong:
            break
        right = input("✓  What's right: ").strip()
        context = input("   When this applies: ").strip()

        corrections.append({
            'wrong': wrong,
            'right': right,
            'context': context
        })
    session['corrections'] = corrections

    # Questions
    print("\nQuestions asked (empty line to finish):")
    questions = []
    while True:
        question = input("Q: ").strip()
        if not question:
            break
        answer = input("A: ").strip()

        questions.append({
            'question': question,
            'answer': answer
        })
    session['questions'] = questions

    return session


def create_session_log(oracle_path, session_id, session_data):
    """Create a session log markdown file."""
    sessions_dir = oracle_path / 'sessions'
    log_file = sessions_dir / f'{session_id}.md'

    content = f"""# Session: {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Session ID**: `{session_id}`

## Summary

{session_data.get('summary', 'No summary provided')}

"""

    # Activities
    if session_data.get('activities'):
        content += "## Activities\n\n"
        for activity in session_data['activities']:
            content += f"- {activity}\n"
        content += "\n"

    # Changes
    if session_data.get('changes'):
        content += "## Changes Made\n\n"
        for change in session_data['changes']:
            content += f"- **File**: `{change['file']}`\n"
            content += f"  - Change: {change['change']}\n"
            if change.get('reason'):
                content += f"  - Reason: {change['reason']}\n"
            content += "\n"

    # Decisions
    if session_data.get('decisions'):
        content += "## Decisions\n\n"
        for decision in session_data['decisions']:
            content += f"- **Decision**: {decision['decision']}\n"
            if decision.get('rationale'):
                content += f"  - Rationale: {decision['rationale']}\n"
            content += "\n"

    # Learnings
    if session_data.get('learnings'):
        content += "## Learnings\n\n"
        for learning in session_data['learnings']:
            priority = learning.get('priority', 'medium')
            priority_emoji = {'critical': '🔴', 'high': '🟡', 'medium': '🔵', 'low': '⚪'}.get(priority, '⚪')
            content += f"- {priority_emoji} **[{priority.upper()}]** {learning['content']}\n"
        content += "\n"

    # Corrections
    if session_data.get('corrections'):
        content += "## Corrections\n\n"
        for correction in session_data['corrections']:
            content += f"- ❌ Wrong: {correction['wrong']}\n"
            content += f"  ✓ Right: {correction['right']}\n"
            if correction.get('context'):
                content += f"  📝 Context: {correction['context']}\n"
            content += "\n"

    # Questions
    if session_data.get('questions'):
        content += "## Questions Asked\n\n"
        for qa in session_data['questions']:
            content += f"- **Q**: {qa['question']}\n"
            content += f"  **A**: {qa['answer']}\n"
            content += "\n"

    content += f"\n---\n\n*Recorded: {datetime.now().isoformat()}*\n"

    with open(log_file, 'w') as f:
        f.write(content)

    return log_file


def update_knowledge_base(oracle_path, session_id, session_data):
    """Update knowledge base with session learnings and corrections."""
    knowledge_dir = oracle_path / 'knowledge'
    updated_categories = set()

    # Add learnings as solutions or patterns
    if session_data.get('learnings'):
        for learning in session_data['learnings']:
            # Determine if it's a pattern or solution based on content
            category = 'solutions'  # Default to solutions

            entry = {
                'id': str(uuid.uuid4()),
                'category': category,
                'priority': learning.get('priority', 'medium'),
                'title': learning['content'][:100],  # Truncate for title
                'content': learning['content'],
                'context': learning.get('context', ''),
                'examples': [],
                'learned_from': session_id,
                'created': datetime.now().isoformat(),
                'last_used': datetime.now().isoformat(),
                'use_count': 1,
                'tags': learning.get('tags', [])
            }

            # Load existing and append
            solutions_file = knowledge_dir / f'{category}.json'
            with open(solutions_file, 'r') as f:
                entries = json.load(f)

            entries.append(entry)

            with open(solutions_file, 'w') as f:
                json.dump(entries, f, indent=2)

            updated_categories.add(category)

    # Add corrections
    if session_data.get('corrections'):
        corrections_file = knowledge_dir / 'corrections.json'

        with open(corrections_file, 'r') as f:
            corrections = json.load(f)

        for correction in session_data['corrections']:
            entry = {
                'id': str(uuid.uuid4()),
                'category': 'correction',
                'priority': 'high',  # Corrections are high priority
                'title': f"Don't: {correction['wrong'][:50]}...",
                'content': f"❌ Wrong: {correction['wrong']}\n✓ Right: {correction['right']}",
                'context': correction.get('context', ''),
                'examples': [],
                'learned_from': session_id,
                'created': datetime.now().isoformat(),
                'last_used': datetime.now().isoformat(),
                'use_count': 1,
                'tags': []
            }

            corrections.append(entry)

        with open(corrections_file, 'w') as f:
            json.dump(corrections, f, indent=2)

        updated_categories.add('corrections')

    return updated_categories


def update_index(oracle_path, session_id):
    """Update the index with new session."""
    index_file = oracle_path / 'index.json'

    with open(index_file, 'r') as f:
        index = json.load(f)

    # Add session to list
    if session_id not in index['sessions']:
        index['sessions'].append(session_id)

    # Update counts
    knowledge_dir = oracle_path / 'knowledge'
    for category in ['patterns', 'preferences', 'gotchas', 'solutions', 'corrections']:
        category_file = knowledge_dir / f'{category}.json'
        with open(category_file, 'r') as f:
            entries = json.load(f)
            index['categories'][category] = len(entries)
            index['total_entries'] += len(entries)

    # Update timestamp
    index['last_updated'] = datetime.now().isoformat()

    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)


def update_timeline(oracle_path, session_id, session_data):
    """Update project timeline."""
    timeline_file = oracle_path / 'timeline' / 'project_timeline.md'

    entry = f"""
## {datetime.now().strftime('%Y-%m-%d %H:%M')} - {session_data.get('summary', 'Session recorded')}

**Session ID**: `{session_id}`

"""

    if session_data.get('activities'):
        entry += "**Activities**:\n"
        for activity in session_data['activities'][:3]:  # Top 3
            entry += f"- {activity}\n"
        if len(session_data['activities']) > 3:
            entry += f"- ... and {len(session_data['activities']) - 3} more\n"
        entry += "\n"

    if session_data.get('learnings'):
        entry += f"**Key Learnings**: {len(session_data['learnings'])}\n\n"

    if session_data.get('corrections'):
        entry += f"**Corrections Made**: {len(session_data['corrections'])}\n\n"

    entry += "---\n"

    # Append to timeline
    with open(timeline_file, 'a') as f:
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(
        description='Record Oracle session',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode with prompts'
    )

    parser.add_argument(
        '--summary',
        help='Session summary'
    )

    parser.add_argument(
        '--learnings',
        help='Learnings (semicolon-separated)'
    )

    parser.add_argument(
        '--corrections',
        help='Corrections in format "wrong->right" (semicolon-separated)'
    )

    args = parser.parse_args()

    # Find Oracle
    oracle_path = find_oracle_root()

    if not oracle_path:
        print("❌ Error: .oracle directory not found.")
        print("   Run: python .claude/skills/oracle/Scripts/init_oracle.py")
        sys.exit(1)

    # Get session data
    if args.interactive:
        session_data = interactive_session_record()
    else:
        session_data = {
            'summary': args.summary or '',
            'activities': [],
            'changes': [],
            'decisions': [],
            'learnings': [],
            'corrections': [],
            'questions': []
        }

        if args.learnings:
            for learning in args.learnings.split(';'):
                session_data['learnings'].append({
                    'content': learning.strip(),
                    'priority': 'medium'
                })

        if args.corrections:
            for correction in args.corrections.split(';'):
                if '->' in correction:
                    wrong, right = correction.split('->', 1)
                    session_data['corrections'].append({
                        'wrong': wrong.strip(),
                        'right': right.strip(),
                        'context': ''
                    })

    # Generate session ID
    session_id = generate_session_id()

    print(f"\n📝 Recording session: {session_id}\n")

    # Create session log
    log_file = create_session_log(oracle_path, session_id, session_data)
    print(f"✅ Session log created: {log_file}")

    # Update knowledge base
    updated_categories = update_knowledge_base(oracle_path, session_id, session_data)
    if updated_categories:
        print(f"✅ Knowledge base updated: {', '.join(updated_categories)}")

    # Update timeline
    update_timeline(oracle_path, session_id, session_data)
    print(f"✅ Timeline updated")

    # Update index
    update_index(oracle_path, session_id)
    print(f"✅ Index updated")

    print(f"\n🎉 Session recorded successfully!\n")
    print(f"View log: {log_file}")
    print(f"Query knowledge: python .claude/skills/oracle/Scripts/query_knowledge.py\n")


if __name__ == '__main__':
    main()
