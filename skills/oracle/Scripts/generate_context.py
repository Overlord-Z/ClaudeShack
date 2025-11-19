#!/usr/bin/env python3
"""
Oracle Context Generation Script

Generate context summaries from Oracle knowledge base for injection into
claude.md, session starts, or specific tasks.

Usage:
    python generate_context.py --session-start
    python generate_context.py --task "implement API"
    python generate_context.py --output claude.md
    python generate_context.py --tier 1

Examples:
    python generate_context.py --session-start
    python generate_context.py --task "database migration" --tier 2
    python generate_context.py --output ../claude.md --update
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


def find_oracle_root():
    """Find the .oracle directory."""
    current = Path.cwd()

    while current != current.parent:
        oracle_path = current / '.oracle'
        if oracle_path.exists():
            return oracle_path
        current = current.parent

    return None


def load_all_knowledge(oracle_path):
    """Load all knowledge from Oracle."""
    knowledge_dir = oracle_path / 'knowledge'
    all_knowledge = []

    for category in ['patterns', 'preferences', 'gotchas', 'solutions', 'corrections']:
        file_path = knowledge_dir / f'{category}.json'
        if file_path.exists():
            with open(file_path, 'r') as f:
                entries = json.load(f)
                for entry in entries:
                    entry['_category'] = category
                    all_knowledge.append(entry)

    return all_knowledge


def filter_by_tier(knowledge, tier=1):
    """Filter knowledge by tier level."""
    if tier == 1:
        # Critical only - always load
        return [k for k in knowledge if k.get('priority') in ['critical', 'high']]
    elif tier == 2:
        # Medium priority - load on relevance
        return [k for k in knowledge if k.get('priority') in ['critical', 'high', 'medium']]
    else:
        # All knowledge
        return knowledge


def filter_by_relevance(knowledge, task_description):
    """Filter knowledge relevant to a specific task."""
    if not task_description:
        return knowledge

    task_lower = task_description.lower()
    relevant = []

    for entry in knowledge:
        # Check if task keywords appear in entry
        score = 0

        if task_lower in entry.get('title', '').lower():
            score += 3
        if task_lower in entry.get('content', '').lower():
            score += 2
        if task_lower in entry.get('context', '').lower():
            score += 1

        # Check tags
        for tag in entry.get('tags', []):
            if tag.lower() in task_lower or task_lower in tag.lower():
                score += 2

        if score > 0:
            entry['_relevance_score'] = score
            relevant.append(entry)

    # Sort by relevance
    return sorted(relevant, key=lambda x: x.get('_relevance_score', 0), reverse=True)


def get_recent_corrections(oracle_path, limit=5):
    """Get most recent corrections."""
    knowledge_dir = oracle_path / 'knowledge'
    corrections_file = knowledge_dir / 'corrections.json'

    if not corrections_file.exists():
        return []

    with open(corrections_file, 'r') as f:
        corrections = json.load(f)

    # Sort by creation date
    sorted_corrections = sorted(
        corrections,
        key=lambda x: x.get('created', ''),
        reverse=True
    )

    return sorted_corrections[:limit]


def generate_session_start_context(oracle_path):
    """Generate context for session start."""
    knowledge = load_all_knowledge(oracle_path)

    # Tier 1: Critical items
    critical_items = filter_by_tier(knowledge, tier=1)

    # Recent corrections
    recent_corrections = get_recent_corrections(oracle_path, limit=5)

    context = """# Oracle Project Knowledge

*Auto-generated context for this session*

"""

    # Project Overview
    index_file = oracle_path / 'index.json'
    if index_file.exists():
        with open(index_file, 'r') as f:
            index = json.load(f)

        context += f"""## Project Status

- Total Knowledge Entries: {index.get('total_entries', 0)}
- Last Updated: {index.get('last_updated', 'Unknown')}
- Sessions Recorded: {len(index.get('sessions', []))}

"""

    # Critical Knowledge
    if critical_items:
        context += "## ⚠️  Critical Knowledge\n\n"

        for item in critical_items[:10]:  # Top 10
            context += f"### {item.get('title', 'Untitled')}\n\n"
            context += f"**Category**: {item['_category'].capitalize()} | **Priority**: {item.get('priority', 'N/A')}\n\n"
            context += f"{item.get('content', 'No content')}\n\n"

            if item.get('context'):
                context += f"*When to apply*: {item['context']}\n\n"

            context += "---\n\n"

    # Recent Corrections
    if recent_corrections:
        context += "## 🔄 Recent Corrections (Learn from these!)\n\n"

        for correction in recent_corrections:
            context += f"- **{correction.get('title', 'Correction')}**\n"
            context += f"  {correction.get('content', '')}\n"

            if correction.get('context'):
                context += f"  *Context*: {correction['context']}\n"

            context += "\n"

    context += f"\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

    return context


def generate_task_context(oracle_path, task_description):
    """Generate context for a specific task."""
    knowledge = load_all_knowledge(oracle_path)

    # Filter by relevance to task
    relevant = filter_by_relevance(knowledge, task_description)

    context = f"""# Oracle Context for: {task_description}

