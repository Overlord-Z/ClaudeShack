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

## 🎨 Creating Templates

ClaudeShack skills are extensible through templates. Add your own without modifying core skills.

### Guardian Templates

Create custom review templates in `skills/guardian/Templates/`:

```json
{
  "name": "API Security Review",
  "description": "Review API endpoints for security issues",
  "version": "1.0.0",
  "focus_areas": [
    "Authentication and authorization",
    "Input validation and sanitization",
    "Rate limiting",
    "SQL injection prevention",
    "API key exposure"
  ],
  "oracle_patterns": [
    "api-security",
    "authentication",
    "rate-limiting"
  ],
  "questions": [
    "Are all endpoints authenticated?",
    "Is input properly validated?",
    "Are API keys in environment variables?"
  ],
  "severity_thresholds": {
    "critical": ["sql_injection", "auth_bypass", "key_exposure"],
    "high": ["missing_auth", "weak_validation"],
    "medium": ["missing_rate_limit", "verbose_errors"]
  }
}
```

**Available Templates:**
- `security_review.json` - OWASP Top 10 security review
- `performance_review.json` - Performance optimization
- `feature_planning.json` - Complex task breakdown
- `session_health.json` - Session degradation monitoring

### Summoner MCD Templates

Create Mission Control Document templates in `skills/summoner/References/`:

- Define standard task structures
- Include quality gate checklists
- Specify agent specifications
- Add context boundaries

### Custom Slash Commands

Add your own commands in `.claude/commands/`:

```markdown
# /mycommand.md

You are helping with [specific task].

## Context
[Provide context for this command]

## Your Task
1. [Step 1]
2. [Step 2]

## Remember
- [Key principle 1]
- [Key principle 2]
```

See existing commands:
- `/handoff` - Session handoff with context preservation

## 🔗 Skill Synergies

Skills work better together:

- **Guardian + Oracle**: +31% suggestion acceptance rate (Oracle provides validation patterns)
- **Wizard + Summoner**: Comprehensive docs through coordinated research agents
- **Wizard + Guardian**: Validated documentation (Guardian checks accuracy against code)
- **Style Master + Oracle**: Consistent styling through remembered preferences
- **Evaluator**: Tracks all skill usage and acceptance rates (opt-in)

**Example**: Guardian reviews code → validates against Oracle patterns → Wizard updates docs → Style Master ensures consistency → Evaluator tracks what worked.

## 🔄 Community Feedback Loop

ClaudeShack improves through **continuous learning from real-world usage**. Here's how your feedback shapes development:

### How It Works

```
1. You Use Skills
   ↓
2. Evaluator Tracks (opt-in, anonymous)
   - Which skills are used most
   - Which suggestions are accepted/rejected
   - Session health patterns
   - Integration effectiveness
   ↓
3. Community Submits Feedback
   - GitHub Issues (bug reports, feature requests)
   - Skill Feedback template (what works, what doesn't)
   - Discussions (Q&A, ideas, showcases)
   ↓
4. Data Analysis
   - Aggregate Evaluator metrics (no individual data)
   - Identify patterns in feedback
   - Guardian threshold tuning needs
   - Oracle knowledge gaps
   ↓
5. Skill Improvements
   - Adjust Guardian sensitivity based on acceptance rates
   - Add Oracle patterns from common corrections
   - New Guardian templates for common reviews
   - Summoner MCD refinements
   - Documentation clarifications
   ↓
6. Release Updates
   - Changelog with what changed and why
   - Performance metrics (before/after)
   - Credit to contributors
   ↓
Back to #1 (continuous improvement)
```

### What Gets Improved

**From Evaluator Metrics:**
- **Guardian thresholds**: If suggestion acceptance is low, triggers are too aggressive
- **Oracle patterns**: Track which patterns prevent the most errors
- **Skill synergies**: Measure which combinations work best
- **Session health**: Learn what signals predict degradation

**From GitHub Feedback:**
- **New templates**: Users request reviews for specific domains (database, accessibility, etc.)
- **Documentation gaps**: Questions reveal what's unclear
- **Feature requests**: What capabilities are missing
- **Bug reports**: What's not working as designed

### Example Improvements

**Real scenario:**
```
Week 1: Evaluator shows Guardian triggers 50 times, but only 20% accepted
  ↓
Analysis: Triggering too aggressively, users find it annoying
  ↓
Week 2: Raise lines_threshold from 50 to 75
  ↓
Week 3: Evaluator shows 40 triggers, 65% accepted (much better!)
  ↓
Record in Oracle: "lines_threshold=75 optimal for this codebase type"
```

### Transparency Reports

We publish quarterly reports showing:
- Total opt-in users (approximate)
- Aggregate skill usage statistics
- Top improvement themes from feedback
- Changes made and why
- Performance improvements

**Next report**: Q2 2025

### Your Feedback Matters

**Submit Feedback:**
- 🐛 [Bug Report](https://github.com/Overlord-Z/ClaudeShack/issues/new?template=bug_report.yml)
- ✨ [Feature Request](https://github.com/Overlord-Z/ClaudeShack/issues/new?template=feature_request.yml)
- ⭐ [Skill Feedback](https://github.com/Overlord-Z/ClaudeShack/issues/new?template=skill_feedback.yml)
- 💬 [Join Discussions](https://github.com/Overlord-Z/ClaudeShack/discussions)

**Enable Telemetry (opt-in):**
```bash
# Help improve skills with anonymous usage data
use evaluator to enable telemetry

# View what's collected locally
use evaluator to show summary
```

**What We DON'T Collect:**
- ❌ Your code or file contents
- ❌ Project names or paths
- ❌ Personal information (name, email, IP)
- ❌ Conversation history
- ❌ Anything identifiable

**What We DO Collect (if you opt in):**
- ✅ Skill usage counts (which skills, how often)
- ✅ Success/failure rates (did the skill work?)
- ✅ Suggestion acceptance rates (Guardian only)
- ✅ Session health metrics (aggregate patterns)
- ✅ Performance timings (how fast skills run)

All data is **anonymous, aggregate, and local-first**. You control what gets sent.

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
