# Oracle Pattern Library

Common patterns, solutions, and best practices for the Oracle knowledge management system.

## Knowledge Entry Patterns

### Pattern: Security Critical

**When:** Recording security-related knowledge

**Structure:**
```json
{
  "category": "gotcha" or "correction",
  "priority": "critical",
  "title": "Always [security practice]",
  "content": "Security vulnerability description and correct approach",
  "context": "When handling [user input/authentication/etc]",
  "tags": ["security", "xss|sql-injection|csrf|etc"]
}
```

**Example:**
- Input validation
- Authentication bypasses
- Injection vulnerabilities
- Data exposure

### Pattern: Performance Optimization

**When:** Recording performance-related learnings

**Structure:**
```json
{
  "category": "solution",
  "priority": "high",
  "title": "Use [optimized approach] for [use case]",
  "content": "Performance problem and solution with metrics",
  "examples": ["Before/after code"],
  "tags": ["performance", "optimization"]
}
```

**Example:**
- Caching strategies
- Query optimization
- Algorithm improvements

### Pattern: Common Mistake

**When:** User corrects a repeated mistake

**Structure:**
```json
{
  "category": "correction",
  "priority": "high",
  "title": "Don't [wrong approach]",
  "content": "❌ Wrong: [what not to do]\\n✓ Right: [correct approach]\\nReason: [why]",
  "context": "When [situation]",
  "tags": ["common-mistake"]
}
```

**Example:**
- API misuse
- Framework gotchas
- Language quirks

## Session Recording Patterns

### Pattern: Bug Fix Session

**When:** Session focused on fixing a bug

**Template:**
```markdown
## Summary
Fixed [bug description]

## Activities
- Identified root cause in [location]
- Implemented fix in [location]
- Added tests to prevent regression

## Changes Made
- File: [path]
  - Change: [what changed]
  - Reason: Fix for [bug]

## Learnings
- 🟡 [HIGH] [Root cause and how to prevent]

## Corrections (if applicable)
- What was wrong: [incorrect assumption/approach]
- What's right: [correct understanding/approach]
```

### Pattern: Feature Implementation

**When:** Adding new functionality

**Template:**
```markdown
## Summary
Implemented [feature name]

## Activities
- Designed [component/system]
- Implemented [components]
- Added tests
- Updated documentation

## Decisions
- Decision: [technical decision made]
  - Rationale: [why this approach]
  - Alternatives: [other options considered]

## Learnings
- [Patterns established]
- [Solutions used]
```

### Pattern: Refactoring Session

**When:** Improving existing code

**Template:**
```markdown
## Summary
Refactored [what] to [improvement]

## Activities
- Analyzed current implementation
- Refactored [components]
- Verified no breaking changes

## Changes Made
- [List of files and changes]

## Learnings
- [Patterns applied]
- [Anti-patterns removed]
```

## Query Patterns

### Pattern: Pre-Task Context

**When:** Starting a new task

**Command:**
```bash
python .claude/skills/oracle/scripts/query_knowledge.py --task "implement [feature]" --priority high
```

**What it does:**
- Surfaces relevant patterns
- Shows related solutions
- Highlights potential gotchas

### Pattern: Post-Correction

**When:** After being corrected

**Command:**
```bash
python .claude/skills/oracle/scripts/record_session.py --corrections "wrong->right"
python .claude/skills/oracle/scripts/query_knowledge.py --category corrections --recent 10
```

**What it does:**
- Records the correction
- Shows recent corrections to identify patterns

### Pattern: Weekly Review

**When:** Regular maintenance

**Commands:**
```bash
# See what we've learned
python .claude/skills/oracle/scripts/query_knowledge.py --recent 20

# Find automation opportunities
python .claude/skills/oracle/scripts/analyze_patterns.py

# Update documentation
python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update
```

## Integration Patterns

### Pattern: Continuous Learning

**Setup:**
1. `claude.md` with Oracle section
2. Session start hook loads context
3. After each session: record learnings
4. Weekly: analyze patterns

**Benefit:** Continuous improvement, knowledge compounds

### Pattern: Team Knowledge Base

**Setup:**
1. Oracle in git repository
2. `.gitignore` excludes sensitive session logs
3. `claude.md` committed and shared
4. Team members contribute learnings

**Benefit:** Shared institutional knowledge

### Pattern: Documentation Sync

**Setup:**
1. Record sessions with learnings
2. Oracle context in `claude.md`
3. Use learnings to update docs
4. Keep docs and knowledge in sync

**Benefit:** Documentation stays current

## Automation Patterns

### Pattern: Repeated Command

**Detection:**
Activity appears 3+ times: "Run tests"

