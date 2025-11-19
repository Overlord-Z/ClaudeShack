#!/usr/bin/env python3
"""
Quality Gates Validator

This script helps validate code against quality gates defined in the
quality-gates.md reference document.

Usage:
    python validate_quality.py [--level task|phase|project] [--interactive]

Example:
    python validate_quality.py --level task --interactive
    python validate_quality.py --level project
"""

import sys
import argparse
from enum import Enum


class Level(Enum):
    TASK = 'task'
    PHASE = 'phase'
    PROJECT = 'project'


class Severity(Enum):
    CRITICAL = '🔴'
    WARNING = '🟡'
    INFO = '🟢'


# Quality Gate Definitions
TASK_GATES = {
    'Functional Requirements': [
        'All specified outputs delivered',
        'Functionality works as described',
        'Edge cases handled',
        'Error cases handled gracefully',
        'No regression in existing functionality'
    ],
    'Code Quality': [
        'Code is readable and self-documenting',
        'Variable/function names are meaningful',
        'No magic numbers or strings',
        'No commented-out code',
        'Consistent code style with project'
    ],
    'DRY': [
        'No duplicated logic',
        'Shared functionality extracted to utilities',
        'Constants defined once',
        'No copy-paste code blocks'
    ],
    'Testing': [
        'Unit tests written for new code',
        'Tests cover happy path',
        'Tests cover edge cases',
        'Tests cover error conditions',
        'All tests pass'
    ],
    'Documentation': [
        'Complex logic has explanatory comments',
        'Public APIs documented',
        'README updated if needed',
        'Breaking changes documented'
    ]
}

PHASE_GATES = {
    'Integration': [
        'All components integrate correctly',
        'Data flows between components as expected',
        'No integration bugs',
        'APIs between components are clean',
        'Interfaces are well-defined'
    ],
    'CLEAN Principles': [
        'Clear: Code is easy to understand',
        'Limited: Functions have single responsibility',
        'Expressive: Naming reveals intent',
        'Abstracted: Proper level of abstraction',
        'Neat: Organized, well-structured code'
    ],
    'Performance': [
        'No obvious performance issues',
        'Efficient algorithms used',
        'No unnecessary computations',
        'Resources properly managed',
        'Meets stated performance requirements'
    ],
    'Security': [
        'No injection vulnerabilities',
        'Input validation in place',
        'Output encoding where needed',
        'Authentication/authorization checked',
        'Sensitive data not logged or exposed',
        'Dependencies have no known vulnerabilities'
    ]
}

PROJECT_GATES = {
    'SOLID - Single Responsibility': [
        'Each class/module has one reason to change',
        'Each function does one thing well',
        'No god objects or god functions',
        'Responsibilities clearly separated'
    ],
    'SOLID - Open/Closed': [
        'Open for extension (can add new behavior)',
        'Closed for modification',
        'Use abstractions for extension points',
        'Configuration over hardcoding'
    ],
    'SOLID - Liskov Substitution': [
        'Subtypes can replace base types without breaking',
        'Derived classes don\'t weaken preconditions',
        'Inheritance is "is-a" relationship'
    ],
    'SOLID - Interface Segregation': [
        'Interfaces are focused and cohesive',
        'No client forced to depend on unused methods',
        'Many small interfaces over one large interface'
    ],
    'SOLID - Dependency Inversion': [
        'High-level modules don\'t depend on low-level modules',
        'Both depend on abstractions',
        'Dependencies injected, not hardcoded'
    ],
    'Testing Coverage': [
        'Unit test coverage meets threshold',
        'Integration tests for key workflows',
        'E2E tests for critical user paths',
        'All tests passing consistently',
        'No flaky tests'
    ],
    'Documentation Completeness': [
        'README is current and accurate',
        'API documentation complete',
        'Architecture documented',
        'Setup instructions clear',
        'Troubleshooting guide available'
    ],
    'Production Readiness': [
        'No breaking changes or migration guide provided',
        'Error handling comprehensive',
        'Logging appropriate',
        'Configuration externalized',
        'Secrets properly managed'
    ]
}


