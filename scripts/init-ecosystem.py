#!/usr/bin/env python3
"""
ClaudeShack Ecosystem Full Initialization

Complete initialization that:
1. Sets up Oracle directory structure
2. Sets up Guardian configuration
3. Mines existing Claude Code conversation history into Oracle
4. Generates session-start context
5. Updates claude.md with Oracle knowledge
6. Provides hook setup instructions

Usage:
    python init-ecosystem.py [project_path]
    python init-ecosystem.py --skip-history   # Skip history mining
    python init-ecosystem.py --verbose        # Detailed output
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

# Get the directory where this script lives
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILLS_DIR = SCRIPT_DIR  # .claude/skills/


def get_platform_settings_path() -> Path:
    """Get Claude Code settings path for the current platform."""
    if sys.platform == 'darwin':  # macOS
        return Path.home() / 'Library' / 'Application Support' / 'Claude' / 'settings.json'
    elif sys.platform == 'win32':  # Windows
        return Path(os.environ.get('APPDATA', '')) / 'Claude' / 'settings.json'
    else:  # Linux
        return Path.home() / '.config' / 'Claude' / 'settings.json'


def run_script(script_path: Path, args: list = None, cwd: Path = None, verbose: bool = False) -> tuple:
    """Run a Python script and return (success, output)."""
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(cwd) if cwd else None,
            timeout=120  # 2 minute timeout
        )
        if verbose:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Script timed out after 120 seconds"
    except Exception as e:
        return False, str(e)


def init_oracle_structure(project_path: Path) -> bool:
    """Initialize Oracle directory structure."""
    print("\n[1/6] Initializing Oracle directory structure...")

    oracle_dir = project_path / '.oracle'

    # Create directory structure
    dirs = ['knowledge', 'sessions', 'timeline', 'scripts', 'hooks']
    for d in dirs:
        (oracle_dir / d).mkdir(parents=True, exist_ok=True)

    # Create empty knowledge files
    knowledge_files = ['patterns.json', 'corrections.json', 'gotchas.json',
                       'solutions.json', 'preferences.json']

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
                'version': '1.0.0',
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'total_entries': 0,
                'sessions_recorded': 0
            }, f, indent=2)

    print(f"   [OK] Oracle structure created at {oracle_dir}")
    return True


def init_guardian_config(project_path: Path) -> bool:
    """Initialize Guardian configuration."""
    print("\n[2/6] Initializing Guardian configuration...")

    guardian_dir = project_path / '.guardian'
    guardian_dir.mkdir(parents=True, exist_ok=True)

    config = {
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

    config_file = guardian_dir / 'config.json'
    if not config_file.exists():
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"   [OK] Guardian config created at {config_file}")
    else:
        print(f"   [OK] Guardian config already exists")

    return True


def mine_conversation_history(project_path: Path, verbose: bool = False) -> bool:
    """Mine existing Claude Code conversation history into Oracle."""
    print("\n[3/6] Mining conversation history into Oracle...")

    analyze_script = SKILLS_DIR / 'oracle' / 'scripts' / 'analyze_history.py'

    if not analyze_script.exists():
        print(f"   [SKIP] analyze_history.py not found")
        return True

    # Check if Claude projects directory exists
    if sys.platform == 'darwin':
        projects_dir = Path.home() / 'Library' / 'Application Support' / 'Claude' / 'projects'
    elif sys.platform == 'win32':
        projects_dir = Path(os.environ.get('APPDATA', '')) / 'Claude' / 'projects'
    else:
        projects_dir = Path.home() / '.claude' / 'projects'

    if not projects_dir.exists():
        print(f"   [SKIP] No conversation history found at {projects_dir}")
        return True

    success, output = run_script(
        analyze_script,
        ['--auto-populate', '--recent-days', '90'],
        cwd=project_path,
        verbose=verbose
    )

    if success:
        print("   [OK] Conversation history mined successfully")
    else:
        print("   [WARN] History mining had issues (non-fatal)")
        if verbose:
            print(f"   Output: {output[:500]}")

    return True  # Non-fatal


def generate_context(project_path: Path, verbose: bool = False) -> bool:
    """Generate session-start context from Oracle knowledge."""
    print("\n[4/6] Generating session-start context...")

    generate_script = SKILLS_DIR / 'oracle' / 'scripts' / 'generate_context.py'

    if not generate_script.exists():
        print(f"   [SKIP] generate_context.py not found")
        return True

    # Check if Oracle has any knowledge
    oracle_dir = project_path / '.oracle'
    if not oracle_dir.exists():
        print("   [SKIP] Oracle not initialized")
        return True

    success, output = run_script(
        generate_script,
        ['--session-start'],
        cwd=project_path,
        verbose=verbose
    )

    if success:
        print("   [OK] Session context generated")
    else:
        print("   [WARN] Context generation had issues (non-fatal)")

    return True


def update_claude_md(project_path: Path) -> bool:
    """Update claude.md with ClaudeShack section and Oracle context."""
    print("\n[5/6] Updating claude.md...")

    claude_md = project_path / 'claude.md'

    claudeshack_section = """
