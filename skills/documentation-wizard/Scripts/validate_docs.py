#!/usr/bin/env python3
"""Documentation validator - checks for stale docs and issues."""
import sys
from pathlib import Path
import re

def validate_docs(project_path):
    """Validate documentation."""
    issues = []

    # Check README exists
    readme = project_path / 'README.md'
    if not readme.exists():
        issues.append("[ERROR] README.md missing")
    else:
        print("[OK] README.md found")

        # Check for broken internal links
        content = readme.read_text()
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, link in links:
            if not link.startswith('http'):
                link_path = project_path / link.lstrip('./')
                if not link_path.exists():
                    issues.append(f"[ERROR] Broken link in README: {link}")

    # Check for CONTRIBUTING.md
    if not (project_path / 'CONTRIBUTING.md').exists():
        issues.append("[WARNING]  CONTRIBUTING.md missing (recommended)")

    return issues

def main():
    project = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    print(f"[SEARCH] Validating documentation for: {project}\n")

    issues = validate_docs(project)

    if issues:
        print("\nIssues found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n[OK] All documentation checks passed!")

if __name__ == '__main__':
    main()