def get_gates_for_level(level):
    """Get quality gates for specified level."""
    if level == Level.TASK:
        return TASK_GATES
    elif level == Level.PHASE:
        return {**TASK_GATES, **PHASE_GATES}
    elif level == Level.PROJECT:
        return {**TASK_GATES, **PHASE_GATES, **PROJECT_GATES}


def interactive_validation(gates):
    """Run interactive validation."""
    results = {}
    total_checks = sum(len(checks) for checks in gates.values())
    current = 0

    print("\n" + "="*70)
    print("🔍 Quality Gates Validation")
    print("="*70)
    print(f"\nTotal checks: {total_checks}")
    print("\nFor each check, respond: y (yes/pass), n (no/fail), s (skip)\n")

    for category, checks in gates.items():
        print(f"\n{'─'*70}")
        print(f"📋 {category}")
        print(f"{'─'*70}")

        category_results = []

        for check in checks:
            current += 1
            while True:
                response = input(f"  [{current}/{total_checks}] {check}? [y/n/s]: ").lower().strip()

                if response in ['y', 'yes']:
                    print(f"    ✅ Pass")
                    category_results.append(('pass', check))
                    break
                elif response in ['n', 'no']:
                    print(f"    ❌ Fail")
                    category_results.append(('fail', check))
                    break
                elif response in ['s', 'skip']:
                    print(f"    ⏭️  Skip")
                    category_results.append(('skip', check))
                    break
                else:
                    print("    Invalid input. Use y/n/s")

        results[category] = category_results

    return results


def print_summary(results, level):
    """Print validation summary."""
    total_pass = sum(1 for cat in results.values() for status, _ in cat if status == 'pass')
    total_fail = sum(1 for cat in results.values() for status, _ in cat if status == 'fail')
    total_skip = sum(1 for cat in results.values() for status, _ in cat if status == 'skip')
    total_checks = total_pass + total_fail + total_skip

    print("\n" + "="*70)
    print("📊 VALIDATION SUMMARY")
    print("="*70)

    print(f"\nLevel: {level.value.upper()}")
    print(f"\nResults:")
    print(f"  ✅ Passed: {total_pass}/{total_checks}")
    print(f"  ❌ Failed: {total_fail}/{total_checks}")
    print(f"  ⏭️  Skipped: {total_skip}/{total_checks}")

    if total_fail > 0:
        print(f"\n🔴 FAILED CHECKS:")
        for category, checks in results.items():
            failed = [(status, check) for status, check in checks if status == 'fail']
            if failed:
                print(f"\n  {category}:")
                for _, check in failed:
                    print(f"    ❌ {check}")

    print("\n" + "="*70)

    if total_fail == 0 and total_skip == 0:
        print("🎉 ALL QUALITY GATES PASSED!")
        print("="*70)
        return True
    elif total_fail == 0:
        print(f"⚠️  All checked gates passed, but {total_skip} checks were skipped.")
        print("="*70)
        return True
    else:
        print(f"❌ {total_fail} QUALITY GATES FAILED")
        print("🔧 Please address failed checks before proceeding.")
        print("="*70)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Validate code against quality gates',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_quality.py --level task --interactive
  python validate_quality.py --level project
  python validate_quality.py --level phase --interactive
        """
    )

    parser.add_argument(
        '--level',
        type=str,
        choices=['task', 'phase', 'project'],
        default='task',
        help='Validation level (default: task)'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run interactive validation'
    )

    args = parser.parse_args()

    level = Level(args.level)
    gates = get_gates_for_level(level)

    if args.interactive:
        results = interactive_validation(gates)
        success = print_summary(results, level)
        sys.exit(0 if success else 1)
    else:
        # Non-interactive mode - just print checklist
        print(f"\n{'='*70}")
        print(f"Quality Gates Checklist - {level.value.upper()} Level")
        print(f"{'='*70}\n")

        for category, checks in gates.items():
            print(f"\n{category}:")
            for check in checks:
                print(f"  [ ] {check}")

        print(f"\n{'='*70}")
        print("Run with --interactive flag for guided validation")
        print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
