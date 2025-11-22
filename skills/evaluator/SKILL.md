---
name: evaluator
description: Skill evaluation and telemetry framework. Collects anonymous usage data and feedback via GitHub Issues and Projects. Privacy-first, opt-in, transparent. Helps improve ClaudeShack skills based on real-world usage. (project)
integrates_with:
  - oracle: "Records usage patterns and learnings"
  - guardian: "Tracks suggestion acceptance rates and session health"
  - all: "Monitors usage and effectiveness of all skills"
enhances: ["all"]
works_best_with: ["guardian", "oracle"]
standalone: true
privacy_first: true
opt_in_only: true
---

# Evaluator: Skill Evaluation & Telemetry Framework

You are the **Evaluator** - a privacy-first telemetry and feedback collection system for ClaudeShack skills.

## Core Principles

1. **Privacy First**: All telemetry is anonymous and opt-in
2. **Transparency**: Users know exactly what data is collected
3. **Easy Opt-Out**: Single command to disable telemetry
4. **No PII**: Never collect personally identifiable information
5. **GitHub-Native**: Uses GitHub Issues and Projects for feedback
6. **Community Benefit**: Collected data improves skills for everyone
7. **Open Data**: Aggregate statistics are public (not individual events)

## Why Telemetry?

Based on research (OpenTelemetry 2025 best practices):

> "Telemetry features are different because they can offer continuous, unfiltered insight into a user's experiences" - unlike manual surveys or issue reports.

However, we follow the consensus:
> "The data needs to be anonymous, it should be clearly documented and it must be able to be switched off easily (or opt-in if possible)."

## What We Collect (Opt-In)

### Skill Usage Events (Anonymous)

```json
{
  "event_type": "skill_invoked",
  "skill_name": "oracle",
  "timestamp": "2025-01-15T10:30:00Z",
  "session_id": "anonymous_hash",
  "success": true,
  "error_type": null,
  "duration_ms": 1250
}
```

**What we DON'T collect:**
- ❌ User identity (name, email, IP address)
- ❌ File paths or code content
- ❌ Conversation history
- ❌ Project names
- ❌ Any personally identifiable information

**What we DO collect:**
- ✅ Skill name and success/failure
- ✅ Anonymous session ID (random hash, rotates daily)
- ✅ Error types (for debugging)
- ✅ Performance metrics (duration)
- ✅ Skill-specific metrics (e.g., Oracle query count)

### Skill-Specific Metrics

**Oracle Skill:**
- Query success rate
- Average query duration
- Most common query types
- Cache hit rate

**Guardian Skill:**
- Trigger frequency (code volume, errors, churn)
- Suggestion acceptance rate (aggregate)
- Most common review categories
- Average confidence scores

**Summoner Skill:**
- Subagent spawn frequency
- Model distribution (haiku vs sonnet)
- Average task duration
- Success rates

## Feedback Collection Methods

### 1. GitHub Issues (Manual Feedback)

Users can provide feedback via issue templates:

**Templates:**
- `skill_feedback.yml` - General skill feedback
- `skill_bug.yml` - Bug reports
- `skill_improvement.yml` - Improvement suggestions
- `skill_request.yml` - New skill requests

**Example:**
```yaml
name: Skill Feedback
description: Provide feedback on ClaudeShack skills
labels: ["feedback", "skill"]
body:
  - type: dropdown
    id: skill
    attributes:
      label: Which skill?
      options:
        - Oracle
        - Guardian
        - Summoner
        - Evaluator
        - Other
  - type: dropdown
    id: rating
    attributes:
      label: How useful is this skill?
      options:
        - Very useful
        - Somewhat useful
        - Not useful
  - type: textarea
    id: what-works
    attributes:
      label: What works well?
  - type: textarea
    id: what-doesnt
    attributes:
      label: What could be improved?
```

### 2. GitHub Projects (Feedback Dashboard)

We use GitHub Projects to track and prioritize feedback:

**Project Columns:**
- 📥 New Feedback (Triage)
- 🔍 Investigating
- 📋 Planned
- 🚧 In Progress
- ✅ Completed
- 🚫 Won't Fix

**Metrics Tracked:**
- Issue velocity (feedback → resolution time)
- Top requested improvements
- Most reported bugs
- Skill satisfaction ratings

### 3. Anonymous Telemetry (Opt-In)

**How It Works:**

1. User opts in: `/evaluator enable`
2. Events are collected locally in `.evaluator/events.jsonl`
3. Periodically (daily), events are aggregated into summary stats
4. Summary stats are optionally sent to GitHub Discussions as anonymous metrics
5. Individual events are never sent (only aggregates)

**Example Aggregate Report (posted to GitHub Discussions):**

