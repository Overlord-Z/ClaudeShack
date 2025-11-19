# Getting Started with ClaudeShack

Welcome to ClaudeShack! This guide will help you get started with your personal Claude Code skill center.

## What is ClaudeShack?

ClaudeShack is a curated collection of Claude Code skills designed to:
- Enhance your productivity with Claude Code
- Ensure code quality through systematic processes
- Enable complex multi-agent workflows
- Prevent common LLM pitfalls (assumptions, context bloat, scope creep)

## Prerequisites

- Claude Code installed and configured
- Basic familiarity with Claude Code skills
- Python 3.7+ (for helper scripts)

## Quick Start

### 1. Clone or Navigate to ClaudeShack

```bash
cd /path/to/ClaudeShack
```

### 2. Verify Skill Installation

Claude Code automatically detects skills in the `.claude/skills/` directory. Your skills are ready to use!

### 3. Use Your First Skill

Try the Summoner skill for a complex task:

```
Use the summoner skill to implement a new feature for user profile management
with avatar uploads, bio editing, and privacy settings.
```

Claude Code will activate the Summoner skill and begin orchestrating the implementation.

## Available Skills

### 🧙 Summoner (Multi-Agent Orchestration)

**Purpose**: Orchestrate complex, multi-component tasks through specialized agents.

**When to Use**:
- Features touching 3+ files/components
- Large refactoring projects
- Migration efforts
- Complex bug fixes
- New system implementations

**Example**:
```
Use the summoner skill to migrate our REST API to GraphQL while maintaining
backwards compatibility.
```

**Learn More**: See `.claude/skills/summoner/README.md`

## Skill Structure

Each skill in ClaudeShack follows this structure:

```
skill-name/
├── SKILL.md              # Skill definition (required)
├── README.md             # Documentation
├── Scripts/              # Executable helpers
├── References/           # Templates and guides
└── Assets/               # Non-contextual files
```

## Using Skills

### Implicit Activation

Skills activate automatically when their trigger contexts are detected:

```
I need to orchestrate a complex refactoring across multiple services
[Summoner skill automatically activates]
```

### Explicit Activation

You can explicitly request a skill:

```
Use the summoner skill to...
```

or

```
Activate the summoner skill
```

## Helper Scripts

### Summoner Skill Scripts

#### Initialize Mission Control Document

```bash
python .claude/skills/summoner/Scripts/init_mission.py "Your Task Name"
```

Creates a new Mission Control Document from the template.

#### Validate Quality Gates

```bash
# Interactive mode
python .claude/skills/summoner/Scripts/validate_quality.py --level task --interactive

# Checklist mode
python .claude/skills/summoner/Scripts/validate_quality.py --level project
```

Validates code against quality standards.

## Best Practices

### 1. Let Skills Guide You

When Claude activates a skill, it's following a specialized workflow. Trust the process.

### 2. Provide Clear Context

Skills work best with clear requirements:

**Good**:
```
Use the summoner skill to add OAuth2 authentication. We need to support
Google and GitHub providers. Users should be able to link multiple accounts.
Security is critical - follow OWASP best practices.
```

**Not as Good**:
```
Add authentication
```

### 3. Use Helper Scripts

The Python scripts aren't just for show - they help maintain quality and organization.

### 4. Review Generated Artifacts

Skills often create planning documents (like Mission Control Documents). Review these to ensure alignment before implementation begins.

### 5. Validate Quality

Use the quality validation scripts regularly, not just at the end:

```bash
# After completing a task
python .claude/skills/summoner/Scripts/validate_quality.py --level task --interactive
```

## Understanding Mission Control Documents

When using the Summoner skill, you'll work with Mission Control Documents (MCDs). These are comprehensive planning documents that:

- Define success criteria
- Preserve context
- Break down tasks
- Track progress
- Ensure quality

### MCD Workflow

1. **Created**: Summoner analyzes your request and creates MCD
2. **Planning**: MCD filled with tasks, phases, dependencies
3. **Execution**: Agents work through tasks systematically
4. **Validation**: Quality gates checked at each phase
5. **Completion**: Final integration and sign-off

## Quality Philosophy