**Action:**
```bash
# Oracle generates
./auto_run_tests.sh

# Which contains
#!/bin/bash
npm test
# or pytest
# or cargo test
```

**Usage:** Use script instead of asking Claude

### Pattern: Multi-Step Process

**Detection:**
Same sequence appears repeatedly:
1. "Build project"
2. "Run linter"
3. "Run tests"

**Action:**
```bash
# Oracle generates
./auto_pre_commit.sh

# Which contains
#!/bin/bash
npm run build && npm run lint && npm test
```

### Pattern: Context Generation

**Detection:**
Repeatedly asking about same topic

**Action:**
Add to claude.md auto-inject:
```markdown
## Authentication Context

[Relevant knowledge auto-injected]
```

## Anti-Patterns (What NOT to Do)

### Anti-Pattern: Recording Everything

❌ **Don't:** Record every tiny action
✓ **Do:** Record meaningful learnings and corrections

**Why:** Bloats knowledge base, harder to find relevant info

### Anti-Pattern: Vague Entries

❌ **Don't:** "Something about databases"
✓ **Do:** "Use connection pooling for database connections to prevent connection exhaustion"

**Why:** Vague entries aren't useful for recall

### Anti-Pattern: Duplicate Knowledge

❌ **Don't:** Create new entry for same knowledge
✓ **Do:** Update existing entry or add examples

**Why:** Duplicates cause confusion and bloat

### Anti-Pattern: Wrong Priorities

❌ **Don't:** Mark everything as critical
✓ **Do:** Save critical for security, data loss, breaking issues

**Why:** Dilutes importance, everything seems urgent

### Anti-Pattern: No Tags

❌ **Don't:** Skip tags thinking title is enough
✓ **Do:** Add 2-4 relevant tags

**Why:** Tags enable better search and categorization

### Anti-Pattern: Never Reviewing

❌ **Don't:** Set and forget
✓ **Do:** Review monthly, update priorities, archive old entries

**Why:** Stale knowledge becomes misleading

### Anti-Pattern: Ignoring Automations

❌ **Don't:** Keep asking LLM for same repeated task
✓ **Do:** Use or create automation scripts

**Why:** Wastes tokens and time on deterministic tasks

## Common Use Cases

### Use Case 1: Onboarding New Developers

**Situation:** New team member joining project

**Solution:**
```bash
# Generate comprehensive onboarding context
python .claude/skills/oracle/scripts/generate_context.py --tier 2 > onboarding.md

# Include:
# - Critical gotchas
# - Key patterns
# - Team preferences
# - Common solutions
```

### Use Case 2: Context Switching

**Situation:** Coming back to project after time away

**Solution:**
```bash
# Load session start context
python .claude/skills/oracle/scripts/load_context.py

# Review recent sessions
python .claude/skills/oracle/scripts/query_knowledge.py --recent 10

# Review project timeline
cat .oracle/timeline/project_timeline.md | tail -50
```

### Use Case 3: Bug Investigation

**Situation:** Investigating a bug

**Solution:**
```bash
# Search for related issues
python .claude/skills/oracle/scripts/query_knowledge.py "bug-related-keywords"

# Check if similar bug was fixed before
python .claude/skills/oracle/scripts/query_knowledge.py --category gotchas --tags bug

# After fix, record to prevent recurrence
python .claude/skills/oracle/scripts/record_session.py --interactive
```

### Use Case 4: Architecture Decision

**Situation:** Making important architectural choice

**Solution:**
```bash
# Review existing patterns
python .claude/skills/oracle/scripts/query_knowledge.py --category patterns

# Review past decisions
grep "Decision:" .oracle/sessions/*.md

# After deciding, record rationale
python .claude/skills/oracle/scripts/record_session.py \
  --summary "Decided to use [approach]" \
  --learnings "Use [approach] because [rationale]"
```

## Success Metrics

Track these to measure Oracle effectiveness:

### Metric 1: Correction Reduction

**Measure:** Count corrections per week

**Target:** Declining trend (learning from mistakes)

**How:**
```bash
grep -c "## Corrections" .oracle/sessions/*.md
```

### Metric 2: Knowledge Reuse

**Measure:** use_count in knowledge entries

**Target:** Increasing use counts on valuable entries

**How:**
```bash
python .claude/skills/oracle/scripts/query_knowledge.py --sort used
```

### Metric 3: Automation Adoption

**Measure:** Generated scripts being used

**Target:** High usage of automation scripts

**How:**
Check git history for manual vs scripted operations

### Metric 4: Context Relevance

**Measure:** How often injected context is actually useful

**Target:** High relevance rate

**How:**
Subjective assessment during sessions

---

**Pattern Library Version**: 1.0
**Last Updated**: 2025-11-19
