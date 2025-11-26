# ClaudeShack: Lean & Autonomous Philosophy

## Core Principle

**Zero-friction intelligence.** The user should never have to:
- Remind Claude of something Oracle knows
- Ask Claude to check for patterns
- Tell Claude to use current documentation
- Repeat corrections already given
- Nudge Claude to be proactive

## The Lean Architecture

### What Goes Where

| Information | Location | When Loaded |
|-------------|----------|-------------|
| Project identity (what it does) | `claude.md` | Always (tiny) |
| Skills available | `claude.md` | Always (tiny) |
| Top 3-5 critical gotchas | `claude.md` | Always (tiny) |
| Project patterns & conventions | `.oracle/knowledge/` | Auto-queried when relevant |
| Past corrections | `.oracle/knowledge/corrections.json` | Auto-queried before similar work |
| Session history | `.oracle/sessions/` | On demand |
| Current library documentation | Context7 MCP | Auto-fetched when library mentioned |

### What Does NOT Go in claude.md

- Full Oracle knowledge dumps
- Library documentation
- Comprehensive project history
- Everything that can be fetched dynamically

**claude.md target size: < 50 lines**

## Autonomous Behavior Rules

### For ALL ClaudeShack Skills

```
BEFORE you write code:
  → Check Oracle for relevant patterns/gotchas
  → If using a library, get current docs via Context7

WHEN user corrects you:
  → IMMEDIATELY record in Oracle (don't wait to be asked)
  → Acknowledge you've recorded it
  → Don't make this mistake again

WHEN you see a familiar topic:
  → Check if Oracle has knowledge on it
  → Apply known patterns automatically
  → Mention "Based on project patterns..." if relevant

WHEN user asks about a library/framework:
  → Context7 for current documentation
  → Oracle for project-specific usage
  → Combine both without being asked
```

### Oracle Auto-Behavior

| Trigger | Automatic Action |
|---------|------------------|
| Starting work on file X | Query Oracle: patterns related to X |
| User mentions library Y | Query Oracle: project's Y patterns |
| User says "that's wrong" | Record correction immediately |
| User says "always/never" | Record as pattern/gotcha |
| Error matches known pattern | Surface the gotcha proactively |

### Context7 Auto-Behavior

| Trigger | Automatic Action |
|---------|------------------|
| User mentions a library | Fetch current docs for that library |
| Version mismatch suspected | Fetch version-specific docs |
| API usage question | Get current API reference |

**Note**: Context7 provides GENERIC current docs. Oracle provides PROJECT-SPECIFIC usage.

## The Learning Loop

```
User works with Claude
        ↓
Claude makes a mistake
        ↓
User corrects Claude
        ↓
Oracle records correction IMMEDIATELY
        ↓
Next similar situation:
  - Oracle auto-surfaces correction
  - Claude applies it automatically
  - User never has to repeat
        ↓
Knowledge compounds over time
```

## Anti-Patterns (What NOT to Do)

### DON'T: Wait to be asked
```
❌ User: "Check Oracle for patterns"
❌ User: "Remember I told you about X"
❌ User: "Use context7 to get the docs"
```

### DO: Act autonomously
```
✅ Claude: "Based on Oracle patterns for this project..."
✅ Claude: "I've recorded this correction in Oracle"
✅ Claude: "Current Prisma 7 docs show X, and your project uses Y pattern..."
```

### DON'T: Bloat claude.md
```
❌ Dumping full Oracle knowledge
❌ Including library documentation
❌ Writing comprehensive guides
```

### DO: Keep claude.md minimal
```
✅ Project name and purpose (2-3 lines)
✅ Available skills (list)
✅ Top 3-5 critical gotchas only
```

### DON'T: Use outdated knowledge
```
❌ "In Prisma 5, you would..."
❌ "React class components typically..."
❌ Assuming old API patterns
```

### DO: Fetch current + apply project-specific
```
✅ Context7 → Current library docs
✅ Oracle → Project's specific patterns
✅ Combine both in response
```

## Skill Responsibilities

### Oracle
- Store/retrieve project-specific knowledge
- Record corrections immediately
- Track patterns, gotchas, preferences
- Provide historical context

### Context7 (External MCP)
- Fetch current library documentation
- Provide version-specific API references
- Eliminate outdated training data assumptions

### Guardian
- Auto-review significant code changes
- Validate against Oracle patterns
- Learn from acceptance/rejection

### Smart-Init
- Discover project context interactively
- Seed Oracle with confirmed knowledge
- Set up Context7 if not installed
- Establish autonomous behavior from start

## Setup for Autonomous Operation

1. **Install Context7 MCP**
   ```bash
   claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
   ```

2. **Initialize with Smart-Init**
   ```
   Use smart-init skill to set up ClaudeShack
   ```

3. **Minimal claude.md**
   ```markdown
   # Project Name
   Brief description.

   ## Skills: oracle, guardian, summoner, wizard

   ## Critical Gotchas
   - [Only 3-5 most critical items]
   ```

4. **Oracle Hook (Optional but Recommended)**
   - Auto-loads critical context at session start
   - See `.claude/skills/oracle/scripts/HOOK_SETUP.md`

## Success Metrics

**The system is working when:**
- User never repeats a correction
- Claude proactively applies project patterns
- Library usage reflects current APIs
- claude.md stays under 50 lines
- Sessions feel like Claude "knows" the project

**Warning signs:**
- User saying "I told you before..."
- Claude using outdated library patterns
- claude.md growing bloated
- User manually invoking skills

---

**"Intelligence without friction. Memory without bloat. Learning without repetition."**
