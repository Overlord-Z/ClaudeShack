#!/usr/bin/env python3
"""
Documentation Wizard - Documentation Audit Tool

Detects outdated, missing, or inconsistent documentation across ClaudeShack.

Usage:
    # Full audit
    python audit_docs.py

    # Audit specific file
    python audit_docs.py --file README.md

    # Check for broken links
    python audit_docs.py --check-links

    # Detect missing documentation
    python audit_docs.py --missing

Environment Variables:
    WIZARD_VERBOSE: Set to '1' for detailed output
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import re


def find_skills() -> List[Path]:
    """Find all skill directories."""
    skills_dir = Path('skills')

    if not skills_dir.exists():
        return []

    return [d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]


def check_skill_documentation(skill_path: Path) -> Dict[str, Any]:
    """Check if a skill has required documentation.

    Args:
        skill_path: Path to skill directory

    Returns:
        Dictionary with audit results
    """
    issues = []
    warnings = []

    # Check for SKILL.md
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        issues.append(f"Missing SKILL.md")
    else:
        # Check frontmatter
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.startswith('---'):
                    issues.append("SKILL.md missing YAML frontmatter")
                elif 'name:' not in content[:500] or 'description:' not in content[:500]:
                    issues.append("SKILL.md frontmatter missing name or description")
        except (OSError, IOError, UnicodeDecodeError):
            issues.append("SKILL.md cannot be read")

    # Check for Scripts directory
    scripts_dir = skill_path / 'Scripts'
    if scripts_dir.exists():
        # Check for Scripts README
        scripts_readme = scripts_dir / 'README.md'
        if not scripts_readme.exists():
            warnings.append("Scripts directory missing README.md")

        # Count Python scripts
        python_scripts = list(scripts_dir.glob('*.py'))
        if len(python_scripts) == 0:
            warnings.append("Scripts directory has no Python files")
    else:
        warnings.append("No Scripts directory (might be documentation-only skill)")

    return {
        'skill': skill_path.name,
        'path': str(skill_path),
        'issues': issues,
        'warnings': warnings,
        'has_skill_md': skill_md.exists(),
        'has_scripts': scripts_dir.exists(),
        'script_count': len(list(scripts_dir.glob('*.py'))) if scripts_dir.exists() else 0
    }


def check_readme_mentions_skills(readme_path: Path, skills: List[Path]) -> List[str]:
    """Check if README mentions all skills.

    Args:
        readme_path: Path to README.md
        skills: List of skill paths

    Returns:
        List of skills not mentioned in README
    """
    if not readme_path.exists():
        return []

    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read().lower()
    except (OSError, IOError, UnicodeDecodeError):
        return []

    missing = []
    for skill in skills:
        skill_name = skill.name
        if skill_name.lower() not in readme_content:
            missing.append(skill_name)

    return missing


def check_broken_links(file_path: Path) -> List[Dict[str, Any]]:
    """Check for broken relative links in markdown file.

    Args:
        file_path: Path to markdown file

    Returns:
        List of broken links with details
    """
    broken = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (OSError, IOError, UnicodeDecodeError):
        return []

    # Find markdown links: [text](path)
    link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    matches = re.finditer(link_pattern, content)

    for match in matches:
        link_text = match.group(1)
        link_path = match.group(2)

        # Skip external links
        if link_path.startswith(('http://', 'https://', 'mailto:', '#')):
            continue

        # Resolve relative path
        resolved = file_path.parent / link_path

        if not resolved.exists():
            broken.append({
                'text': link_text,
                'path': link_path,
                'resolved': str(resolved),
                'line': content[:match.start()].count('\n') + 1
            })

    return broken


def audit_documentation() -> Dict[str, Any]:
    """Perform full documentation audit.

    Returns:
        Audit results dictionary
    """
    results = {
        'skills': [],
        'main_readme': {},
        'contributing': {},
        'broken_links': [],
        'summary': {
            'total_skills': 0,
            'skills_with_issues': 0,
            'total_issues': 0,
            'total_warnings': 0,
            'missing_from_readme': []
        }
    }

    # Audit skills
    skills = find_skills()
    results['summary']['total_skills'] = len(skills)

    for skill in skills:
        audit = check_skill_documentation(skill)
        results['skills'].append(audit)

        if audit['issues']:
            results['summary']['skills_with_issues'] += 1
            results['summary']['total_issues'] += len(audit['issues'])

        results['summary']['total_warnings'] += len(audit['warnings'])

    # Check README
    readme_path = Path('README.md')
    if readme_path.exists():
        missing = check_readme_mentions_skills(readme_path, skills)
        results['summary']['missing_from_readme'] = missing

        # Check for broken links in README
        broken = check_broken_links(readme_path)
        if broken:
            results['broken_links'].append({
                'file': 'README.md',
                'links': broken
            })
    else:
        results['main_readme']['missing'] = True

    # Check CONTRIBUTING.md
    contributing_path = Path('CONTRIBUTING.md')
    if contributing_path.exists():
        broken = check_broken_links(contributing_path)
        if broken:
            results['broken_links'].append({
                'file': 'CONTRIBUTING.md',
                'links': broken
            })
    else:
        results['contributing']['missing'] = True

    return results


def format_audit_report(results: Dict[str, Any]) -> str:
    """Format audit results as readable report.

    Args:
        results: Audit results

    Returns:
        Formatted report string
    """
    lines = []

    lines.append("=" * 70)
    lines.append("DOCUMENTATION WIZARD - AUDIT REPORT")
    lines.append("=" * 70)
    lines.append("")

    # Summary
    summary = results['summary']
    lines.append("SUMMARY")
    lines.append("-" * 70)
    lines.append(f"Total Skills: {summary['total_skills']}")
    lines.append(f"Skills with Issues: {summary['skills_with_issues']}")
    lines.append(f"Total Issues: {summary['total_issues']}")
    lines.append(f"Total Warnings: {summary['total_warnings']}")
    lines.append("")

    # Skills not in README
    if summary['missing_from_readme']:
        lines.append("⚠️  Skills Not Mentioned in README:")
        for skill in summary['missing_from_readme']:
            lines.append(f"   - {skill}")
        lines.append("")

    # Skill-specific issues
    if summary['skills_with_issues'] > 0:
        lines.append("SKILL ISSUES")
        lines.append("-" * 70)

        for skill_audit in results['skills']:
            if skill_audit['issues'] or skill_audit['warnings']:
                lines.append(f"\n{skill_audit['skill']}:")

                for issue in skill_audit['issues']:
                    lines.append(f"   ❌ {issue}")

                for warning in skill_audit['warnings']:
                    lines.append(f"   ⚠️  {warning}")

        lines.append("")

    # Broken links
    if results['broken_links']:
        lines.append("BROKEN LINKS")
        lines.append("-" * 70)

        for file_links in results['broken_links']:
            lines.append(f"\n{file_links['file']}:")
            for link in file_links['links']:
                lines.append(f"   Line {link['line']}: [{link['text']}]({link['path']})")
                lines.append(f"      Resolved to: {link['resolved']} (NOT FOUND)")

        lines.append("")

    # Overall status
    lines.append("=" * 70)
    if summary['total_issues'] == 0 and not results['broken_links']:
        lines.append("✅ DOCUMENTATION AUDIT PASSED - No critical issues found")
    else:
        lines.append(f"❌ DOCUMENTATION AUDIT FAILED - {summary['total_issues']} issues found")

    if summary['total_warnings'] > 0:
        lines.append(f"⚠️  {summary['total_warnings']} warnings (non-critical)")

    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Documentation Wizard - Audit documentation for issues',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--file',
        help='Audit specific file only'
    )

    parser.add_argument(
        '--check-links',
        action='store_true',
        help='Check for broken links only'
    )

    parser.add_argument(
        '--missing',
        action='store_true',
        help='Check for missing documentation only'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()

    # Run audit
    results = audit_documentation()

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        report = format_audit_report(results)
        print(report)

    # Exit code
    if results['summary']['total_issues'] > 0 or results['broken_links']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
