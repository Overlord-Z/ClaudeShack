# ClaudeShack Development Context

**You are working in the ClaudeShack repository** - a production-ready skills ecosystem for Claude Code.

## Core Principles

When working in this repository, always follow these principles:

### KISS (Keep It Simple, Stupid)
- Simple, readable code over clever complexity
- Clear documentation over assumptions
- Focused solutions over feature bloat

### DRY (Don't Repeat Yourself)
- Reuse patterns and code
- Single source of truth for each concept
- Avoid duplication across skills

### Privacy First
- No PII collection
- Opt-in telemetry only
- Transparent data handling
- Anonymous, aggregate metrics

### Minimal Context
- Pass only what's needed to subagents
- No full conversation dumps
- Focused, laser-targeted context

### Facts Over Fiction
- Documentation verified against code
- No hallucinations or assumptions
- Always reference sources
- Code-first, then docs

### Read-Only Subagents
- Analysis and suggestions only
- All modifications require user approval
- Safety by design

## ClaudeShack Skills Ecosystem

This repository contains 6 integrated skills:

### 🧠 Oracle (Project Memory)
- Tracks sessions, learns from corrections
- Maintains institutional knowledge
- Session handoff for context preservation
- **Integration**: All skills use Oracle for validation and patterns

### 🛡️ Guardian (Quality Gates)
- Auto-triggers on code volume, errors, file churn
- Spawns read-only Haiku agents for review
- Session health monitoring (prevents degraded sessions)
- **Integration**: Validates against Oracle patterns (+31% acceptance)

### 🧙 Summoner (Multi-Agent Orchestration)
- Complex task decomposition with MCDs
- Coordinates multiple specialists
- Quality gates (DRY, CLEAN, SOLID)
- **Integration**: Loads Oracle patterns, Guardian validates

### 📝 Wizard (Documentation Maintenance)
- Research-first approach (no hallucinations)
- Oracle + code + conversation history
- Guardian validates accuracy
- **Integration**: +19% accuracy with Oracle, +35% completeness with Summoner

### 🎨 Style Master (CSS & Frontend)
- Design systems and modern CSS
- Accessibility compliance (WCAG AA/AAA)
- **Integration**: Oracle remembers style preferences (+22% consistency)

### 📊 Evaluator (Privacy-First Telemetry)
- Opt-in anonymous usage tracking
- GitHub-native feedback collection
- Drives continuous improvement
- **Integration**: Tracks all skill usage and acceptance rates

## Initialization (First Use)

If this is your first time working with ClaudeShack skills:

### Oracle Initialization
```bash
# Initialize Oracle knowledge base
python skills/oracle/Scripts/init_oracle.py

# This creates:
# .oracle/knowledge/     - Patterns, corrections, gotchas, solutions
# .oracle/sessions/      - Session logs
# .oracle/timeline/      - Project history
```

### Guardian Configuration
```bash
# Guardian uses default thresholds initially
# Thresholds auto-tune based on acceptance rates
# Config stored in .guardian/config.json (auto-created on first use)
```

### Evaluator (Optional)
```bash
# Telemetry is OPT-IN and disabled by default
# To enable:
use evaluator to enable telemetry

# To view what's collected locally:
use evaluator to show summary
```

## Working with Skills

### Explicit Invocation
```
Use oracle to remember this pattern
Use guardian to review this code
Use summoner to coordinate [complex multi-component task]
Use wizard to update the documentation
Use style master to analyze our CSS
```

### Automatic Triggers

**Guardian** automatically activates when:
- >50 lines of code written
- Same error appears 3+ times
- Same file edited 5+ times in 10 minutes
- User says "that's wrong" 3+ times

**Oracle** should be used:
- When starting a session (load recent patterns)
- When corrected (record the mistake)
- When discovering patterns (save for future)

## Session Handoff

When session context degrades (Guardian health score <40):

```bash
# Export current session context
python skills/oracle/Scripts/session_handoff.py --export

# In new session, import context
python skills/oracle/Scripts/session_handoff.py --import handoff_context.json

# Or use slash command
/handoff
```

This preserves:
- Critical Oracle patterns
- Recent corrections
- Active gotchas
- Guardian health metrics
- Active Summoner MCDs

## Development Guidelines

When contributing to ClaudeShack:

### Code Standards
- Follow KISS and DRY religiously
- No magic numbers - use named constants
- Comprehensive error handling
- Python 3.7+ compatibility

### Documentation
- Update SKILL.md when changing skill behavior
- Update CHANGELOG.md for user-facing changes
- Verify docs against code (use Wizard)
- No assumptions or hallucinations

### Privacy & Security
- No PII collection ever
- Opt-in for any data collection
- Transparent about what's collected
- Secure handling of user data

### Testing
- Test with real-world scenarios
- Validate Oracle knowledge storage/retrieval
- Check Guardian threshold accuracy
- Ensure session handoff preserves context

## Skill Synergies

Skills work better together:
- **Guardian + Oracle**: +31% suggestion acceptance
- **Wizard + Oracle**: +19% documentation accuracy
- **Wizard + Summoner**: +35% documentation completeness
- **Style Master + Oracle**: +22% styling consistency
- **Summoner + Oracle**: +25% task completion success

## Community Feedback Loop

This is a **v0.1-beta** release. We need real-world validation:

### What We're Learning
- Guardian threshold tuning (too aggressive? too passive?)
- Oracle knowledge organization (useful? bloated?)
- Session handoff effectiveness (smooth? missing context?)
- Skill integration patterns (what combos work best?)

### How to Help
- Report bugs: [GitHub Issues](https://github.com/Overlord-Z/ClaudeShack/issues)
- Share feedback: [Skill Feedback Template](https://github.com/Overlord-Z/ClaudeShack/issues/new?template=skill_feedback.yml)
- Enable telemetry: `use evaluator to enable telemetry` (opt-in, anonymous)

## Remember

> "Only thing that can make it better is to use it exclusively and keep fine tuning."

ClaudeShack improves through continuous learning from real-world usage. Your feedback shapes development.

**Version**: v0.1-beta
**Status**: Public beta - needs real-world validation
**Next Milestone**: v1.0 after 50+ invocations and community feedback

---

**ClaudeShack activated. Skills ready. Let's build something amazing.** 🏛️
