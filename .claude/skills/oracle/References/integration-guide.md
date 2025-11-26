# Oracle Integration Guide

This guide explains how to integrate Oracle into your development workflow for maximum effectiveness.

## Integration Methods

### 1. claude.md Integration (Recommended)

The `claude.md` file is automatically loaded by Claude Code at session start. Integrating Oracle here ensures context is always available.

#### Setup

1. Create or open `claude.md` in your project root:

```bash
touch claude.md
```

2. Add Oracle context section:

```markdown
# Project Documentation

## Project Knowledge (Oracle)

<!-- ORACLE_CONTEXT_START -->
<!-- Auto-updated by Oracle - Do not edit manually -->

Run to update:
```bash
python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update
```

<!-- ORACLE_CONTEXT_END -->

## Project Overview

[Your project description...]
```

3. Update Oracle context:

```bash
python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update
```

4. (Optional) Add to your workflow to auto-update after sessions.

#### Auto-Update

Add to your session workflow:

```bash
# After recording a session
python .claude/skills/oracle/scripts/record_session.py --interactive
python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update
```

### 2. Session Start Hooks

Load Oracle context automatically when Claude Code starts.

#### Setup

1. Create hooks directory:

```bash
mkdir -p .claude/hooks
```

2. Create session-start hook:

```bash
cat > .claude/hooks/session-start.sh << 'EOF'
#!/bin/bash
# Load Oracle context at session start

python .claude/skills/oracle/scripts/load_context.py
EOF

chmod +x .claude/hooks/session-start.sh
```

3. Claude Code will run this hook at session start.

### 3. Git Hooks Integration

Track commits in Oracle timeline automatically.

#### Setup

1. Create post-commit hook:

```bash
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# Record commit in Oracle timeline

python .claude/skills/oracle/scripts/record_commit.py
EOF

chmod +x .git/hooks/post-commit
```

2. Commits are now automatically tracked in `.oracle/timeline/project_timeline.md`.

### 4. CI/CD Integration

Update Oracle knowledge as part of your CI/CD pipeline.

#### Example: GitHub Actions

```yaml
name: Update Oracle

on:
  push:
    branches: [ main ]

jobs:
  update-oracle:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Update Oracle Timeline
        run: |
          python .claude/skills/oracle/scripts/record_commit.py

      - name: Update claude.md
        run: |
          python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update

      - name: Commit changes
        run: |
          git config --local user.email "oracle@bot"
          git config --local user.name "Oracle Bot"
          git add claude.md
          git diff --quiet && git diff --staged --quiet || git commit -m "Update Oracle context [skip ci]"
          git push
```

## Workflow Patterns

### Pattern 1: Active Learning

**For:** Projects where you're learning and making frequent corrections.

**Workflow:**
1. Work on tasks
2. When corrected, immediately record: `python .claude/skills/oracle/scripts/record_session.py --corrections "wrong->right"`
3. Context auto-updates for next session
4. Corrections are avoided in future

**Best for:** New projects, learning new technologies

### Pattern 2: Pattern Detection

**For:** Mature projects with established patterns.

**Workflow:**
1. Record sessions regularly
2. Weekly: Run pattern analysis `python .claude/skills/oracle/scripts/analyze_patterns.py --generate-scripts`
3. Review and customize generated scripts
4. Use scripts for repeated tasks

**Best for:** Established projects, teams with repeated workflows

### Pattern 3: Knowledge Sharing

**For:** Team projects where knowledge needs to be shared.

**Workflow:**
1. Each team member records sessions
2. Knowledge base synced via git
3. `claude.md` updated and committed
4. All team members benefit from shared learning

**Best for:** Team projects, open source projects

### Pattern 4: Documentation Sync

**For:** Projects where documentation must stay current.

**Workflow:**
1. Record sessions with learnings
2. Use Oracle with documentation skill/tool
3. Auto-generate documentation updates from learnings
4. Review and commit documentation

