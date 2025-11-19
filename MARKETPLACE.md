# ClaudeShack Skills Marketplace

**Professional skills for Claude Code developers**

ClaudeShack is a curated marketplace of production-ready Claude Code skills that enhance your development workflow with orchestration, memory, styling, and documentation expertise.

## 🎯 Featured Skills

### 🧙 Summoner - Multi-Agent Orchestration
**Complex task coordination made easy**

Break down complex projects into manageable tasks, coordinate specialized agents, and ensure quality with built-in DRY, CLEAN, and SOLID enforcement.

**Use for**: Large features, refactoring projects, migrations, complex bug fixes

---

### 🧠 Oracle - Project Memory & Learning
**Never forget, always improve**

Track sessions, learn from corrections, build institutional knowledge, and automatically generate scripts for repeated tasks.

**Use for**: Long-term projects, team collaboration, preventing repeated mistakes

---

### 🎨 Style Master - CSS & Frontend Styling
**Beautiful, consistent, accessible UIs**

Analyze codebases, maintain style guides, suggest modern improvements, and ensure WCAG compliance.

**Use for**: Design systems, visual consistency, accessibility, frontend modernization

---

### 📚 Documentation Wizard - Living Documentation
**Documentation that stays in sync**

Auto-generate and maintain README, API docs, ADRs, and onboarding materials from code, Oracle knowledge, and Summoner decisions.

**Use for**: Documentation setup, keeping docs current, generating changelogs

---

## 📦 Installation

### Add ClaudeShack Marketplace

First, add the ClaudeShack marketplace to Claude Code:

```bash
/plugin marketplace add Overlord-Z/ClaudeShack
```

### Browse and Install Skills

After adding the marketplace, use the `/plugin` menu to browse and install:

- **Individual skills**: summoner, oracle, style-master, documentation-wizard
- **Skill bundles**:
  - **all** - All four skills for complete coverage
  - **core** - Summoner + Oracle for essential orchestration and memory
  - **frontend** - Style Master + Documentation Wizard + Oracle for frontend work

### Manual Installation

Clone the repository:
```bash
git clone https://github.com/Overlord-Z/ClaudeShack.git
cd ClaudeShack
```

Skills are automatically available when Claude Code runs in this directory.

## 🔗 Skill Integrations

Skills work better together:

```
┌─────────────┐
│  Summoner   │ ← Orchestrates complex tasks
└──────┬──────┘
       │
       ├─────→ Oracle (remembers patterns)
       ├─────→ Style Master (styling guidance)
       └─────→ Documentation Wizard (documents decisions)

┌─────────────┐
│   Oracle    │ ← Learns and remembers
└──────┬──────┘
       │
       ├─────→ Summoner (provides context)
       ├─────→ Style Master (remembers style preferences)
       └─────→ Documentation Wizard (documents learnings)
```

**Example Workflow**:
1. **Summoner** creates plan for redesigning component library
2. **Oracle** provides context on style preferences and past decisions
3. **Style Master** analyzes current styles and proposes improvements
4. **Summoner** coordinates implementation across components
5. **Documentation Wizard** auto-generates updated style guide
6. **Oracle** records new patterns for future use

## 📊 Skill Catalog

| Skill | Category | Version | Integrations |
|-------|----------|---------|--------------|
| **Summoner** | Orchestration | 1.0.0 | Oracle |
| **Oracle** | Knowledge | 1.0.0 | Summoner, Style Master, Doc Wizard |
| **Style Master** | Frontend | 1.0.0 | Oracle, Doc Wizard |
| **Documentation Wizard** | Documentation | 1.0.0 | Oracle, Summoner, Style Master |

## 🚀 Getting Started

### 1. Choose Your Skills

**For Solo Developers**:
- Start with: Oracle + one domain skill (Style Master or Doc Wizard)
- Add: Summoner for complex projects

**For Teams**:
- Essential: Oracle (shared knowledge) + Documentation Wizard
- Recommended: Summoner + Style Master

**For Large Projects**:
- Install all four skills for complete coverage

### 2. Initialize Oracle (Recommended)

Oracle works best when initialized:
```bash
cd your-project
python /path/to/ClaudeShack/.claude/skills/oracle/Scripts/init_oracle.py
```

### 3. Use Skills in Claude Code

Skills activate automatically based on context:
```
# Summoner activates
"Refactor our authentication system to microservices"

# Oracle provides context
[Remembers: "Prefer JWT tokens, use Redis for sessions"]

# Style Master analyzes
"Analyze our CSS and suggest improvements"

# Documentation Wizard generates
"Generate API documentation from our codebase"
```

Or explicitly:
```
Use the summoner skill to coordinate this complex refactor
```

## 📚 Documentation

Each skill includes comprehensive documentation:

- **SKILL.md**: Complete skill definition and workflows
- **README.md**: Quick start and examples
- **Scripts/**: Automation tools
- **References/**: Templates and guides

## 🆘 Support

### Common Issues

**Q: Skills not activating?**
A: Ensure you're in the ClaudeShack directory or properly installed via plugin system.

**Q: How do skills share information?**
A: Oracle stores knowledge that other skills can access. Summoner creates MCDs that Doc Wizard can read.

**Q: Can I use skills separately?**
A: Yes! Each skill works independently, but they're more powerful together.

### Getting Help

- **Documentation**: See individual skill README files
- **Issues**: [GitHub Issues](https://github.com/Overlord-Z/ClaudeShack/issues)
- **Examples**: See `docs/examples/` for usage scenarios

## 🔄 Updates

Updates are available through the Claude Code plugin system or by pulling the latest from git:
```bash
cd ClaudeShack
git pull origin main
```

## 🤝 Contributing

ClaudeShack welcomes contributions!

- **Suggest Skills**: Open an issue with skill ideas
- **Improve Existing**: Submit PRs for enhancements
- **Share Workflows**: Document how you use skills together

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](./LICENSE) file

---

## 🎓 Skill Comparison

### Summoner vs Manual Planning
| Aspect | Manual | With Summoner |
|--------|--------|---------------|
| Planning | Ad-hoc notes | Structured MCD |
| Quality | Inconsistent | DRY/CLEAN/SOLID enforced |
| Coordination | Mental tracking | Systematic agent management |
| Documentation | Often forgotten | Built into workflow |

### Oracle vs No Memory System
| Aspect | Without Oracle | With Oracle |
|--------|----------------|-------------|
| Corrections | Repeat mistakes | Learn once, remember forever |
| Context | Lost between sessions | Preserved and loaded |
| Automation | Manual repetition | Auto-generated scripts |
| Onboarding | Tribal knowledge | Documented learnings |

### Style Master vs Manual CSS
| Aspect | Manual | With Style Master |
|--------|--------|-------------------|
| Consistency | Ad-hoc | Design system enforced |
| Analysis | Manual review | Automated detection |
| Style Guide | Stale docs | Living documentation |
| Accessibility | Often missed | WCAG built-in |

### Documentation Wizard vs Manual Docs
| Aspect | Manual Docs | With Doc Wizard |
|--------|-------------|-----------------|
| Sync | Often stale | Always current |
| Generation | Time-consuming | Automated |
| ADRs | Rarely created | Auto-generated from decisions |
| Examples | May not work | Validated from code/tests |

---

**ClaudeShack**: Professional skills for professional developers

*Visit [github.com/Overlord-Z/ClaudeShack](https://github.com/Overlord-Z/ClaudeShack) for more information*
