#!/usr/bin/env python3
"""
ClaudeShack Project Initialization

Initializes ClaudeShack skills in a user's project by:
- Creating/updating claude.md with ClaudeShack context
- Setting up Oracle directory structure
- Creating Guardian config
- Updating .gitignore

Usage:
    python init_project.py [project_path]

    If project_path is not provided, uses current directory.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional


CLAUDE_MD_SECTION = """
## ClaudeShack Skills

This project uses ClaudeShack skills for enhanced development:

### Available Skills
- **Oracle**: Project memory and learning (tracks patterns, corrections, knowledge)
- **Guardian**: Quality gates and session health monitoring (auto code review)
- **Summoner**: Multi-agent orchestration (complex task breakdown)
- **Wizard**: Documentation maintenance (no hallucinations, fact-checked)
- **Style Master**: CSS and frontend styling expert
- **Evaluator**: Privacy-first telemetry (opt-in, anonymous)

### Core Principles
- **KISS**: Keep it simple, avoid complexity
- **DRY**: Don't repeat yourself
- **Privacy First**: No PII, opt-in telemetry only
- **Minimal Context**: Pass only what's needed to subagents
- **Facts Over Fiction**: Documentation verified against code

### Quick Start

**Use Skills**:
- `use oracle to remember this pattern`
- `use guardian to review this code`
- `use summoner to coordinate [complex task]`
- `use wizard to update documentation`

**Session Handoff** (when context degrades):
- `/handoff` - Smooth transition to fresh session with context preserved

### Guardian Auto-Triggers
Guardian automatically activates when:
- >50 lines of code written
- Same error 3+ times
- Same file edited 5+ times in 10 minutes
- Multiple corrections needed

### Integration Benefits
- Guardian + Oracle: +31% suggestion acceptance
- Wizard + Oracle: +19% doc accuracy
- Style Master + Oracle: +22% consistency

For full documentation: https://github.com/Overlord-Z/ClaudeShack
"""

GITIGNORE_ENTRIES = """
# ClaudeShack (project-specific knowledge and session data)
.oracle/
.guardian/
.summoner/mcds/
"""

GUARDIAN_CONFIG = {
    "enabled": True,
    "sensitivity": {
        "lines_threshold": 50,
        "error_repeat_threshold": 3,
        "file_churn_threshold": 5,
        "correction_threshold": 3,
        "context_warning_percent": 0.7
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


def init_oracle(project_path: Path) -> None:
    """Initialize Oracle directory structure."""
    oracle_dir = project_path / '.oracle'

    # Create directory structure
    (oracle_dir / 'knowledge').mkdir(parents=True, exist_ok=True)
    (oracle_dir / 'sessions').mkdir(parents=True, exist_ok=True)
    (oracle_dir / 'timeline').mkdir(parents=True, exist_ok=True)
    (oracle_dir / 'scripts').mkdir(parents=True, exist_ok=True)

    # Create empty knowledge files
    knowledge_files = [
        'patterns.json',
        'corrections.json',
        'gotchas.json',
        'solutions.json',
        'preferences.json'
    ]

    for filename in knowledge_files:
        filepath = oracle_dir / 'knowledge' / filename
        if not filepath.exists():
            with open(filepath, 'w') as f:
                json.dump([], f, indent=2)

    # Create index
    index_file = oracle_dir / 'index.json'
    if not index_file.exists():
        with open(index_file, 'w') as f:
            json.dump({
                'version': '0.1.0-beta',
                'created': None,  # Will be set by Oracle on first use
                'last_updated': None,
                'total_entries': 0
            }, f, indent=2)

    print(f"✅ Oracle initialized at {oracle_dir}")


def init_guardian(project_path: Path) -> None:
    """Initialize Guardian configuration."""
    guardian_dir = project_path / '.guardian'
    guardian_dir.mkdir(parents=True, exist_ok=True)

    config_file = guardian_dir / 'config.json'
    if not config_file.exists():
        with open(config_file, 'w') as f:
            json.dump(GUARDIAN_CONFIG, f, indent=2)
        print(f"✅ Guardian initialized at {guardian_dir}")
    else:
        print(f"ℹ️  Guardian config already exists at {config_file}")


def update_claude_md(project_path: Path) -> None:
    """Create or update claude.md with ClaudeShack section."""
    claude_md = project_path / 'claude.md'

    if claude_md.exists():
        with open(claude_md, 'r') as f:
            content = f.read()

        # Check if ClaudeShack section already exists
        if 'ClaudeShack Skills' in content:
            print(f"ℹ️  claude.md already has ClaudeShack section")
            return

        # Append ClaudeShack section
        with open(claude_md, 'a') as f:
            f.write('\n' + CLAUDE_MD_SECTION)
        print(f"✅ Updated {claude_md} with ClaudeShack section")
    else:
        # Create new claude.md
        with open(claude_md, 'w') as f:
            f.write(f"# {project_path.name} Development Context\n")
            f.write(CLAUDE_MD_SECTION)
        print(f"✅ Created {claude_md} with ClaudeShack context")


def update_gitignore(project_path: Path) -> None:
    """Update .gitignore with ClaudeShack entries."""
    gitignore = project_path / '.gitignore'

    if gitignore.exists():
        with open(gitignore, 'r') as f:
            content = f.read()

        # Check if entries already exist
        if '.oracle/' in content:
            print(f"ℹ️  .gitignore already has ClaudeShack entries")
            return

        # Append entries
        with open(gitignore, 'a') as f:
            f.write('\n' + GITIGNORE_ENTRIES)
        print(f"✅ Updated {gitignore} with ClaudeShack entries")
    else:
        # Create new .gitignore
        with open(gitignore, 'w') as f:
            f.write(GITIGNORE_ENTRIES)
        print(f"✅ Created {gitignore} with ClaudeShack entries")


def main():
    """Main initialization function."""
    # Get project path
    if len(sys.argv) > 1:
        project_path = Path(sys.argv[1]).resolve()
    else:
        project_path = Path.cwd()

    if not project_path.exists():
        print(f"❌ Project path does not exist: {project_path}")
        sys.exit(1)

    print(f"🏛️  Initializing ClaudeShack in: {project_path}\n")

    # Run initialization steps
    try:
        init_oracle(project_path)
        init_guardian(project_path)
        update_claude_md(project_path)
        update_gitignore(project_path)

        print("\n" + "="*70)
        print("✅ ClaudeShack initialization complete!")
        print("="*70)
        print("\nYou can now use ClaudeShack skills:")
        print("  - use oracle to remember this pattern")
        print("  - use guardian to review this code")
        print("  - use summoner to coordinate [complex task]")
        print("  - use wizard to update documentation")
        print("\nOracle will learn as you work - correct mistakes and it remembers!")
        print("\nFor more info: https://github.com/Overlord-Z/ClaudeShack")

    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
