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

**Location:** `.claude/skills/summoner/`

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

**Location:** `.claude/skills/oracle/`

## 🚀 Getting Started

### Installation

This is a skills repository for Claude Code. Skills are automatically available when Claude Code runs in this directory.

### Using Skills

Skills in this repository can be invoked by Claude Code when their trigger contexts are detected, or you can explicitly request a skill:

```
Use the summoner skill to implement [complex task description]
```

## 📁 Repository Structure

```
ClaudeShack/
├── .claude/
│   └── skills/          # All Claude Code skills
│       ├── summoner/    # Multi-agent orchestration skill
│       ├── oracle/      # Project memory & learning skill
│       └── ...          # Future skills
├── README.md
└── docs/                # Additional documentation
```

## 🛠️ Skill Development

Want to create your own skill? Check out:
- [Anthropic's Skill Creator Guide](https://github.com/anthropics/skills/tree/main/skill-creator)
- [Official Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)

## 📚 Resources

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
