# ClaudeShack 🏛️

**Your Personal Marketplace and Skill Center for Claude Code**

ClaudeShack is a curated collection of powerful Claude Code skills designed to enhance productivity, ensure code quality, and enable complex multi-agent workflows.

## 🎯 Mission

To provide production-ready, high-quality skills that:
- Minimize context bloat and LLM assumptions
- Enforce DRY, CLEAN, SOLID principles
- Break down complex tasks into manageable, well-defined units
- Provide quality control and validation at every step

## 📦 Available Skills

### 🧙 Summoner (Multi-Agent Orchestration)

The **Summoner** is a meta-skill for orchestrating complex, multi-agent tasks. It excels at:

- **Task Decomposition**: Breaking down complex requirements into highly specific, atomic tasks
- **Context Preservation**: Creating detailed task indexes that preserve all necessary context and details
- **Agent Orchestration**: Summoning specialized agents with clear responsibilities and boundaries
- **Quality Control**: Ensuring all deliverables follow best practices (DRY, CLEAN, SOLID)
- **Zero Slop Policy**: Preventing assumptions, scope creep, and breaking changes

**Use When:**
- Tasks require coordination across multiple domains or components
- Context preservation is critical to success
- You need to ensure consistency and quality across a large implementation
- Multiple specialized agents would be more effective than a single generalist

**Location:** `skills/summoner/`

---

### 🧠 Oracle (Project Memory & Learning)

The **Oracle** is a sophisticated memory and learning system that maintains institutional knowledge across sessions. It excels at:

- **Session Recording**: Track interactions, decisions, corrections, and learnings
- **Learning from Mistakes**: Remember corrections and avoid repeating errors
- **Smart Context Injection**: Load only relevant knowledge when needed
- **Pattern Detection**: Identify automation opportunities from repeated tasks
- **Knowledge Compounding**: Build and maintain project knowledge over time
- **Token Efficiency**: KISS approach with strategic, minimal context loading

**Use When:**
- Need to remember project-specific patterns and preferences across sessions
- Avoid repeating the same mistakes or corrections
- Track what works and what doesn't in your project
- Want to automate repeated patterns and save tokens
- Building long-term institutional knowledge
- Onboarding new team members or returning to a project after time away

**Location:** `skills/oracle/`

---

### 🎨 Style Master (CSS & Frontend Styling)

The **Style Master** is an expert in CSS, design systems, and frontend styling. It excels at:

- **Codebase Analysis**: Detect styling approaches, extract design tokens, identify patterns
- **Style Guide Maintenance**: Generate and maintain living style guides automatically
- **Expert Suggestions**: Modernization, performance, accessibility improvements
- **Design System Development**: Create cohesive, scalable design systems
- **Framework Expertise**: Tailwind, CSS-in-JS, Sass, and modern CSS techniques
- **Accessibility First**: Ensure WCAG compliance and inclusive design

**Use When:**
- Setting up or maintaining a design system
- Ensuring visual consistency across your application
- Need expert CSS/styling guidance
- Modernizing legacy styles
- Creating accessible, performant UIs
- Integrating with Oracle to remember style preferences

**Location:** `skills/style-master/`

---

### 📚 Documentation Wizard (Living Documentation)

The **Documentation Wizard** keeps documentation perfectly synchronized with code and knowledge. It excels at:

- **Auto-Generation**: Create README, API docs, ADRs, changelogs from code and knowledge
- **Continuous Sync**: Keep docs current with Oracle learnings, Summoner decisions, Style Master guides
- **Validation**: Detect stale docs, broken links, invalid examples
- **Integration Powerhouse**: Leverages Oracle, Summoner, and Style Master for comprehensive documentation
- **Living Documentation**: Docs that evolve with your project

**Use When:**
- Setting up project documentation
- Keeping docs synchronized with code changes
- Generating Architecture Decision Records (ADRs)
- Creating onboarding materials from Oracle sessions
- Automating changelog generation
- Ensuring documentation quality

