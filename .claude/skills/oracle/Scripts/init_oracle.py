#!/usr/bin/env python3
"""
Oracle Initialization Script

Initializes the Oracle knowledge management system for a project.
Creates directory structure and base files.

Usage:
    python init_oracle.py [--path /path/to/project]

Example:
    python init_oracle.py
    python init_oracle.py --path ~/my-project
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


ORACLE_STRUCTURE = {
    'knowledge': {
        'patterns.json': [],
        'preferences.json': [],
        'gotchas.json': [],
        'solutions.json': [],
        'corrections.json': []
    },
    'sessions': {},
    'timeline': {
        'project_timeline.md': '# Project Timeline\n\nChronological history of project development.\n\n'
    },
    'scripts': {},
    'hooks': {}
}

INDEX_TEMPLATE = {
    'created': None,
    'last_updated': None,
    'total_entries': 0,
    'categories': {
        'patterns': 0,
        'preferences': 0,
        'gotchas': 0,
        'solutions': 0,
        'corrections': 0
    },
    'sessions': [],
    'version': '1.0'
}


def create_oracle_structure(base_path):
    """Create Oracle directory structure."""
    oracle_path = Path(base_path) / '.oracle'

    if oracle_path.exists():
        response = input(f"⚠️  Oracle already exists at {oracle_path}. Reinitialize? [y/N]: ")
        if response.lower() != 'y':
            print("❌ Initialization cancelled.")
            return False

    print(f"📁 Creating Oracle structure at {oracle_path}")

    # Create directories and files
    for dir_name, contents in ORACLE_STRUCTURE.items():
        dir_path = oracle_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created {dir_name}/")

        # Create files in directory
        for filename, content in contents.items():
            file_path = dir_path / filename

            if filename.endswith('.json'):
                with open(file_path, 'w') as f:
                    json.dump(content, f, indent=2)
            else:
                with open(file_path, 'w') as f:
                    f.write(content)

            print(f"      📄 Created {filename}")

    # Create index.json
    index_data = INDEX_TEMPLATE.copy()
    index_data['created'] = datetime.now().isoformat()
    index_data['last_updated'] = datetime.now().isoformat()

    with open(oracle_path / 'index.json', 'w') as f:
        json.dump(index_data, f, indent=2)

    print(f"   ✅ Created index.json")

    # Create README
    readme_content = """# Oracle Knowledge Base

This directory contains the Oracle knowledge management system for this project.

## Structure

- `knowledge/`: Categorized knowledge entries
  - `patterns.json`: Code patterns and conventions
  - `preferences.json`: User/team preferences
  - `gotchas.json`: Known issues and pitfalls
  - `solutions.json`: Proven solutions
  - `corrections.json`: Historical corrections
- `sessions/`: Session logs by date
- `timeline/`: Chronological project history
- `scripts/`: Auto-generated automation scripts
- `hooks/`: Integration hooks
- `index.json`: Fast lookup index

## Usage

See `.claude/skills/oracle/README.md` for complete documentation.

## Quick Commands

```bash
# Query knowledge
python .claude/skills/oracle/Scripts/query_knowledge.py "search term"

# Record session
python .claude/skills/oracle/Scripts/record_session.py

# Generate context
python .claude/skills/oracle/Scripts/generate_context.py

# Analyze patterns
python .claude/skills/oracle/Scripts/analyze_patterns.py
```

---

*Initialized: {}*
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    with open(oracle_path / 'README.md', 'w') as f:
        f.write(readme_content)

    print(f"   ✅ Created README.md")

    # Create .gitignore
    gitignore_content = """# Session logs may contain sensitive information
sessions/*.md

# Keep the structure
!sessions/.gitkeep

# Generated scripts
scripts/*
!scripts/.gitkeep
!scripts/README.md
"""

    with open(oracle_path / '.gitignore', 'w') as f:
        f.write(gitignore_content)

    # Create .gitkeep files
    (oracle_path / 'sessions' / '.gitkeep').touch()
    (oracle_path / 'scripts' / '.gitkeep').touch()
    (oracle_path / 'hooks' / '.gitkeep').touch()

    print(f"   ✅ Created .gitignore")

    return oracle_path


def create_integration_hints(oracle_path, project_path):
    """Create hints for integrating Oracle."""
    print("\n" + "="*70)
    print("🎉 Oracle Initialized Successfully!")
    print("="*70)

    print(f"\n📍 Location: {oracle_path}")

    print("\n📚 Next Steps:\n")

    print("1. **Add to claude.md** (if you have one):")
    print("   Add this section to your project's claude.md:")
    print("""
   ## Project Knowledge (Oracle)

   <!-- ORACLE_CONTEXT_START -->
   Run: python .claude/skills/oracle/Scripts/generate_context.py --session-start
   <!-- ORACLE_CONTEXT_END -->
   """)

    print("\n2. **Create Session Start Hook** (optional):")
    print(f"   Create: {project_path}/.claude/hooks/session-start.sh")
    print("""
   #!/bin/bash
   python .claude/skills/oracle/Scripts/load_context.py
   """)

    print("\n3. **Start Recording Knowledge:**")
    print("   After sessions, run:")
    print("   python .claude/skills/oracle/Scripts/record_session.py")

    print("\n4. **Query Knowledge:**")
    print("   python .claude/skills/oracle/Scripts/query_knowledge.py \"search term\"")

    print("\n" + "="*70)
    print("Oracle is ready to learn and remember! 🧠")
    print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Initialize Oracle knowledge management system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python init_oracle.py
  python init_oracle.py --path ~/my-project
        """
    )

    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='Path to project root (default: current directory)'
    )

    args = parser.parse_args()

    project_path = Path(args.path).resolve()

    if not project_path.exists():
        print(f"❌ Error: Path does not exist: {project_path}")
        sys.exit(1)

    print(f"🚀 Initializing Oracle for project at: {project_path}\n")

    oracle_path = create_oracle_structure(project_path)

    if oracle_path:
        create_integration_hints(oracle_path, project_path)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
