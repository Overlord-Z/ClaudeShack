#!/usr/bin/env python3
"""
Guardian Template Loader

Loads and applies Guardian review/planning templates for consistent,
structured agent interactions.

Usage:
    # List available templates
    python template_loader.py --list

    # Load a template
    python template_loader.py --template security_review

    # Load template and apply to context
    python template_loader.py --template security_review --file auth.py --output prompt.txt

    # Create custom template
    python template_loader.py --create my_review --based-on security_review
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any


def find_templates_dir() -> Path:
    """Find the Guardian Templates directory."""
    # First try relative to this script
    script_dir = Path(__file__).parent
    templates_dir = script_dir.parent / 'Templates'

    if templates_dir.exists():
        return templates_dir

    # Try from current directory
    templates_dir = Path.cwd() / 'skills' / 'guardian' / 'Templates'
    if templates_dir.exists():
        return templates_dir

    raise FileNotFoundError("Guardian Templates directory not found")


def list_templates() -> List[Dict[str, str]]:
    """List all available Guardian templates.

    Returns:
        List of template metadata dictionaries
    """
    templates_dir = find_templates_dir()
    templates = []

    for template_file in templates_dir.glob('*.json'):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                template = json.load(f)
                templates.append({
                    'name': template.get('name', template_file.stem),
                    'description': template.get('description', 'No description'),
                    'task_type': template.get('task_type', 'unknown'),
                    'file': str(template_file)
                })
        except (json.JSONDecodeError, OSError, IOError):
            continue

    return templates


def load_template(template_name: str) -> Dict[str, Any]:
    """Load a Guardian template by name.

    Args:
        template_name: Name of the template (with or without .json extension)

    Returns:
        Template configuration dictionary
    """
    templates_dir = find_templates_dir()

    # Remove .json extension if provided
    if template_name.endswith('.json'):
        template_name = template_name[:-5]

    template_file = templates_dir / f"{template_name}.json"

    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_name}")

    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid template JSON: {e}")


def apply_template_to_context(
    template: Dict[str, Any],
    context: str
) -> str:
    """Apply a template to extracted context.

    Args:
        template: Template configuration
        context: Extracted minimal context

    Returns:
        Formatted agent prompt
    """
    prompt_template = template.get('agent_prompt_template', '')

    # Replace context placeholder
    prompt = prompt_template.replace('{context}', context)

    return prompt


def get_template_config(template: Dict[str, Any]) -> Dict[str, Any]:
    """Extract configuration parameters from template.

    Args:
        template: Template configuration

    Returns:
        Configuration dictionary for context_filter.py
    """
    return {
        'task_type': template.get('task_type', 'review'),
        'focus': template.get('focus', ''),
        'oracle_categories': template.get('oracle_categories', ['patterns', 'gotchas']),
        'oracle_tags': template.get('oracle_tags_required', []),
        'max_patterns': template.get('max_oracle_patterns', 5),
        'max_gotchas': template.get('max_oracle_gotchas', 5),
        'validation_rules': template.get('validation_rules', {})
    }


def create_custom_template(
    name: str,
    base_template: Optional[str] = None,
    description: str = "",
    task_type: str = "review"
) -> Path:
    """Create a new custom template.

    Args:
        name: Name for the new template
        base_template: Optional template to base this on
        description: Template description
        task_type: Type of task (review, plan, debug)

    Returns:
        Path to the created template file
    """
    templates_dir = find_templates_dir()

    if base_template:
        # Load base template
        base = load_template(base_template)
        new_template = base.copy()
        new_template['name'] = name
        if description:
            new_template['description'] = description
    else:
        # Create minimal template
        new_template = {
            "name": name,
            "description": description or f"Custom {task_type} template",
            "task_type": task_type,
            "focus": "",
            "agent_prompt_template": "You are a READ-ONLY code reviewer for Guardian.\n\nCRITICAL CONSTRAINTS:\n- DO NOT modify any files\n- ONLY read and analyze\n\n{context}\n\nReturn suggestions as JSON array.",
            "oracle_categories": ["patterns", "gotchas"],
            "oracle_tags_required": [],
            "max_oracle_patterns": 5,
            "max_oracle_gotchas": 5,
            "always_include_files": [],
            "validation_rules": {
                "min_confidence": 0.5,
                "block_contradictions": true
            }
        }

    # Save template
    template_file = templates_dir / f"{name}.json"

    with open(template_file, 'w', encoding='utf-8') as f:
        json.dump(new_template, f, indent=2)

    return template_file


def main():
    parser = argparse.ArgumentParser(
        description='Guardian template loader and manager',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available templates'
    )

    parser.add_argument(
        '--template',
        help='Template name to load'
    )

    parser.add_argument(
        '--file',
        help='File to apply template to (used with --output)'
    )

    parser.add_argument(
        '--output',
        help='Output file for generated prompt'
    )

    parser.add_argument(
        '--create',
        help='Create a new custom template with this name'
    )

    parser.add_argument(
        '--based-on',
        help='Base the new template on an existing one'
    )

    parser.add_argument(
        '--description',
        help='Description for new template'
    )

    parser.add_argument(
        '--show-config',
        action='store_true',
        help='Show template configuration (for use with context_filter.py)'
    )

    args = parser.parse_args()

    # List templates
    if args.list:
        templates = list_templates()

        print("Available Guardian Templates:")
        print("=" * 60)

        for template in templates:
            print(f"\nName: {template['name']}")
            print(f"  Type: {template['task_type']}")
            print(f"  Description: {template['description']}")
            print(f"  File: {template['file']}")

        print("\n" + "=" * 60)
        print(f"Total: {len(templates)} templates")
        sys.exit(0)

    # Create template
    if args.create:
        template_file = create_custom_template(
            args.create,
            args.based_on,
            args.description or "",
            "review"
        )

        print(f"Created template: {template_file}")
        print("Edit this file to customize your template")
        sys.exit(0)

    # Load template
    if args.template:
        template = load_template(args.template)

        if args.show_config:
            config = get_template_config(template)
            print(json.dumps(config, indent=2))
            sys.exit(0)

        if args.output and args.file:
            # Apply template to file
            # This would integrate with context_filter.py
            print(f"Applying template '{args.template}' to {args.file}...")
            print(f"Output will be saved to: {args.output}")
            print("\nTo apply this template:")
            print(f"  1. Run context_filter.py with template config")
            print(f"  2. Apply template to extracted context")
            print(f"  3. Save to {args.output}")
        else:
            # Just show template
            print(json.dumps(template, indent=2))

        sys.exit(0)

    parser.print_help()
    sys.exit(1)


if __name__ == '__main__':
    main()
