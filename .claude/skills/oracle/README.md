# Oracle Skill

**Project Memory & Learning System for Claude Code**

Oracle is a sophisticated memory and learning system that tracks interactions, learns from corrections, maintains knowledge across sessions, and generates token-efficient context to prevent wasted effort and repeated mistakes.

## The Problem

When working with LLMs across multiple sessions:
- **Context is lost** between sessions
- **Mistakes repeat** because corrections aren't remembered
- **Tokens are wasted** explaining the same things
- **Knowledge doesn't compound** - each session starts from zero
- **Patterns aren't detected** - automation opportunities missed

## The Solution

Oracle provides:
- 📝 **Session Recording** - Track what happens, what works, what doesn't
- 🧠 **Learning from Corrections** - When you correct Claude, it's remembered
- 🔍 **Smart Context Injection** - Load only relevant knowledge when needed
- 📊 **Pattern Detection** - Identify automation opportunities
- 📈 **Knowledge Compounding** - Learning accumulates over time
- 🤖 **Auto-Script Generation** - Automate repeated patterns

## Quick Start

### 1. Initialize Oracle

```bash
python .claude/skills/oracle/scripts/init_oracle.py
```

This creates `.oracle/` directory with knowledge management structure.

### 2. Record Your First Session

After working with Claude:

```bash
python .claude/skills/oracle/scripts/record_session.py --interactive
```

Answer prompts to record what you learned, what was corrected, decisions made.

### 3. Load Context Next Session

```bash
python .claude/skills/oracle/scripts/load_context.py
```

Oracle loads relevant knowledge so Claude starts context-aware.

### 4. Query Knowledge Anytime

```bash
python .claude/skills/oracle/scripts/query_knowledge.py "authentication"
```

Search the knowledge base for relevant information.

## Core Features

### 🎯 Session Recording

Track every session's:
- Activities and accomplishments
- Files changed and why
- Decisions made and rationale
- Learnings and discoveries
- Corrections and mistakes
- Questions asked and answered

**Usage:**
```bash
# Interactive mode (recommended)
python .claude/skills/oracle/scripts/record_session.py --interactive

# Quick mode
python .claude/skills/oracle/scripts/record_session.py \
  --summary "Implemented auth" \
  --learnings "Use bcrypt not md5" \
  --corrections "innerHTML->textContent for user input"
```

### 🧠 Knowledge Management

Oracle maintains categorized knowledge:

| Category | Purpose | Example |
|----------|---------|---------|
| **Patterns** | Code patterns, architecture decisions | "Use factory pattern for DB connections" |
| **Preferences** | Team/user style preferences | "Prefer functional over OOP" |
| **Gotchas** | Known issues, pitfalls | "Connection pool must be closed" |
| **Solutions** | Proven solutions | "Use cursor-based pagination" |
| **Corrections** | Mistakes to avoid | "Don't use innerHTML with user input" |

**Usage:**
```bash
# Search all knowledge
python .claude/skills/oracle/scripts/query_knowledge.py "database"

# Filter by category
python .claude/skills/oracle/scripts/query_knowledge.py --category gotchas

# Filter by priority
python .claude/skills/oracle/scripts/query_knowledge.py --priority critical

# Recent learnings
python .claude/skills/oracle/scripts/query_knowledge.py --recent 10
```

### 💡 Smart Context Injection

Oracle uses **tiered context loading**:

**Tier 1 (Critical)**: Always load
- Critical gotchas
- Recent corrections
- High-priority patterns

**Tier 2 (Relevant)**: Load when relevant
- Related patterns
- Similar solutions
- Contextual preferences

**Tier 3 (Archive)**: Load on request
- Full history
- All solutions
- Complete timeline

**Usage:**
```bash
# Session start context
python .claude/skills/oracle/scripts/generate_context.py --session-start

# Task-specific context
python .claude/skills/oracle/scripts/generate_context.py --task "implement API"

# Update claude.md
python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update
```

### 🔍 Pattern Detection & Automation

Oracle analyzes sessions to find:
- Repeated tasks → automation candidates
- Common corrections → update defaults
- Frequent queries → add to auto-inject
- Token-heavy operations → create scripts

**Usage:**
```bash
# Analyze patterns
python .claude/skills/oracle/scripts/analyze_patterns.py

# Generate automation scripts
python .claude/skills/oracle/scripts/analyze_patterns.py --generate-scripts --threshold 3
```

## Integration

### claude.md Integration

Add Oracle context to `claude.md`:

```markdown
## Project Knowledge (Oracle)

<!-- ORACLE_CONTEXT_START -->
<!-- Auto-generated - Run: python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update -->
<!-- ORACLE_CONTEXT_END -->
```

Update it:
```bash
python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update
```

### Session Start Hook

Auto-load context at session start:

```bash
# Create hook
cat > .claude/hooks/session-start.sh << 'EOF'
#!/bin/bash
python .claude/skills/oracle/scripts/load_context.py
EOF

chmod +x .claude/hooks/session-start.sh
```

### Git Hook Integration

Auto-track commits:

```bash
# Create post-commit hook
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
python .claude/skills/oracle/scripts/record_commit.py
EOF

chmod +x .git/hooks/post-commit
```

See `References/integration-guide.md` for complete integration options.

## Directory Structure

