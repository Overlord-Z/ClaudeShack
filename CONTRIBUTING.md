# Contributing to ClaudeShack

Thank you for your interest in contributing to ClaudeShack! This document provides guidelines for contributing to the project.

## Ways to Contribute

### 1. Suggest New Skills

Have an idea for a skill? Open an issue with:
- Skill name and purpose
- Key features and use cases
- How it would integrate with existing skills

### 2. Improve Existing Skills

- Fix bugs
- Add new features
- Improve documentation
- Add examples and use cases

### 3. Report Issues

Found a bug or issue? Please include:
- Skill name and version
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior

### 4. Share Workflows

Document how you use skills together:
- Real-world use cases
- Integration patterns
- Best practices

## Development Guidelines

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

### Quality Standards

- **DRY**: No duplicated logic
- **CLEAN**: Readable, maintainable code
- **Documented**: Clear documentation and examples
- **Tested**: Scripts should be tested
- **Integrated**: Consider integrations with other skills

### Integration with Other Skills

New skills should consider:
- **Oracle**: Can it record/use knowledge?
- **Summoner**: Can it be orchestrated?
- **Style Master**: (if frontend-related)
- **Documentation Wizard**: Can it generate/sync docs?

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

- [ ] Skill follows structure guidelines
- [ ] SKILL.md includes proper frontmatter
- [ ] README.md is comprehensive
- [ ] Scripts are tested and executable
- [ ] Integration points documented
- [ ] Examples provided
- [ ] Updated MARKETPLACE.md (if new skill)
- [ ] Updated main README.md (if new skill)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow best practices

## Questions?

Open an issue or discussion on GitHub!

---

Thank you for contributing to ClaudeShack! 🏛️
