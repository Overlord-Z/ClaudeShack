# Style Master Skill

**Expert CSS & Frontend Styling Specialist**

Style Master is your go-to expert for all things CSS, design systems, and frontend styling. It analyzes codebases, maintains style guides, suggests improvements, and ensures beautiful, consistent, accessible UIs.

## What It Does

### 🔍 **Codebase Analysis**
- Detects styling approach (Tailwind, CSS-in-JS, Sass, etc.)
- Extracts design tokens (colors, spacing, typography)
- Identifies patterns and inconsistencies
- Assesses accessibility and performance

### 📚 **Style Guide Maintenance**
- Generates living style guides from your code
- Documents design tokens and component patterns
- Keeps guidelines up-to-date
- Integrates with Oracle to remember preferences

### 💡 **Suggestions & Improvements**
- Modernization opportunities (Grid, custom properties, etc.)
- Performance optimizations
- Accessibility enhancements
- Consistency improvements

### 🎨 **Expert Styling**
- Modern CSS techniques (Container queries, Grid, Flexbox)
- Framework expertise (Tailwind, styled-components, etc.)
- Design system development
- Dark mode and theming support

## Quick Start

### Analyze Your Codebase

```bash
python .claude/skills/style-master/scripts/analyze_styles.py --detailed
```

### Generate Style Guide

```bash
python .claude/skills/style-master/scripts/generate_styleguide.py --output docs/STYLEGUIDE.md
```

### Validate Consistency

```bash
python .claude/skills/style-master/scripts/validate_consistency.py
```

### Get Suggestions

```bash
python .claude/skills/style-master/scripts/suggest_improvements.py
```

## Use Cases

### 1. Start a New Project
```
Use the style master skill to set up a design system for our new React app.

[Proposes modern approach with Tailwind + CSS custom properties]
[Generates initial style guide]
[Sets up design tokens]
```

### 2. Maintain Consistency
```
Analyze our styles and ensure everything follows our design system.

[Scans codebase]
[Finds 5 colors not in design tokens]
[Suggests consolidation]
```

### 3. Modernize Legacy Styles
```
Help modernize our CSS from floats to modern layouts.

[Analyzes current CSS]
[Proposes Grid/Flexbox migration]
[Works with Summoner for large refactor]
```

### 4. Create Components
```
Style a card component with our design system.

[Loads style guide]
[Uses design tokens]
[Creates responsive, accessible card]
[Documents in style guide]
```

## Integration with Other Skills

### With Oracle 🧠
- Remembers your style preferences
- Records component patterns
- Tracks design decisions
- Avoids repeated style mistakes

### With Summoner 🧙
- Coordinates large styling refactors
- Multi-phase design system rollouts
- Complex component library updates

### With Documentation Wizard 📝
- Syncs style guide with documentation
- Auto-updates component docs
- Keeps examples current

## Modern Techniques

### Container Queries
```css
.card {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card { display: grid; }
}
```

### CSS Custom Properties
```css
:root {
  --color-primary: #007bff;
}

[data-theme="dark"] {
  --color-primary: #0d6efd;
}
```

### Modern Layouts
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}
```

## Accessibility First

Style Master ensures:
- ✅ WCAG AA/AAA color contrast
- ✅ Visible focus indicators
- ✅ Keyboard navigation support
- ✅ Screen reader compatibility
- ✅ `prefers-reduced-motion` respect

## Framework Support

- **Tailwind CSS**: Theme config, plugins, optimization
- **CSS-in-JS**: styled-components, Emotion
- **Sass/SCSS**: Modern patterns, organization
- **CSS Modules**: Component-scoped styles
- **UI Libraries**: Material UI, Chakra UI, shadcn/ui

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `analyze_styles.py` | Analyze codebase styling approach and patterns |
| `generate_styleguide.py` | Create living style guide from code |
| `validate_consistency.py` | Check adherence to design tokens |
| `suggest_improvements.py` | Suggest modernization and optimizations |

## Example Workflow

```bash
# 1. Analyze current state
python .claude/skills/style-master/scripts/analyze_styles.py --detailed

# 2. Generate style guide
python .claude/skills/style-master/scripts/generate_styleguide.py

# 3. Review and customize STYLEGUIDE.md

# 4. Validate consistency
python .claude/skills/style-master/scripts/validate_consistency.py

# 5. Get improvement suggestions
python .claude/skills/style-master/scripts/suggest_improvements.py

# 6. Use Style Master skill in Claude Code
# "Use the style master skill to implement the new design system"
```

## Philosophy

**"Form follows function, but both deserve excellence."**

- Consistency is king
- Maintainability matters
- Performance counts
- Accessibility first
- Modern but pragmatic

## Success Indicators

✅ **Style Master is working when:**
- Visual consistency across app
- Up-to-date style guide
- No duplicate styles
- WCAG compliance
- Optimized performance
- Design tokens used consistently

---

**Style Master v1.0** - Beautiful, consistent, accessible interfaces
