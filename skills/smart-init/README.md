# Smart Init

**Interactive, Intelligent ClaudeShack Initialization**

Smart Init doesn't just create empty directories - it **understands your project** and seeds Oracle with verified, high-quality knowledge.

## Why Smart Init?

| Traditional Init | Smart Init |
|------------------|------------|
| Creates empty `.oracle/` | Discovers languages, frameworks, patterns |
| Generic config | Project-specific Guardian thresholds |
| No knowledge | Seeds Oracle with discovered + confirmed knowledge |
| Hope it works | Verifies understanding through conversation |

## How It Works

### Phase 1: Discovery
Automatically analyzes:
- Languages (by file count and LOC)
- Frameworks (React, Django, Express, etc.)
- Conventions (linting, formatting, git style)
- Project structure
- Existing documentation
- Conversation history (if available)

### Phase 2: Discussion
Presents findings and asks targeted questions:
- "Is this understanding correct?"
- "What are the top gotchas I should know?"
- "Any tribal knowledge that isn't documented?"

### Phase 3: Seeding
Creates Oracle entries from **confirmed** understanding:
- Patterns → from code + your confirmation
- Gotchas → from history + your input
- Preferences → from config + your clarification

### Phase 4: Learning
After setup, the system improves over use:
- Corrections get recorded
- Guardian learns what you accept/reject
- Patterns get refined
- Knowledge compounds

## Usage

### Via Skill Invocation
```
Use the smart-init skill to initialize ClaudeShack for this project
```

### Via Discovery Script
```bash
# See what Smart Init would discover
python .claude/skills/smart-init/scripts/discover.py

# JSON output for automation
python .claude/skills/smart-init/scripts/discover.py --json
```

## What Gets Created

After Smart Init completes:

```
.oracle/
├── knowledge/
│   ├── patterns.json      # Discovered + confirmed patterns
│   ├── gotchas.json       # Critical issues to watch for
│   ├── preferences.json   # Team/user preferences
│   ├── corrections.json   # (empty, learns over time)
│   └── solutions.json     # (empty, learns over time)
├── sessions/
├── timeline/
└── index.json

.guardian/
└── config.json            # Project-appropriate thresholds

claude.md                  # Updated with project context
```

## Knowledge Quality

Every seeded entry has:
- **Source tracking**: `learned_from` field
- **Confidence level**: Based on discovery + confirmation
- **Appropriate priority**: Only critical if truly critical

### Source Types
- `smart-init-discovery` - Found in code/config
- `smart-init-history` - From conversation history
- `smart-init-user` - Directly from user input
- `smart-init-confirmed` - Discovered + user confirmed

## Example Session

```
User: Initialize ClaudeShack for this project

Smart Init: [Runs discovery for ~30 seconds]

"I've analyzed your project. Here's what I found:

**Project**: my-app
**Stack**: TypeScript + React + Express + PostgreSQL

I detected:
- Conventional commits style
- ESLint with Airbnb config
- Jest for testing
- Prisma for database

Questions:
1. Is PostgreSQL your primary database?
2. Any critical gotchas about the database I should know?
3. What coding patterns should I enforce?"

User: "Yes PostgreSQL. Watch out - connection pool doesn't auto-close.
       We prefer async/await everywhere."

Smart Init: "Got it! Setting up Oracle with:
- [CRITICAL] Database pool must be explicitly closed
- [HIGH] Prefer async/await over callbacks
- [MEDIUM] Use Prisma for all database operations

Creating directories and seeding knowledge..."
```

## Fine-Tuning Over Use

After initialization, the system self-improves:

1. **You correct Claude** → Recorded in Oracle corrections
2. **Guardian reviews code** → Learns what you accept/reject
3. **You record sessions** → Patterns get refined
4. **Weekly analysis** → Finds automation opportunities

The knowledge base **grows smarter** over time without manual maintenance.

## Scripts

| Script | Purpose |
|--------|---------|
| `discover.py` | Analyze project and output findings |

## Integration

Smart Init sets up the full ecosystem:
- **Oracle**: Seeded with project knowledge
- **Guardian**: Calibrated for project complexity
- **Wizard**: Has accurate project understanding
- **Summoner**: Knows constraints for orchestration

---

**"Understanding first. Setup second. Learning forever."**