## ClaudeShack Skills

This project uses ClaudeShack skills for enhanced development:

### Available Skills
- **Oracle**: Project memory and learning (tracks patterns, corrections, knowledge)
- **Guardian**: Quality gates and session health monitoring (auto code review)
- **Summoner**: Multi-agent orchestration (complex task breakdown)
- **Wizard**: Documentation maintenance (no hallucinations, fact-checked)
- **Documentation Wizard**: Living documentation that stays in sync with code
- **Style Master**: CSS and frontend styling expert
- **Evaluator**: Privacy-first telemetry (opt-in, anonymous)

### Quick Start
- `use oracle to remember this pattern`
- `use guardian to review this code`
- `use summoner to coordinate [complex task]`
- `use wizard to update documentation`

### Session Handoff (when context degrades)
- `/handoff` - Smooth transition to fresh session with context preserved

### Guardian Auto-Triggers
Guardian automatically activates when:
- >50 lines of code written
- Same error 3+ times
- Same file edited 5+ times in 10 minutes
- Multiple corrections needed

For full documentation: https://github.com/Overlord-Z/ClaudeShack

## Project Knowledge (Oracle)

<!-- ORACLE_CONTEXT_START -->
*Run `python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update` to populate*
<!-- ORACLE_CONTEXT_END -->
"""

    if claude_md.exists():
        with open(claude_md, 'r') as f:
            content = f.read()

        if 'ClaudeShack Skills' in content:
            print("   [OK] claude.md already has ClaudeShack section")
            return True

        with open(claude_md, 'a') as f:
            f.write('\n' + claudeshack_section)
        print(f"   [OK] Updated {claude_md}")
    else:
        with open(claude_md, 'w') as f:
            f.write(f"# {project_path.name} Development Context\n")
            f.write(claudeshack_section)
        print(f"   [OK] Created {claude_md}")

    return True


def update_gitignore(project_path: Path) -> bool:
    """Update .gitignore with ClaudeShack entries."""
    print("\n[6/6] Updating .gitignore...")

    gitignore = project_path / '.gitignore'
    entries = """
# ClaudeShack (project-specific data)
.oracle/
.guardian/
.summoner/mcds/
.evaluator/
"""

    if gitignore.exists():
        with open(gitignore, 'r') as f:
            content = f.read()

        if '.oracle/' in content:
            print("   [OK] .gitignore already has ClaudeShack entries")
            return True

        with open(gitignore, 'a') as f:
            f.write(entries)
        print(f"   [OK] Updated {gitignore}")
    else:
        with open(gitignore, 'w') as f:
            f.write(entries)
        print(f"   [OK] Created {gitignore}")

    return True


def print_hook_instructions():
    """Print instructions for setting up SessionStart hook."""
    settings_path = get_platform_settings_path()

    # Determine the correct path to the hook script
    oracle_hook = SKILLS_DIR / 'oracle' / 'scripts' / 'session_start_hook.py'

    print("\n" + "="*70)
    print("OPTIONAL: SessionStart Hook Setup")
    print("="*70)
    print("""
To auto-load Oracle context at session start, add this to your
Claude Code settings file:
""")
    print(f"Settings location: {settings_path}")
    print("""
Add to the "hooks" section:

{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "python """ + str(oracle_hook) + """"
          }
        ]
      }
    ]
  }
}

For detailed setup: See .claude/skills/oracle/scripts/HOOK_SETUP.md
""")


def main():
    """Main initialization function."""
    import argparse

    parser = argparse.ArgumentParser(description='Initialize ClaudeShack ecosystem')
    parser.add_argument('project_path', nargs='?', default='.',
                        help='Project path (default: current directory)')
    parser.add_argument('--skip-history', action='store_true',
                        help='Skip mining conversation history')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()

    if not project_path.exists():
        print(f"[ERROR] Project path does not exist: {project_path}")
        sys.exit(1)

    print("="*70)
    print("ClaudeShack Ecosystem Initialization")
    print("="*70)
    print(f"\nProject: {project_path}")
    print(f"Skills:  {SKILLS_DIR}")

    # Run initialization steps
    try:
        init_oracle_structure(project_path)
        init_guardian_config(project_path)

        if not args.skip_history:
            mine_conversation_history(project_path, args.verbose)
        else:
            print("\n[3/6] Skipping history mining (--skip-history)")

        generate_context(project_path, args.verbose)
        update_claude_md(project_path)
        update_gitignore(project_path)

        print("\n" + "="*70)
        print("[OK] ClaudeShack ecosystem initialized!")
        print("="*70)

        print("""
Ready to use:
  - skill: "oracle"     - Project memory and learning
  - skill: "guardian"   - Quality gates and code review
  - skill: "summoner"   - Multi-agent orchestration
  - skill: "wizard"     - Documentation maintenance

Oracle learns as you work - correct mistakes and it remembers!
""")

        print_hook_instructions()

    except KeyboardInterrupt:
        print("\n[CANCELLED] Initialization cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error during initialization: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