**Best for:** Projects requiring up-to-date docs

## Context Injection Strategies

### Strategy 1: Minimal Context (Default)

Load only critical and high-priority items.

```bash
python .claude/skills/oracle/scripts/generate_context.py --tier 1
```

**Pros:** Low token usage, fast loading
**Cons:** May miss relevant context
**Use when:** Token budget is tight

### Strategy 2: Relevant Context

Load context relevant to current task.

```bash
python .claude/skills/oracle/scripts/generate_context.py --task "implement authentication"
```

**Pros:** Highly relevant, moderate token usage
**Cons:** Requires knowing the task upfront
**Use when:** Starting a specific task

### Strategy 3: Full Context

Load all available knowledge.

```bash
python .claude/skills/oracle/scripts/generate_context.py --tier 3
```

**Pros:** Complete picture, no missing context
**Cons:** High token usage, may be overwhelming
**Use when:** Complex tasks, architecture decisions

## Maintenance

### Weekly Maintenance

```bash
# 1. Analyze patterns
python .claude/skills/oracle/scripts/analyze_patterns.py

# 2. Generate automation scripts
python .claude/skills/oracle/scripts/analyze_patterns.py --generate-scripts

# 3. Update claude.md
python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update

# 4. Review knowledge base
python .claude/skills/oracle/scripts/query_knowledge.py --summary
```

### Monthly Maintenance

1. Review corrections - are patterns emerging?
2. Update knowledge priorities
3. Archive old sessions (optional)
4. Review automation scripts - are they being used?
5. Clean up duplicate knowledge entries

### Knowledge Curation

Periodically review and curate:

```bash
# Find rarely used knowledge
python .claude/skills/oracle/scripts/query_knowledge.py --sort used

# Find old corrections (may be outdated)
python .claude/skills/oracle/scripts/query_knowledge.py --category corrections --sort recent
```

## Troubleshooting

### Oracle Not Loading

**Problem:** Context not appearing at session start.

**Solutions:**
1. Check `.claude/hooks/session-start.sh` exists and is executable
2. Verify Oracle is initialized: `ls -la .oracle/`
3. Test manually: `python .claude/skills/oracle/scripts/load_context.py --verbose`

### Context Too Large

**Problem:** Too much context being injected.

**Solutions:**
1. Use tier 1 context: `--tier 1`
2. Increase priorities of only critical items
3. Use task-specific context instead of session-start
4. Review and archive old knowledge

### Knowledge Not Relevant

**Problem:** Loaded knowledge doesn't apply to current task.

**Solutions:**
1. Use task-specific context generation
2. Improve tags on knowledge entries
3. Use more specific queries
4. Update priorities to better reflect importance

### Scripts Not Generating

**Problem:** Pattern analysis doesn't find automation candidates.

**Solutions:**
1. Lower threshold: `--threshold 2`
2. Record more sessions
3. Be consistent in activity descriptions
4. Manually identify patterns and add as automation opportunities

## Best Practices

### 1. Record Sessions Consistently

Don't wait until end of day - record immediately after completing work while details are fresh.

### 2. Be Specific in Corrections

Instead of: "That's wrong"
Use: "Don't use innerHTML for user input -> use textContent to prevent XSS"

### 3. Tag Thoughtfully

Use consistent, meaningful tags. Review existing tags before creating new ones.

### 4. Prioritize Ruthlessly

Not everything is critical. Save high/critical priorities for things that truly matter.

### 5. Review Regularly

Knowledge bases become stale. Review and update monthly.

### 6. Use Automation

If pattern analysis suggests automation, implement it. Oracle works best when reducing repetitive LLM usage.

### 7. Share Knowledge

In team settings, commit Oracle knowledge to git (exclude sensitive session logs via .gitignore).

---

**Integration Version**: 1.0
**Last Updated**: 2025-11-19