*Relevant knowledge from Oracle*

"""

    if not relevant:
        context += "No specific knowledge found for this task.\n\n"
        context += "This might be a new area - remember to record learnings!\n"
        return context

    context += f"Found {len(relevant)} relevant knowledge entries.\n\n"

    # Group by category
    by_category = {}
    for item in relevant[:20]:  # Top 20 most relevant
        category = item['_category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(item)

    # Format by category
    category_names = {
        'patterns': '📐 Patterns',
        'preferences': '⚙️  Preferences',
        'gotchas': '⚠️  Gotchas',
        'solutions': '✅ Solutions',
        'corrections': '🔄 Corrections'
    }

    for category, items in by_category.items():
        context += f"## {category_names.get(category, category.capitalize())}\n\n"

        for item in items:
            context += f"### {item.get('title', 'Untitled')}\n\n"
            context += f"{item.get('content', 'No content')}\n\n"

            if item.get('examples'):
                context += "**Examples**:\n"
                for ex in item['examples']:
                    context += f"- {ex}\n"
                context += "\n"

            context += "---\n\n"

    context += f"\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

    return context


def generate_compact_context(oracle_path):
    """Generate compact context for claude.md injection."""
    knowledge = load_all_knowledge(oracle_path)

    critical = [k for k in knowledge if k.get('priority') == 'critical']
    high = [k for k in knowledge if k.get('priority') == 'high']

    context = "<!-- ORACLE_CONTEXT_START -->\n"
    context += "<!-- Auto-generated by Oracle - Do not edit manually -->\n\n"

    if critical:
        context += "**Critical Knowledge**:\n"
        for item in critical[:5]:
            context += f"- {item.get('title', 'Untitled')}\n"
        context += "\n"

    if high:
        context += "**Important Patterns**:\n"
        for item in high[:5]:
            context += f"- {item.get('title', 'Untitled')}\n"
        context += "\n"

    # Recent corrections
    recent_corrections = get_recent_corrections(oracle_path, limit=3)
    if recent_corrections:
        context += "**Recent Learnings**:\n"
        for correction in recent_corrections:
            content = correction.get('content', '')
            # Extract just the "right" part if it's a correction
            if '✓ Right:' in content:
                right_part = content.split('✓ Right:')[1].split('\n')[0].strip()
                context += f"- {right_part}\n"
            else:
                context += f"- {correction.get('title', '')}\n"
        context += "\n"

    context += f"*Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    context += "<!-- ORACLE_CONTEXT_END -->\n"

    return context


def update_claude_md(oracle_path, project_path):
    """Update claude.md with Oracle context."""
    claude_md = project_path / 'claude.md'

    context = generate_compact_context(oracle_path)

    if not claude_md.exists():
        # Create new claude.md with Oracle section
        content = f"""# Project Documentation

## Project Knowledge (Oracle)

{context}

## Additional Context

[Add your project-specific context here]
"""
        with open(claude_md, 'w') as f:
            f.write(content)

        print(f"✅ Created new claude.md with Oracle context")
        return

    # Update existing claude.md
    with open(claude_md, 'r') as f:
        content = f.read()

    # Replace Oracle section if it exists
    if '<!-- ORACLE_CONTEXT_START -->' in content:
        import re
        pattern = r'<!-- ORACLE_CONTEXT_START -->.*?<!-- ORACLE_CONTEXT_END -->'
        content = re.sub(pattern, context, content, flags=re.DOTALL)
        print(f"✅ Updated Oracle context in claude.md")
    else:
        # Add Oracle section at the top
        content = f"## Project Knowledge (Oracle)\n\n{context}\n\n{content}"
        print(f"✅ Added Oracle context to claude.md")

    with open(claude_md, 'w') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Oracle context summaries',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--session-start',
        action='store_true',
        help='Generate context for session start'
    )

    parser.add_argument(
        '--task',
        help='Generate context for specific task'
    )

    parser.add_argument(
        '--tier',
        type=int,
        choices=[1, 2, 3],
        default=1,
        help='Context tier level (1=critical, 2=medium, 3=all)'
    )

    parser.add_argument(
        '--output',
        help='Output file (default: stdout)'
    )

    parser.add_argument(
        '--update',
        action='store_true',
        help='Update the output file (for claude.md)'
    )

    args = parser.parse_args()

    # Find Oracle
    oracle_path = find_oracle_root()

    if not oracle_path:
        print("❌ Error: .oracle directory not found.")
        sys.exit(1)

    # Generate context
    if args.session_start:
        context = generate_session_start_context(oracle_path)
    elif args.task:
        context = generate_task_context(oracle_path, args.task)
    elif args.update and args.output:
        project_path = oracle_path.parent
        update_claude_md(oracle_path, project_path)
        return
    else:
        context = generate_compact_context(oracle_path)

    # Output
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            f.write(context)
        print(f"✅ Context written to: {output_path}")
    else:
        print(context)


if __name__ == '__main__':
    main()
