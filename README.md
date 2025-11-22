# ClaudeShack 🏛️

**Production-Ready Skills for Claude Code**

[![Status](https://img.shields.io/badge/status-beta-blue)]()
[![Version](https://img.shields.io/badge/version-v0.1--beta-orange)]()
[![License](https://img.shields.io/github/license/Overlord-Z/ClaudeShack)](LICENSE)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](CODE_OF_CONDUCT.md)

ClaudeShack is a curated collection of powerful Claude Code skills designed to enhance productivity, ensure code quality, and enable intelligent multi-agent workflows - all while maintaining privacy, minimizing context bloat, and preventing hallucinations.

## 🎯 Core Principles

- **Privacy First**: No PII collection, opt-in telemetry, transparent data handling
- **Minimal Context**: Focused context passing to subagents, no full conversation dumps
- **Facts Over Fiction**: Documentation verified against code, no hallucinations
- **Read-Only Subagents**: Analysis and suggestions only, modifications require user approval
- **Community Driven**: GitHub-native feedback, telemetry-informed improvements

## 📦 Available Skills

### 🧠 Oracle (Project Memory & Learning)

Project memory system that tracks interactions, learns from corrections, and maintains knowledge across sessions.

**Core Features:**
- Session recording and timeline tracking
- Learn from mistakes and corrections
- Strategic context injection (KISS - load only what's needed)
- Pattern detection for automation opportunities
- Token-efficient knowledge storage

**Use When:** Remembering project patterns, avoiding repeated mistakes, maintaining institutional knowledge

**Location:** `skills/oracle/`

**Integrates With:** All skills (provides memory and learning foundation)

---

### 🛡️ Guardian (Quality Gates & Session Health)

Automatic quality monitoring that spawns focused Haiku agents for code review when degradation detected.

**Core Features:**
- Triggers on code volume (>50 lines), repeated errors (3+), file churn (5+ edits)
- Read-only subagents (analysis only, no modifications)
- Oracle validation (cross-checks suggestions against known patterns)
- Learning from feedback (adjusts sensitivity based on acceptance rates)
- Session health tracking

**Use When:** Automatic code review, detecting session degradation, task planning for complex work

**Location:** `skills/guardian/`

**Integrates With:** Oracle (+31% suggestion acceptance when active)

---

### 🧙 Summoner (Multi-Agent Orchestration)

Coordinates multiple specialized agents for complex, multi-component tasks.

**Core Features:**
- Task decomposition into atomic subtasks
- Mission Control Documents (MCD) as single source of truth
- Parallel agent execution where dependencies allow
- Quality gates (DRY, CLEAN, SOLID enforcement)
- Minimal context passing to each agent

**Use When:** Tasks with 3+ distinct components, multi-phase execution, complex research coordination

**Location:** `skills/summoner/`

**Integrates With:** Oracle (loads patterns), Guardian (validates quality), Wizard (coordinates research)

---

### 📝 Wizard (Documentation Maintenance)

Intelligent documentation that stays accurate through research, fact-checking, and validation.

**Core Features:**
- Research-first approach (Oracle + code + conversation history)
- No-hallucination policy (facts only with references)
- Spawns read-only research agents via Summoner
- Guardian validates accuracy
- Auto-detects outdated documentation

**Use When:** Updating docs, generating skill documentation, validating accuracy, cross-referencing with code

**Location:** `skills/wizard/`

**Integrates With:** Oracle (knowledge source), Summoner (research coordination), Guardian (doc validation)

---

### 🎨 Style Master (CSS & Frontend Styling)

Expert in CSS, design systems, and frontend styling.

**Core Features:**
- Codebase style analysis and design token extraction
- Living style guide generation
- Modern CSS techniques (container queries, custom properties, logical properties)
- Accessibility compliance (WCAG AA/AAA)
- Framework expertise (Tailwind, CSS-in-JS, Sass)

**Use When:** Design systems, visual consistency, CSS guidance, modernizing legacy styles

**Location:** `skills/style-master/`

**Integrates With:** Oracle (remembers style preferences), Summoner (complex refactors)

---

### 📊 Evaluator (Privacy-First Telemetry)

Anonymous, opt-in telemetry and feedback collection for continuous improvement.

**Core Features:**
- Opt-in only (disabled by default)
- No PII collection (anonymous session IDs, daily rotation)
- Local-first storage (you control what's sent)
- GitHub-native feedback (issues and projects)
- Aggregate metrics only (no individual events shared)

**Use When:** Enabling telemetry to help improve skills, submitting feedback, viewing usage analytics

**Location:** `skills/evaluator/`

**Integrates With:** All skills (tracks usage and acceptance rates)

## 🚀 Getting Started

### Marketplace Installation

Add the ClaudeShack marketplace and install the plugin:

```bash
# Add the marketplace
/plugin marketplace add Overlord-Z/ClaudeShack

# Then install the claudeshack plugin from the marketplace
# (Use the /plugin menu to browse and install)
```

All skills included:
- **oracle** - Project memory and learning
- **guardian** - Quality gates and session health
- **summoner** - Multi-agent orchestration
- **wizard** - Documentation maintenance (no hallucinations)
- **style-master** - CSS and frontend styling
- **evaluator** - Privacy-first telemetry

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
Use oracle to remember this pattern
Use guardian to review this code
Use summoner to coordinate [complex multi-component task]
Use wizard to update the documentation
Use style master to analyze our CSS
Use evaluator to view telemetry summary
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
├── skills/                          # All ClaudeShack skills
│   ├── oracle/                      # Project memory & learning
│   ├── guardian/                    # Quality gates & session health
│   ├── summoner/                    # Multi-agent orchestration
│   ├── wizard/                      # Documentation maintenance
│   ├── style-master/                # CSS & frontend styling
│   ├── evaluator/                   # Privacy-first telemetry
│   └── documentation-wizard/        # Legacy doc sync (use wizard instead)
├── .github/                         # GitHub configuration
│   ├── ISSUE_TEMPLATE/              # Bug reports, feature requests, feedback
│   └── PULL_REQUEST_TEMPLATE.md     # PR template
├── README.md                        # This file
├── CONTRIBUTING.md                  # Contribution guidelines
├── CODE_OF_CONDUCT.md               # Community standards
└── REPO_SETUP_GUIDE.md              # Public release setup guide
```

## 🛠️ Skill Development

Want to create your own skill? Check out:
- [Anthropic's Skill Creator Guide](https://github.com/anthropics/skills/tree/main/skill-creator)
- [Official Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)

## 🔗 Skill Synergies

Skills work better together:

- **Guardian + Oracle**: +31% suggestion acceptance rate (Oracle provides validation patterns)
- **Wizard + Summoner**: Comprehensive docs through coordinated research agents
- **Wizard + Guardian**: Validated documentation (Guardian checks accuracy against code)
- **Style Master + Oracle**: Consistent styling through remembered preferences
- **Evaluator**: Tracks all skill usage and acceptance rates (opt-in)

**Example**: Guardian reviews code → validates against Oracle patterns → Wizard updates docs → Style Master ensures consistency → Evaluator tracks what worked.

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
