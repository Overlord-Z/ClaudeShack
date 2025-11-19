#!/usr/bin/env python3
"""
Oracle Pattern Analysis Script

Analyze Oracle knowledge base and session logs to identify:
- Repeated tasks (candidates for automation)
- Common corrections (update defaults/documentation)
- Frequent queries (add to auto-inject context)
- Token-heavy operations (automate)

Usage:
    python analyze_patterns.py
    python analyze_patterns.py --generate-scripts
    python analyze_patterns.py --threshold 3

Examples:
    python analyze_patterns.py
    python analyze_patterns.py --generate-scripts --threshold 5
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict
import re


def find_oracle_root():
    """Find the .oracle directory."""
    current = Path.cwd()

    while current != current.parent:
        oracle_path = current / '.oracle'
        if oracle_path.exists():
            return oracle_path
        current = current.parent

    return None


def load_all_sessions(oracle_path):
    """Load all session logs."""
    sessions_dir = oracle_path / 'sessions'
    sessions = []

    for session_file in sessions_dir.glob('*.md'):
        try:
            with open(session_file, 'r') as f:
                content = f.read()
                sessions.append({
                    'id': session_file.stem,
                    'file': session_file,
                    'content': content
                })
        except Exception as e:
            print(f"Warning: Could not read {session_file}: {e}")

    return sessions


def analyze_repeated_activities(sessions):
    """Find repeated activities across sessions."""
    all_activities = []

    for session in sessions:
        # Extract activities from session log
        content = session['content']
        if '## Activities' in content:
            activities_section = content.split('## Activities')[1].split('\n\n')[0]
            activities = re.findall(r'^- (.+)$', activities_section, re.MULTILINE)
            all_activities.extend(activities)

    # Count occurrences
    activity_counts = Counter(all_activities)

    return activity_counts


def analyze_corrections(oracle_path):
    """Analyze correction patterns."""
    knowledge_dir = oracle_path / 'knowledge'
    corrections_file = knowledge_dir / 'corrections.json'

    if not corrections_file.exists():
        return {}

    with open(corrections_file, 'r') as f:
        corrections = json.load(f)

    # Group by common themes
    themes = defaultdict(list)

    for correction in corrections:
        content = correction.get('content', '')

        # Try to identify theme
        if 'async' in content.lower() or 'await' in content.lower():
            themes['async-programming'].append(correction)
        elif 'security' in content.lower() or 'xss' in content.lower() or 'injection' in content.lower():
            themes['security'].append(correction)
        elif 'performance' in content.lower() or 'optimization' in content.lower():
            themes['performance'].append(correction)
        elif 'test' in content.lower():
            themes['testing'].append(correction)
        else:
            themes['general'].append(correction)

    return themes


def analyze_file_patterns(sessions):
    """Analyze which files are changed most often."""
    file_changes = Counter()

    for session in sessions:
        content = session['content']
        if '## Changes Made' in content:
            # Extract file paths
            files = re.findall(r'\*\*File\*\*: `([^`]+)`', content)
            file_changes.update(files)

    return file_changes


def identify_automation_candidates(activity_counts, threshold=3):
    """Identify tasks that are repeated enough to warrant automation."""
    candidates = []

    for activity, count in activity_counts.items():
        if count >= threshold:
            # Analyze if it's automatable
            automation_score = 0

            # Keyword-based scoring
            deterministic_keywords = ['run tests', 'build', 'lint', 'format', 'deploy', 'update dependencies']
            for keyword in deterministic_keywords:
                if keyword in activity.lower():
                    automation_score += 2

            if automation_score > 0 or count >= threshold * 2:
                candidates.append({
                    'activity': activity,
                    'count': count,
                    'automation_score': automation_score,
                    'confidence': 'high' if automation_score >= 2 else 'medium'
                })

    return sorted(candidates, key=lambda x: (x['automation_score'], x['count']), reverse=True)


def generate_automation_script(activity):
    """Generate a basic automation script for an activity."""
    activity_lower = activity.lower()

    script_name = re.sub(r'[^a-z0-9]+', '_', activity_lower).strip('_')
    script_name = f"auto_{script_name}.sh"

    # Basic script template
    script = f"""#!/bin/bash
# Auto-generated by Oracle Pattern Analysis
# Purpose: {activity}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

set -e  # Exit on error

echo "🤖 Automated task: {activity}"
echo "---"

# TODO: Implement automation logic
# Based on the activity pattern, add appropriate commands here

"""

    # Add common commands based on keywords
    if 'test' in activity_lower:
        script += """# Run tests
# npm test
# pytest
# cargo test
"""
    elif 'build' in activity_lower:
        script += """# Build project
# npm run build
# cargo build
# make
"""
    elif 'lint' in activity_lower:
        script += """# Run linter
# npm run lint
# cargo clippy
# pylint
"""
    elif 'format' in activity_lower:
        script += """# Format code
# npm run format
# cargo fmt
# black .
"""

    script += """