ClaudeShack emphasizes **quality over speed**:

- **DRY**: Don't Repeat Yourself
- **CLEAN**: Clear, Limited, Expressive, Abstracted, Neat
- **SOLID**: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion

### The "Zero Slop" Policy

We prevent:
- Assumptions without validation
- Context bloat
- Scope creep
- Breaking changes without migration paths
- Untested code
- Poor documentation

## Troubleshooting

### Skill Not Activating

**Problem**: Requested a skill but it didn't activate.

**Solutions**:
1. Check skill name is correct
2. Verify `.claude/skills/` structure
3. Be explicit: "Use the [skill-name] skill to..."

### Context Issues

**Problem**: Agent asking for information repeatedly.

**Solutions**:
1. Provide context upfront in your initial request
2. Review the Mission Control Document
3. Make sure context is clearly documented

### Quality Gates Failing

**Problem**: Code doesn't meet quality standards.

**Solutions**:
1. Review which specific gate failed
2. Consult `References/quality-gates.md` for details
3. Fix the issues and revalidate
4. Consider if the standards need adjustment for your use case

## Examples

### Example 1: Simple Feature (No Summoner Needed)

```
Add a "dark mode" toggle to the settings page
```

This is straightforward enough that Claude Code can handle it directly.

### Example 2: Complex Feature (Use Summoner)

```
Use the summoner skill to implement a complete notification system with:
- Real-time WebSocket notifications
- Email fallback for offline users
- Notification preferences per category
- Notification history and read/unread states
- Mobile push notification support
```

This is complex and multi-faceted - perfect for Summoner orchestration.

### Example 3: Refactoring (Use Summoner)

```
Use the summoner skill to refactor our monolithic application into microservices.
Start with extracting the user authentication service while maintaining 100%
backwards compatibility with existing clients.
```

Large refactoring with high risk - Summoner ensures systematic approach.

## Next Steps

### Explore Summoner Skill

Read the comprehensive guide:
```bash
cat .claude/skills/summoner/README.md
```

### Try It Out

Pick a complex task in your project and try the Summoner skill:
```
Use the summoner skill to [your complex task]
```

### Review Templates

Check out the templates to understand how planning works:
```bash
cat .claude/skills/summoner/References/mission-control-template.md
```

### Validate Your Code

Try the quality validator:
```bash
python .claude/skills/summoner/Scripts/validate_quality.py --level task --interactive
```

## Creating Your Own Skills

Want to create a custom skill for ClaudeShack?

1. **Study Existing Skills**: See how Summoner is structured
2. **Read Anthropic's Guide**: Check the official skill creator guide
3. **Use the Template**: Anthropic provides a skill template
4. **Test Thoroughly**: Make sure it works in various scenarios
5. **Document Well**: Clear documentation makes skills more useful

### Skill Creation Resources

- [Anthropic Skill Creator Guide](https://github.com/anthropics/skills/tree/main/skill-creator)
- [Official Claude Code Skills Docs](https://docs.claude.com/en/docs/claude-code/skills)
- [Community Skills](https://github.com/travisvn/awesome-claude-skills)

## Getting Help

### Documentation

- **Summoner Skill**: `.claude/skills/summoner/README.md`
- **Main README**: `README.md`
- **This Guide**: `docs/GETTING_STARTED.md`

### Resources

- [Claude Code Documentation](https://docs.claude.com)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)

### Issues

Found a bug or have a suggestion? Open an issue in the repository!

## Tips for Success

1. **Start with Clear Goals**: Define what success looks like before starting
2. **Break Down Complexity**: Use Summoner for multi-faceted tasks
3. **Validate Often**: Don't wait until the end to check quality
4. **Document Decisions**: Use decision logs in MCDs
5. **Iterate and Improve**: Skills and processes can evolve

## Welcome to ClaudeShack!

You're now ready to leverage the power of structured, quality-focused AI development. The Summoner skill will help you tackle complex projects with confidence, ensuring that every deliverable meets high standards.

**Remember**: Context is precious. Orchestration is power. Quality is non-negotiable.

Happy coding! 🏛️

---

*Last Updated: 2025-11-19*
