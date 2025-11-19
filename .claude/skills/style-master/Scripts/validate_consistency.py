#!/usr/bin/env python3
"""Style consistency validator - checks for design token adherence."""
import sys
from pathlib import Path
import re
from collections import Counter

def validate_colors(root_path):
    """Check for color consistency."""
    colors = []
    for css_file in root_path.rglob('*.css'):
        if 'node_modules' not in str(css_file):
            try:
                content = css_file.read_text()
                colors.extend(re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b', content))
            except: pass

    counts = Counter(colors)
    print(f"🎨 Colors: {len(counts)} unique colors found")
    if len(counts) > 20:
        print(f"  ⚠️  Consider consolidating to a color system")
    return counts

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    print("🔍 Validating style consistency...\n")
    validate_colors(root)
    print("\n✅ Validation complete")

if __name__ == '__main__':
    main()