echo "---"
echo "✅ Completed: {activity}"
""".format(activity=activity)

    return script_name, script


def generate_report(oracle_path, sessions, threshold):
    """Generate analysis report."""
    print("="*70)
    print("🔍 Oracle Pattern Analysis Report")
    print("="*70)
    print(f"\nAnalyzing {len(sessions)} sessions\n")

    # Repeated activities
    print("## Repeated Activities\n")
    activity_counts = analyze_repeated_activities(sessions)

    if activity_counts:
        print("Top repeated tasks:\n")
        for activity, count in activity_counts.most_common(10):
            emoji = "🔁" if count >= threshold else "📋"
            print(f"  {emoji} [{count}x] {activity}")
    else:
        print("  No repeated activities found\n")

    print()

    # Automation candidates
    print("## Automation Opportunities\n")
    candidates = identify_automation_candidates(activity_counts, threshold)

    if candidates:
        print(f"Found {len(candidates)} automation candidates:\n")
        for candidate in candidates:
            confidence_emoji = "🟢" if candidate['confidence'] == 'high' else "🟡"
            print(f"  {confidence_emoji} [{candidate['count']}x] {candidate['activity']}")
            print(f"      Confidence: {candidate['confidence']}, Score: {candidate['automation_score']}\n")
    else:
        print(f"  No automation candidates (threshold: {threshold} occurrences)\n")

    print()

    # Correction patterns
    print("## Correction Patterns\n")
    correction_themes = analyze_corrections(oracle_path)

    if correction_themes:
        print("Corrections by theme:\n")
        for theme, corrections in sorted(correction_themes.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  • {theme.capitalize()}: {len(corrections)} corrections")

        print("\n⚠️  Consider updating documentation or creating safeguards for common themes\n")
    else:
        print("  No corrections recorded yet\n")

    print()

    # File change patterns
    print("## Frequently Modified Files\n")
    file_changes = analyze_file_patterns(sessions)

    if file_changes:
        print("Most frequently changed files:\n")
        for file_path, count in file_changes.most_common(10):
            print(f"  [{count}x] {file_path}")

        print("\n💡 Consider if these files need refactoring or better structure\n")
    else:
        print("  No file change patterns found\n")

    print()

    # Recommendations
    print("="*70)
    print("📊 Recommendations")
    print("="*70)
    print()

    if candidates:
        print(f"1. **Automate {len(candidates)} repeated tasks**")
        print(f"   Run with --generate-scripts to create automation scripts\n")

    if correction_themes:
        most_common_theme = max(correction_themes.items(), key=lambda x: len(x[1]))[0]
        print(f"2. **Address {most_common_theme} corrections**")
        print(f"   Review and create guidelines or linting rules\n")

    if file_changes:
        top_file = file_changes.most_common(1)[0]
        print(f"3. **Review frequently changed file: {top_file[0]}**")
        print(f"   Changed {top_file[1]} times - may need refactoring\n")

    print("="*70)


def save_automation_scripts(oracle_path, candidates):
    """Generate and save automation scripts."""
    scripts_dir = oracle_path / 'scripts'
    scripts_generated = []

    for candidate in candidates:
        script_name, script_content = generate_automation_script(candidate['activity'])
        script_path = scripts_dir / script_name

        with open(script_path, 'w') as f:
            f.write(script_content)

        # Make executable
        os.chmod(script_path, 0o755)

        scripts_generated.append(script_path)

        print(f"✅ Generated: {script_path}")

    # Create README in scripts dir
    readme_path = scripts_dir / 'README.md'
    readme_content = f"""# Auto-Generated Automation Scripts

These scripts were generated by Oracle pattern analysis on {datetime.now().strftime('%Y-%m-%d')}.

## Scripts

"""

    for candidate in candidates:
        script_name = re.sub(r'[^a-z0-9]+', '_', candidate['activity'].lower()).strip('_')
        readme_content += f"- `auto_{script_name}.sh` - {candidate['activity']} (used {candidate['count']}x)\n"

    readme_content += """
## Usage

Each script is executable:

```bash
./auto_script_name.sh
```

## Customization

These scripts are templates. Review and customize them for your specific needs.
"""

    with open(readme_path, 'w') as f:
        f.write(readme_content)

    print(f"\n📄 Created README: {readme_path}")

    return scripts_generated


def main():
    parser = argparse.ArgumentParser(
        description='Analyze Oracle patterns and identify automation opportunities',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--threshold',
        type=int,
        default=3,
        help='Minimum occurrences to consider for automation (default: 3)'
    )

    parser.add_argument(
        '--generate-scripts',
        action='store_true',
        help='Generate automation scripts for candidates'
    )

    args = parser.parse_args()

    # Find Oracle
    oracle_path = find_oracle_root()

    if not oracle_path:
        print("❌ Error: .oracle directory not found.")
        sys.exit(1)

    # Load sessions
    sessions = load_all_sessions(oracle_path)

    if not sessions:
        print("⚠️  No sessions found. Start recording sessions to enable pattern analysis.")
        sys.exit(0)

    # Generate report
    generate_report(oracle_path, sessions, args.threshold)

    # Generate scripts if requested
    if args.generate_scripts:
        activity_counts = analyze_repeated_activities(sessions)
        candidates = identify_automation_candidates(activity_counts, args.threshold)

        if candidates:
            print("\n" + "="*70)
            print("🤖 Generating Automation Scripts")
            print("="*70 + "\n")

            scripts = save_automation_scripts(oracle_path, candidates)

            print(f"\n🎉 Generated {len(scripts)} automation scripts!")
            print(f"   Location: {oracle_path / 'scripts'}")
            print("\n⚠️  Review and customize these scripts before use.\n")
        else:
            print("\n⚠️  No automation candidates found (threshold: {args.threshold})\n")


if __name__ == '__main__':
    main()
