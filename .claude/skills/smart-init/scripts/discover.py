#!/usr/bin/env python3
"""
Smart Init Discovery Script

Analyzes a project to gather context for intelligent initialization.
Outputs structured JSON with findings for the Smart Init skill.

Usage:
    python discover.py [project_path]
    python discover.py --json          # Machine-readable output
    python discover.py --verbose       # Detailed human output
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
from typing import Dict, List, Any, Optional


def run_command(cmd: str, cwd: Path = None, timeout: int = 10) -> Optional[str]:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            cwd=str(cwd) if cwd else None, timeout=timeout
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, Exception):
        return None


def detect_languages(project_path: Path) -> Dict[str, int]:
    """Detect programming languages by file extension."""
    extensions = {
        '.ts': 'TypeScript', '.tsx': 'TypeScript',
        '.js': 'JavaScript', '.jsx': 'JavaScript',
        '.py': 'Python',
        '.rs': 'Rust',
        '.go': 'Go',
        '.java': 'Java',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.cs': 'C#',
        '.cpp': 'C++', '.cc': 'C++', '.cxx': 'C++',
        '.c': 'C', '.h': 'C/C++',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.css': 'CSS', '.scss': 'SCSS', '.sass': 'Sass',
        '.html': 'HTML',
        '.vue': 'Vue',
        '.svelte': 'Svelte',
    }

    counts = Counter()

    for root, dirs, files in os.walk(project_path):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if d not in [
            'node_modules', '.git', 'venv', '__pycache__',
            'target', 'dist', 'build', '.next', 'vendor'
        ]]

        for file in files:
            ext = Path(file).suffix.lower()
            if ext in extensions:
                counts[extensions[ext]] += 1

    return dict(counts.most_common(10))


def detect_frameworks(project_path: Path) -> Dict[str, List[str]]:
    """Detect frameworks and tools from config files."""
    frameworks = {
        'frontend': [],
        'backend': [],
        'database': [],
        'testing': [],
        'build': [],
        'ci_cd': [],
        'containerization': []
    }

    # Check package.json
    pkg_json = project_path / 'package.json'
    if pkg_json.exists():
        try:
            with open(pkg_json) as f:
                pkg = json.load(f)
            deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

            # Frontend
            if 'react' in deps:
                frameworks['frontend'].append(f"React {deps.get('react', '')}")
            if 'vue' in deps:
                frameworks['frontend'].append(f"Vue {deps.get('vue', '')}")
            if 'angular' in deps or '@angular/core' in deps:
                frameworks['frontend'].append("Angular")
            if 'svelte' in deps:
                frameworks['frontend'].append("Svelte")
            if 'next' in deps:
                frameworks['frontend'].append(f"Next.js {deps.get('next', '')}")

            # Backend
            if 'express' in deps:
                frameworks['backend'].append("Express.js")
            if 'fastify' in deps:
                frameworks['backend'].append("Fastify")
            if 'koa' in deps:
                frameworks['backend'].append("Koa")
            if 'nestjs' in deps or '@nestjs/core' in deps:
                frameworks['backend'].append("NestJS")

            # Database
            if 'prisma' in deps or '@prisma/client' in deps:
                frameworks['database'].append("Prisma")
            if 'mongoose' in deps:
                frameworks['database'].append("MongoDB (Mongoose)")
            if 'pg' in deps:
                frameworks['database'].append("PostgreSQL")
            if 'mysql2' in deps:
                frameworks['database'].append("MySQL")
            if 'sequelize' in deps:
                frameworks['database'].append("Sequelize ORM")

            # Testing
            if 'jest' in deps:
                frameworks['testing'].append("Jest")
            if 'vitest' in deps:
                frameworks['testing'].append("Vitest")
            if 'mocha' in deps:
                frameworks['testing'].append("Mocha")
            if '@testing-library/react' in deps:
                frameworks['testing'].append("React Testing Library")
            if 'cypress' in deps:
                frameworks['testing'].append("Cypress")
            if 'playwright' in deps:
                frameworks['testing'].append("Playwright")

            # Build tools
            if 'vite' in deps:
                frameworks['build'].append("Vite")
            if 'webpack' in deps:
                frameworks['build'].append("Webpack")
            if 'esbuild' in deps:
                frameworks['build'].append("esbuild")
            if 'turbo' in deps:
                frameworks['build'].append("Turborepo")

        except (json.JSONDecodeError, IOError):
            pass

    # Check Python
    for pyfile in ['pyproject.toml', 'requirements.txt', 'setup.py']:
        pypath = project_path / pyfile
        if pypath.exists():
            try:
                content = pypath.read_text()
                if 'django' in content.lower():
                    frameworks['backend'].append("Django")
                if 'fastapi' in content.lower():
                    frameworks['backend'].append("FastAPI")
                if 'flask' in content.lower():
                    frameworks['backend'].append("Flask")
                if 'pytest' in content.lower():
                    frameworks['testing'].append("pytest")
                if 'sqlalchemy' in content.lower():
                    frameworks['database'].append("SQLAlchemy")
            except IOError:
                pass

    # Check Rust
    cargo = project_path / 'Cargo.toml'
    if cargo.exists():
        try:
            content = cargo.read_text()
            if 'actix' in content:
                frameworks['backend'].append("Actix")
            if 'axum' in content:
                frameworks['backend'].append("Axum")
            if 'tokio' in content:
                frameworks['backend'].append("Tokio (async runtime)")
        except IOError:
            pass

    # Check CI/CD
    if (project_path / '.github' / 'workflows').exists():
        frameworks['ci_cd'].append("GitHub Actions")
    if (project_path / '.gitlab-ci.yml').exists():
        frameworks['ci_cd'].append("GitLab CI")
    if (project_path / 'Jenkinsfile').exists():
        frameworks['ci_cd'].append("Jenkins")

    # Check containerization
    if (project_path / 'Dockerfile').exists():
        frameworks['containerization'].append("Docker")
    if (project_path / 'docker-compose.yml').exists() or (project_path / 'docker-compose.yaml').exists():
        frameworks['containerization'].append("Docker Compose")
    if (project_path / 'kubernetes').exists() or (project_path / 'k8s').exists():
        frameworks['containerization'].append("Kubernetes")

    # Filter empty
    return {k: v for k, v in frameworks.items() if v}


def detect_conventions(project_path: Path) -> Dict[str, Any]:
    """Detect coding conventions and style configs."""
    conventions = {
        'linting': [],
        'formatting': [],
        'git': {},
        'typing': False
    }

    # Linting
    lint_files = ['.eslintrc', '.eslintrc.js', '.eslintrc.json', '.eslintrc.yml',
                  'pylintrc', '.pylintrc', 'ruff.toml', '.flake8']
    for lf in lint_files:
        if (project_path / lf).exists():
            conventions['linting'].append(lf)

    # Formatting
    format_files = ['.prettierrc', '.prettierrc.js', '.prettierrc.json',
                    'rustfmt.toml', '.editorconfig', 'pyproject.toml']
    for ff in format_files:
        if (project_path / ff).exists():
            conventions['formatting'].append(ff)

    # Git conventions (from recent commits)
    git_log = run_command('git log --oneline -50', cwd=project_path)
    if git_log:
        commits = git_log.split('\n')
        # Check for conventional commits
        conventional_pattern = r'^[a-f0-9]+ (feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?:'
        conventional_count = sum(1 for c in commits if re.match(conventional_pattern, c))
        if conventional_count > len(commits) * 0.5:
            conventions['git']['style'] = 'conventional-commits'

        # Check branch pattern
        branch = run_command('git branch --show-current', cwd=project_path)
        if branch:
            conventions['git']['current_branch'] = branch

    # TypeScript/typing
    if (project_path / 'tsconfig.json').exists():
        conventions['typing'] = 'TypeScript'
    elif (project_path / 'py.typed').exists() or (project_path / 'mypy.ini').exists():
        conventions['typing'] = 'Python type hints'

    return conventions


def detect_project_structure(project_path: Path) -> Dict[str, Any]:
    """Detect project structure pattern."""
    structure = {
        'type': 'unknown',
        'key_directories': [],
        'entry_points': []
    }

    # Check for monorepo indicators
    if (project_path / 'packages').exists() or (project_path / 'apps').exists():
        structure['type'] = 'monorepo'
        if (project_path / 'packages').exists():
            structure['key_directories'].append('packages/')
        if (project_path / 'apps').exists():
            structure['key_directories'].append('apps/')

    # Check for standard patterns
    src = project_path / 'src'
    if src.exists():
        structure['key_directories'].append('src/')
        structure['type'] = 'standard'

        # Detect src subdirectories
        for subdir in ['components', 'pages', 'api', 'lib', 'utils',
                       'hooks', 'services', 'models', 'controllers', 'views']:
            if (src / subdir).exists():
                structure['key_directories'].append(f'src/{subdir}/')

    # Entry points
    entry_files = ['index.ts', 'index.js', 'main.ts', 'main.js',
                   'main.py', 'app.py', 'main.rs', 'lib.rs', 'main.go']
    for ef in entry_files:
        for match in project_path.rglob(ef):
            rel_path = str(match.relative_to(project_path))
            if 'node_modules' not in rel_path and 'target' not in rel_path:
                structure['entry_points'].append(rel_path)
                break

    return structure


def detect_documentation(project_path: Path) -> Dict[str, Any]:
    """Detect existing documentation."""
    docs = {
        'readme': None,
        'contributing': None,
        'docs_directory': False,
        'api_docs': False,
        'claude_md': None
    }

    # README
    for readme in ['README.md', 'README.rst', 'README.txt', 'readme.md']:
        readme_path = project_path / readme
        if readme_path.exists():
            docs['readme'] = readme
            # Check quality (rough estimate by size)
            size = readme_path.stat().st_size
            if size > 5000:
                docs['readme_quality'] = 'detailed'
            elif size > 1000:
                docs['readme_quality'] = 'basic'
            else:
                docs['readme_quality'] = 'minimal'
            break

    # Contributing
    for contrib in ['CONTRIBUTING.md', 'contributing.md', 'CONTRIBUTE.md']:
        if (project_path / contrib).exists():
            docs['contributing'] = contrib
            break

    # Docs directory
    docs['docs_directory'] = (project_path / 'docs').exists()

    # API docs
    docs['api_docs'] = any([
        (project_path / 'docs' / 'api').exists(),
        (project_path / 'api-docs').exists(),
        (project_path / 'openapi.yaml').exists(),
        (project_path / 'openapi.json').exists(),
        (project_path / 'swagger.yaml').exists(),
    ])

    # claude.md
    claude_md = project_path / 'claude.md'
    if claude_md.exists():
        docs['claude_md'] = 'exists'
        content = claude_md.read_text()
        if 'ClaudeShack' in content:
            docs['claude_md'] = 'has-claudeshack'

    return docs


def mine_history(project_path: Path) -> Dict[str, Any]:
    """Mine Claude Code conversation history for patterns."""
    history = {
        'found': False,
        'patterns': [],
        'corrections': [],
        'gotchas': [],
        'preferences': []
    }

    # Determine Claude projects directory
    if sys.platform == 'darwin':
        projects_dir = Path.home() / 'Library' / 'Application Support' / 'Claude' / 'projects'
    elif sys.platform == 'win32':
        projects_dir = Path(os.environ.get('APPDATA', '')) / 'Claude' / 'projects'
    else:
        projects_dir = Path.home() / '.claude' / 'projects'

    if not projects_dir.exists():
        return history

    # Try to find project hash
    project_name = project_path.name.lower()

    for project_hash_dir in projects_dir.iterdir():
        if not project_hash_dir.is_dir():
            continue

        # Look for JSONL files
        for jsonl_file in project_hash_dir.glob('*.jsonl'):
            try:
                with open(jsonl_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Simple pattern matching
                if project_name in content.lower() or str(project_path) in content:
                    history['found'] = True

                    # Look for corrections (simple heuristic)
                    correction_patterns = [
                        r"no,?\s+(use|prefer|don't|never|always)",
                        r"actually,?\s+(it's|that's|we)",
                        r"that's\s+(wrong|incorrect|not right)",
                    ]

                    for pattern in correction_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            history['corrections'].append(f"Found {len(matches)} potential corrections")
                            break

                    # Don't process too much
                    break

            except (IOError, UnicodeDecodeError):
                continue

    return history


def get_project_name(project_path: Path) -> str:
    """Get project name from config files or directory."""
    # Try package.json
    pkg_json = project_path / 'package.json'
    if pkg_json.exists():
        try:
            with open(pkg_json) as f:
                return json.load(f).get('name', project_path.name)
        except:
            pass

    # Try Cargo.toml
    cargo = project_path / 'Cargo.toml'
    if cargo.exists():
        try:
            content = cargo.read_text()
            match = re.search(r'name\s*=\s*"([^"]+)"', content)
            if match:
                return match.group(1)
        except:
            pass

    # Try pyproject.toml
    pyproject = project_path / 'pyproject.toml'
    if pyproject.exists():
        try:
            content = pyproject.read_text()
            match = re.search(r'name\s*=\s*"([^"]+)"', content)
            if match:
                return match.group(1)
        except:
            pass

    return project_path.name


def discover(project_path: Path) -> Dict[str, Any]:
    """Run full discovery on a project."""
    return {
        'project_name': get_project_name(project_path),
        'project_path': str(project_path),
        'discovered_at': datetime.now().isoformat(),
        'languages': detect_languages(project_path),
        'frameworks': detect_frameworks(project_path),
        'conventions': detect_conventions(project_path),
        'structure': detect_project_structure(project_path),
        'documentation': detect_documentation(project_path),
        'history': mine_history(project_path)
    }


def format_human_readable(discovery: Dict[str, Any]) -> str:
    """Format discovery results for human reading."""
    output = []
    output.append("=" * 60)
    output.append(f"Project Discovery: {discovery['project_name']}")
    output.append("=" * 60)

    # Languages
    if discovery['languages']:
        output.append("\n## Languages")
        total = sum(discovery['languages'].values())
        for lang, count in discovery['languages'].items():
            pct = (count / total) * 100
            output.append(f"  - {lang}: {count} files ({pct:.0f}%)")

    # Frameworks
    if discovery['frameworks']:
        output.append("\n## Tech Stack")
        for category, items in discovery['frameworks'].items():
            if items:
                output.append(f"  **{category.replace('_', ' ').title()}**: {', '.join(items)}")

    # Conventions
    conv = discovery['conventions']
    if conv['linting'] or conv['formatting']:
        output.append("\n## Conventions")
        if conv['linting']:
            output.append(f"  - Linting: {', '.join(conv['linting'])}")
        if conv['formatting']:
            output.append(f"  - Formatting: {', '.join(conv['formatting'])}")
        if conv.get('typing'):
            output.append(f"  - Typing: {conv['typing']}")
        if conv.get('git', {}).get('style'):
            output.append(f"  - Git: {conv['git']['style']}")

    # Structure
    struct = discovery['structure']
    output.append(f"\n## Structure: {struct['type']}")
    if struct['key_directories']:
        output.append(f"  Key dirs: {', '.join(struct['key_directories'][:5])}")

    # Documentation
    docs = discovery['documentation']
    output.append("\n## Documentation")
    if docs['readme']:
        output.append(f"  - README: {docs['readme']} ({docs.get('readme_quality', 'unknown')})")
    if docs['docs_directory']:
        output.append("  - docs/ directory: Yes")
    if docs['claude_md']:
        output.append(f"  - claude.md: {docs['claude_md']}")

    # History
    hist = discovery['history']
    if hist['found']:
        output.append("\n## Conversation History")
        output.append("  Found existing Claude conversations for this project")
        if hist['corrections']:
            output.append(f"  - {hist['corrections'][0]}")

    output.append("\n" + "=" * 60)
    return "\n".join(output)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Discover project context')
    parser.add_argument('project_path', nargs='?', default='.',
                        help='Project path (default: current directory)')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()
    project_path = Path(args.project_path).resolve()

    if not project_path.exists():
        print(f"Error: Path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    discovery = discover(project_path)

    if args.json:
        print(json.dumps(discovery, indent=2))
    else:
        print(format_human_readable(discovery))


if __name__ == '__main__':
    main()