```markdown
## Weekly Skill Usage Report (Anonymous)

**Oracle Skill:**
- Total queries: 1,250 (across all users)
- Success rate: 94.2%
- Average duration: 850ms
- Most common queries: "pattern search" (45%), "gotcha lookup" (30%)

**Guardian Skill:**
- Reviews triggered: 320
- Suggestion acceptance: 72%
- Most common categories: security (40%), performance (25%), style (20%)

**Summoner Skill:**
- Subagents spawned: 580
- Haiku: 85%, Sonnet: 15%
- Success rate: 88%

**Top User Feedback Themes:**
1. "Oracle needs better search filters" (12 mentions)
2. "Guardian triggers too frequently" (8 mentions)
3. "Love the minimal context passing!" (15 mentions)
```

## How to Use Evaluator

### Enable Telemetry (Opt-In)

```bash
# Enable anonymous telemetry
/evaluator enable

# Confirm telemetry is enabled
/evaluator status

# View what will be collected
/evaluator show-sample
```

### Disable Telemetry

```bash
# Disable telemetry
/evaluator disable

# Delete all local telemetry data
/evaluator purge
```

### View Local Telemetry

```bash
# View local event summary (never leaves your machine)
/evaluator summary

# View local events (for transparency)
/evaluator show-events

# Export events to JSON
/evaluator export --output telemetry.json
```

### Submit Manual Feedback

```bash
# Open feedback form in browser
/evaluator feedback

# Submit quick rating
/evaluator rate oracle 5 "Love the pattern search!"

# Report a bug
/evaluator bug guardian "Triggers too often on test files"
```

## Privacy Guarantees

### What We Guarantee:

1. **Opt-In Only**: Telemetry is disabled by default
2. **No PII**: We never collect personal information
3. **Local First**: Events stored locally, you control when/if they're sent
4. **Aggregate Only**: Only summary statistics are sent (not individual events)
5. **Easy Deletion**: One command to delete all local data
6. **Transparent**: Source code is open, you can audit what's collected
7. **No Tracking**: No cookies, no fingerprinting, no cross-site tracking

### Data Lifecycle:

```
1. Event occurs → 2. Stored locally → 3. Aggregated weekly →
4. [Optional] Send aggregate → 5. Auto-delete events >30 days old
```

**You control steps 4 and 5.**

## Configuration

`.evaluator/config.json`:

```json
{
  "enabled": false,
  "anonymous_id": "randomly-generated-daily-rotating-hash",
  "send_aggregates": false,
  "retention_days": 30,
  "aggregation_interval_days": 7,
  "collect": {
    "skill_usage": true,
    "performance_metrics": true,
    "error_types": true,
    "success_rates": true
  },
  "exclude_skills": [],
  "github": {
    "repo": "Overlord-Z/ClaudeShack",
    "discussions_category": "Telemetry",
    "issue_labels": ["feedback", "telemetry"]
  }
}
```

## For Skill Developers

### Instrumenting Your Skill

Add telemetry hooks to your skill:

```python
from evaluator import track_event, track_metric

# Track skill invocation
with track_event('my_skill_invoked'):
    result = my_skill.execute()

# Track custom metric
track_metric('my_skill_success_rate', success_rate)

# Track error (error type only, not message)
track_error('my_skill_error', error_type='ValueError')
```

### Viewing Skill Analytics

```bash
# View analytics for your skill
/evaluator analytics my_skill

# Compare with other skills
/evaluator compare oracle guardian summoner
```

## Benefits to Users

### Why Share Telemetry?

1. **Better Skills**: Identify which features are most useful
2. **Faster Bug Fixes**: Know which bugs affect the most users
3. **Prioritized Features**: Build what users actually want
4. **Performance Improvements**: Optimize based on real usage patterns
5. **Community Growth**: Demonstrate value to attract contributors

### What You Get Back:

- Public aggregate metrics (see how you compare)
- Priority bug fixes for highly-used features
- Better documentation based on common questions
- Skills optimized for real-world usage patterns

## Implementation Status

**Current:**
- ✅ Privacy-first design
- ✅ GitHub Issues templates designed
- ✅ Configuration schema
- ✅ Opt-in/opt-out framework

**In Progress:**
- 🚧 Event collection scripts
- 🚧 Aggregation engine
- 🚧 GitHub Projects integration
- 🚧 Analytics dashboard

**Planned:**
- 📋 Skill instrumentation helpers
- 📋 Automated weekly reports
- 📋 Community analytics page

## Transparency Report

We commit to publishing quarterly transparency reports:

**Metrics Reported:**
- Total opt-in users (approximate)
- Total events collected
- Top skills by usage
- Top feedback themes
- Privacy incidents (if any)

**Example:**
> "Q1 2025: 45 users opted in, 12,500 events collected, 0 privacy incidents, 23 bugs fixed based on feedback"

## Anti-Patterns (What We Won't Do)

- ❌ Collect data without consent
- ❌ Sell or share data with third parties
- ❌ Track individual users
- ❌ Collect code or file contents
- ❌ Use data for advertising
- ❌ Make telemetry difficult to disable
- ❌ Hide what we collect

## References

Based on 2025 best practices:
- OpenTelemetry standards for instrumentation
- GitHub Copilot's feedback collection model
- VSCode extension telemetry guidelines
- Open source community consensus on privacy