**Location:** `skills/documentation-wizard/`

## 🚀 Getting Started

### Plugin Installation

Install ClaudeShack as a plugin in Claude Code:

```bash
# Install the ClaudeShack plugin (includes all 4 skills)
/plugin add Overlord-Z/ClaudeShack
```

This installs all four skills:
- **summoner** - Multi-agent orchestration
- **oracle** - Project memory and learning
- **style-master** - CSS and frontend styling
- **documentation-wizard** - Living documentation

### Manual Installation

Clone this repository to use skills locally:

```bash
git clone https://github.com/Overlord-Z/ClaudeShack.git
cd ClaudeShack
```

Skills are automatically available when Claude Code runs in this directory.

### Using Skills

Skills activate automatically based on context, or you can explicitly request them:

```
Use the summoner skill to implement [complex task description]
Use the oracle skill to remember this pattern
Use the style master skill to analyze our CSS
Use the documentation wizard to generate API docs
```

See [MARKETPLACE.md](./MARKETPLACE.md) for detailed installation and usage instructions.

### ClaudeShack CLI

Manage skills with the marketplace CLI:

```bash
# Set up CLI
export CLAUDESHACK_HOME="/path/to/ClaudeShack"
export PATH="$PATH:$CLAUDESHACK_HOME/marketplace/scripts"

# List all skills
claudeshack list

# Get skill info
claudeshack info oracle

# Verify installation
claudeshack verify

# Show version
claudeshack version
```

See [marketplace/INSTALL.md](./marketplace/INSTALL.md) for complete installation guide.

## 📁 Repository Structure

```
ClaudeShack/
├── .claude-plugin/
│   └── plugin.json                  # Plugin manifest
├── skills/                          # All Claude Code skills
│   ├── summoner/                    # Multi-agent orchestration (10 files)
│   ├── oracle/                      # Project memory & learning (15 files)
│   ├── style-master/                # CSS & frontend styling (9 files)
│   ├── documentation-wizard/        # Living documentation (9 files)
│   └── ...                          # Future skills
├── marketplace/                     # Repository management tools
│   ├── scripts/
│   │   └── claudeshack              # CLI management tool
│   ├── registry/
│   │   └── skills.json              # Complete skill catalog
│   ├── INSTALL.md                   # Installation guide
│   └── README.md                    # Marketplace docs
├── README.md                        # This file
├── MARKETPLACE.md                   # User-facing marketplace guide
├── CONTRIBUTING.md                  # Contribution guidelines
└── docs/                            # Additional documentation
```

## 🛠️ Skill Development

Want to create your own skill? Check out:
- [Anthropic's Skill Creator Guide](https://github.com/anthropics/skills/tree/main/skill-creator)
- [Official Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)

## 🔗 Skill Integrations

Skills work powerfully together:

- **Summoner** ← Oracle (context) + Style Master (styling) + Doc Wizard (documentation)
- **Oracle** → All skills (provides memory and learning)
- **Style Master** ← Oracle (preferences) → Doc Wizard (style guide docs)
- **Documentation Wizard** ← Oracle + Summoner + Style Master (comprehensive docs)

**Example**: Summoner orchestrates a refactor, Oracle provides patterns, Style Master handles styling, Documentation Wizard auto-generates the updated docs.

## 📚 Resources

- **Marketplace**: [MARKETPLACE.md](./MARKETPLACE.md) - Full installation and usage guide
- **Official Skills Repository**: [anthropics/skills](https://github.com/anthropics/skills)
- **Claude Code Documentation**: [docs.claude.com](https://docs.claude.com)
- **Community Skills**: [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)

## 🤝 Contributing

This is a personal skill center, but ideas and suggestions are welcome! Feel free to:
- Open issues for skill ideas
- Suggest improvements to existing skills
- Share your own skill implementations

## 📄 License

This repository contains custom skills. See individual skill directories for specific licensing.

---

**Built with ❤️ for the Claude Code community**
