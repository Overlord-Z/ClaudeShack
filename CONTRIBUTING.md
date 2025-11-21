# Contributing to ClaudeShack

First off, thanks for taking the time to contribute! 🎉

ClaudeShack is a collection of skills for Claude Code that enhance productivity and code quality. We welcome contributions of all kinds: bug fixes, new skills, improvements to existing skills, documentation, and more.

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Development Setup](#development-setup)
- [Skill Development Guidelines](#skill-development-guidelines)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

## Ways to Contribute

### 1. Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. Use our **bug report template** and include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages or logs (with sensitive info removed)

### 2. Suggesting Features

Feature requests are welcome! Use our **feature request template** and provide:
- Clear description of the problem or use case
- Proposed solution
- Examples of how it would work
- Whether you're willing to contribute

### 3. Contributing Code

- Fix bugs
- Add new features
- Improve documentation
- Add examples and use cases
- Create Guardian templates
- Enhance existing skills

### 4. Sharing Feedback

Use the **skill feedback template** to share your experience:
- What works well
- What could be improved
- How often you use skills
- Your use cases

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of Claude Code and skills

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ClaudeShack.git
cd ClaudeShack

# Create a branch for your work
git checkout -b feature/my-new-feature

# Make your changes and test them

# Test Guardian templates
python skills/guardian/Scripts/template_loader.py --list

# Test event tracking
python skills/evaluator/Scripts/track_event.py --status
```

### Testing Your Changes

Before submitting a PR:
1. Test the skill manually in a real Claude Code session
2. Verify all scripts work with example inputs
3. Check for errors in logs and output
4. Test edge cases and error scenarios

## Skill Development Guidelines

### Skill Structure

All skills should follow this structure:
```
skill-name/
├── SKILL.md              # Skill definition (required)
├── README.md             # Documentation (required)
├── Scripts/              # Automation scripts
├── References/           # Templates and guides
└── Assets/               # Non-contextual files
```

### Skill Definition (SKILL.md)

Required YAML frontmatter:
```yaml
---
name: Skill Name
description: Clear description that helps Claude know when to use this skill
---
```

### Core Principles for New Skills

When creating skills, follow these principles:

1. **Privacy First**: No PII, opt-in telemetry only
2. **Minimal Context**: Don't pass full conversations to subagents
3. **Read-Only Subagents**: Analysis only, no modifications without user approval
4. **User Authority**: User has final say on all actions
5. **Clear Documentation**: Examples and comprehensive usage docs

### Quality Standards

- **DRY**: No duplicated logic
- **CLEAN**: Readable, maintainable code
- **Documented**: Clear documentation and examples
- **Tested**: Scripts should be tested
- **Integrated**: Consider integrations with other skills
- **Privacy-Respecting**: Follow Evaluator patterns if collecting data
- **Memory-Efficient**: Limit data structure growth, check file sizes

### Integration with Other Skills

New skills should consider:
- **Oracle**: Can it record/use knowledge for learning?
- **Guardian**: Can it provide quality checks or validation?
- **Summoner**: Can it be orchestrated with other skills?
- **Evaluator**: Should it track usage metrics (opt-in)?

### Guardian Template Guidelines

When creating Guardian templates:
1. Follow template structure in existing templates
2. Include read-only constraints prominently
3. Specify Oracle integration (categories, tags, limits)
4. Define validation rules appropriate for the review type
5. Test with real code before submitting
6. Document use cases in Templates/README.md

### Privacy and Telemetry

If your skill collects any data:
1. Make it **opt-in** by default
2. Collect **only anonymous data** (no PII)
3. Document **what's collected** clearly
4. Provide **easy opt-out** mechanism
5. Follow **Evaluator patterns** for telemetry

**Never collect**: User identity, code content, file paths, conversation history, project names

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-skill`)
3. Make your changes
4. Update documentation
5. Test your changes
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

### PR Checklist

**For All PRs:**
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Changes tested manually
- [ ] No new warnings or errors

**For New Skills:**
- [ ] Skill follows structure guidelines
- [ ] SKILL.md includes proper frontmatter
- [ ] README.md is comprehensive
- [ ] Scripts are tested and executable
- [ ] Integration points documented
- [ ] Examples provided
- [ ] Privacy principles followed (if collecting data)
- [ ] Updated main README.md

**For Guardian Templates:**
- [ ] Template follows JSON structure
- [ ] Read-only constraints included
- [ ] Oracle integration configured
- [ ] Validation rules defined
- [ ] Tested with real code
- [ ] Usage documented in Templates/README.md

## Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints for function parameters and returns
- Add docstrings for all functions
- Handle errors gracefully (no uncaught exceptions)

### Markdown Documentation

- Use clear headings (H1 for title, H2 for sections)
- Include code examples with syntax highlighting
- Add usage examples
- Keep README files up to date

### Git Commit Messages

```
<type>: <subject>

<body>
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`

**Example**:
```
feat: Add API review template for Guardian

Includes checks for rate limiting, authentication, and input validation.

Closes #42
```

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow best practices
- Welcome newcomers and help them contribute

## Questions?

Open an issue or discussion on GitHub!

---

Thank you for contributing to ClaudeShack! 🏛️