```
.oracle/
├── knowledge/
│   ├── patterns.json          # Code patterns
│   ├── preferences.json       # Team preferences
│   ├── gotchas.json          # Known issues
│   ├── solutions.json        # Proven solutions
│   └── corrections.json      # Historical corrections
├── sessions/
│   └── YYYY-MM-DD_HHMMSS_*.md  # Session logs
├── timeline/
│   └── project_timeline.md   # Chronological history
├── scripts/
│   └── auto_*.sh             # Generated automation
├── hooks/
│   └── *.sh                  # Integration hooks
├── index.json                # Fast lookup index
└── README.md                 # Oracle documentation
```

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `init_oracle.py` | Initialize Oracle for a project |
| `record_session.py` | Record session activities and learnings |
| `query_knowledge.py` | Search knowledge base |
| `generate_context.py` | Generate context summaries |
| `analyze_patterns.py` | Detect patterns and automation opportunities |
| `load_context.py` | Load context (for hooks) |
| `record_commit.py` | Record git commits (for hooks) |

Run any script with `--help` for detailed options.

## Workflow Examples

### Example 1: Daily Development

```bash
# Morning - load context
python .claude/skills/oracle/scripts/load_context.py

# Work with Claude...

# Evening - record session
python .claude/skills/oracle/scripts/record_session.py --interactive
```

### Example 2: Bug Fix

```bash
# Search for related knowledge
python .claude/skills/oracle/scripts/query_knowledge.py "bug keywords"

# Fix bug with Claude...

# Record the fix
python .claude/skills/oracle/scripts/record_session.py \
  --summary "Fixed bug in authentication" \
  --learnings "Root cause was connection timeout - added retry logic"
```

### Example 3: New Feature

```bash
# Get context for the feature
python .claude/skills/oracle/scripts/generate_context.py --task "user profile feature"

# Implement feature...

# Record decisions and patterns
python .claude/skills/oracle/scripts/record_session.py --interactive
# Document: decisions made, patterns used, learnings
```

### Example 4: Weekly Maintenance

```bash
# Analyze for patterns
python .claude/skills/oracle/scripts/analyze_patterns.py --generate-scripts

# Review knowledge base
python .claude/skills/oracle/scripts/query_knowledge.py --summary

# Update claude.md
python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update
```

## Best Practices

### 1. Record Sessions Immediately

Don't wait - record while details are fresh.

### 2. Be Specific in Corrections

❌ "That's wrong"
✅ "Don't use innerHTML -> use textContent to prevent XSS"

### 3. Use Consistent Tags

Review existing tags before creating new ones.

### 4. Prioritize Ruthlessly

- **Critical**: Security, data loss, breaking issues
- **High**: Important patterns, frequent gotchas
- **Medium**: Helpful solutions, preferences
- **Low**: Nice-to-know, historical context

### 5. Leverage Automation

When Oracle suggests automation, implement it.

### 6. Review Monthly

Knowledge bases get stale - review and update regularly.

### 7. Integration is Key

Set up hooks so Oracle works automatically.

## Philosophy

> "What is learned once should never be forgotten. What works should be remembered. What fails should be avoided."

Oracle operates on:
- **KISS**: Simple, readable formats
- **Token Efficiency**: Dense storage, strategic recall
- **Learning from Feedback**: Adapt when corrected
- **Progressive Recall**: Load what's needed, when needed
- **Human-Readable**: No special tools required

## Success Indicators

✅ **Oracle is working when:**
- Similar questions get "I remember we..."
- Corrections don't repeat
- Context is relevant without asking
- Knowledge base grows steadily
- Scripts reduce repetitive tasks
- Timeline shows clear project evolution

❌ **Warning signs:**
- Same corrections repeating
- Duplicate knowledge entries
- Irrelevant context injections
- No automation scripts generated
- Timeline has gaps

## Documentation

- **SKILL.md**: Full skill definition and workflows
- **References/knowledge-schema.md**: Knowledge entry structure
- **References/session-log-template.md**: Session recording template
- **References/integration-guide.md**: Integration options and patterns
- **References/pattern-library.md**: Common patterns and anti-patterns

## Troubleshooting

### Context Not Loading

```bash
# Check Oracle exists
ls -la .oracle/

# Test manually
python .claude/skills/oracle/scripts/load_context.py --verbose
```

### Knowledge Not Relevant

```bash
# Use task-specific context
python .claude/skills/oracle/scripts/generate_context.py --task "specific task"

# Review and update tags
python .claude/skills/oracle/scripts/query_knowledge.py --category patterns
```

### Too Much Context

```bash
# Use tier 1 only (critical)
python .claude/skills/oracle/scripts/generate_context.py --tier 1

# Review priorities
python .claude/skills/oracle/scripts/query_knowledge.py --priority critical
```

## Use Cases

### Solo Developer

- Track personal learnings
- Build institutional knowledge
- Automate repeated tasks
- Prevent repeating mistakes

### Team Project

- Share knowledge via git
- Onboard new members
- Maintain consistency
- Document tribal knowledge

### Open Source

- Help contributors understand patterns
- Document decisions and rationale
- Reduce repetitive questions
- Build comprehensive knowledge base

### Learning New Technology

- Record discoveries
- Track corrections
- Build reference materials
- Compound knowledge over time

## Examples

See `Assets/` directory for:
- Example knowledge entries
- Sample session logs
- Generated automation scripts

## Contributing

Oracle is part of ClaudeShack. Improvements welcome!

- Suggest new patterns
- Propose script enhancements
- Share successful workflows
- Report issues

## Version

**Oracle v1.0**
- Initial release
- Core knowledge management
- Session recording
- Pattern detection
- Context generation
- Automation script generation

---

**"Remember everything. Learn from mistakes. Never waste context."**
