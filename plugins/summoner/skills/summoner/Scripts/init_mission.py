#!/usr/bin/env python3
"""
Mission Control Document Initializer

This script creates a new Mission Control Document from the template
with proper naming and initial metadata.

Usage:
    python init_mission.py "Task Name" [output_dir]

Example:
    python init_mission.py "Add User Authentication"
    python init_mission.py "Refactor API Layer" ./missions
"""

import sys
import os
from datetime import datetime
from pathlib import Path


def slugify(text):
    """Convert text to a safe filename slug."""
    # Remove special characters and replace spaces with hyphens
    slug = text.lower()
    slug = ''.join(c if c.isalnum() or c in ' -_' else '' for c in slug)
    slug = '-'.join(slug.split())
    return slug


def create_mission_control(task_name, output_dir='.'):
    """Create a new Mission Control Document."""

    # Load template
    template_path = Path(__file__).parent.parent / 'References' / 'mission-control-template.md'

    if not template_path.exists():
        print(f"❌ Error: Template not found at {template_path}")
        return False

    with open(template_path, 'r') as f:
        template = f.read()

    # Replace placeholders
    date_str = datetime.now().strftime('%Y-%m-%d')
    content = template.replace('[TASK NAME]', task_name)
    content = content.replace('[DATE]', date_str)
    content = content.replace('[Planning | In Progress | Integration | Complete]', 'Planning')

    # Create output filename
    slug = slugify(task_name)
    filename = f"mission-{slug}.md"
    output_path = Path(output_dir) / filename

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write file
    with open(output_path, 'w') as f:
        f.write(content)

    print(f"✅ Mission Control Document created: {output_path}")
    print(f"\n📋 Next steps:")
    print(f"   1. Open {output_path}")
    print(f"   2. Fill in Executive Summary and Context")
    print(f"   3. Define Success Criteria")
    print(f"   4. Break down into Tasks")
    print(f"   5. Summon agents and begin orchestration!")

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python init_mission.py \"Task Name\" [output_dir]")
        print("\nExample:")
        print("  python init_mission.py \"Add User Authentication\"")
        print("  python init_mission.py \"Refactor API Layer\" ./missions")
        sys.exit(1)

    task_name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'

    success = create_mission_control(task_name, output_dir)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
