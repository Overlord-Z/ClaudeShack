# Guardian Scripts

This directory contains the implementation scripts for the Guardian skill.

## Core Scripts

### guardian.py
**Main orchestrator** - Coordinates all Guardian components.

Usage:
```bash
# Review code
python guardian.py review --file auth.py --focus security

# Plan complex task
python guardian.py plan --task "Build REST API"

# Debug error
python guardian.py debug --file app.py --error "TypeError: cannot unpack"

# Check triggers
python guardian.py check

# Session status
python guardian.py status
```

### monitor_session.py
**Session health monitor** - Tracks metrics and detects when intervention is needed.

Key Features:
- Tracks code volume, errors, file edits, corrections
- Detects threshold crossings
- Calculates session health scores
- Minimal storage (only metrics, not full conversation)

Usage:
```bash
# Track events
python monitor_session.py --event code-written --file auth.py --lines 60
python monitor_session.py --event error --message "TypeError: ..."
python monitor_session.py --event file-edit --file app.py
python monitor_session.py --event correction --message "that's wrong..."

# Check health
python monitor_session.py --check-health
python monitor_session.py --check-triggers

# Initialize/reset
python monitor_session.py --init
python monitor_session.py --reset
```

### context_filter.py
**Minimal context extractor** - Extracts only what's needed for subagent tasks.

Key Principle: "Caller should only pass exactly what is needed for the task so it can be laser focused"

Features:
- Loads only relevant files
- Extracts relevant Oracle patterns (max 5)
- Finds recent corrections (max 3)
- NO full conversation passing

Usage:
```bash
# Extract context for review
python context_filter.py --task review --file auth.py --focus security

# Extract context for planning
python context_filter.py --task plan --description "Build REST API"

# Extract context for debugging
python context_filter.py --task debug --file app.py --error "TypeError: ..."

# Output as JSON
python context_filter.py --task review --file auth.py --format json
```

### validator.py
**Suggestion validator** - Cross-checks subagent suggestions against Oracle knowledge.

Key Principle: "Subagent might be missing important codebase context - need validation layer"

Features:
- Validates against Oracle patterns
- Detects contradictions with known practices
- Checks rejection history
- Calculates confidence scores
- Learns from acceptance rates

Usage:
```bash
# Validate single suggestion
python validator.py --suggestion "Use MD5 for passwords" --category security

# Validate from file
python validator.py --suggestions-file suggestions.json

# Record rejection
python validator.py --record-rejection "Add rate limiting" --rejection-reason "We handle at nginx level" --category performance

# Update stats
python validator.py --update-stats accept --category security
python validator.py --update-stats reject --category style

# Check rejection history
python validator.py --check-rejection "Use rate limiting"
```

### learning.py
**Learning system** - Adjusts thresholds based on user feedback.

Features:
- Tracks acceptance/rejection rates
- Adjusts thresholds to maintain target acceptance rate
- Learns anti-patterns from rejections
- Updates auto-review rules dynamically

Usage:
```bash
# Apply adjustments
python learning.py --adjust

# Show recommendations (dry run)
python learning.py --recommend

# View statistics
python learning.py --stats

# Configure
python learning.py --set-target 0.75
python learning.py --set-speed 0.1
```

## Architecture

```
guardian.py (orchestrator)
    |
    +-- monitor_session.py (check triggers & health)
    |
    +-- context_filter.py (extract minimal context)
    |
    +-- [Task tool with Haiku agent] (perform review/planning)
    |
    +-- validator.py (validate suggestions)
    |
    +-- [Present to user with confidence scores]
    |
    +-- learning.py (adjust based on feedback)
```

## Data Storage

Guardian stores minimal data in `.guardian/`:

```
.guardian/
├── config.json              # Configuration and thresholds
├── session_state.json       # Current session metrics (NOT full conversation)
├── rejection_history.json   # Recently rejected suggestions
└── acceptance_stats.json    # Acceptance rate statistics
```

## Key Design Principles

1. **Minimal Context Passing** - Never pass full conversations to subagents
2. **Suggestion Mode** - Present findings as suggestions, not commands
3. **Oracle Validation** - Cross-check all suggestions against known patterns
4. **Learning from Feedback** - Adjust sensitivity based on user acceptance
5. **Haiku Only** - All subagents use haiku model (fast & cheap)
6. **User Authority** - User has final say on all suggestions

## Integration with Oracle

Guardian automatically:
- Loads relevant Oracle patterns before review
- Validates suggestions against Oracle knowledge
- Records validated suggestions in Oracle
- Stores rejection reasons as anti-patterns in Oracle

## Example Workflow

1. **User writes 60 lines of auth code**
2. **monitor_session.py** detects threshold crossed
3. **guardian.py** extracts minimal context via **context_filter.py**
4. **Guardian spawns Haiku agent** with only: auth.py + security patterns
5. **Haiku agent** returns suggestions
6. **validator.py** checks suggestions against Oracle
7. **Guardian presents** filtered suggestions with confidence scores
8. **User accepts/rejects**
9. **learning.py** adjusts thresholds based on feedback

## Testing

```bash
# Initialize Guardian
cd /path/to/your/project
python guardian.py --init

# Simulate code writing
python monitor_session.py --event code-written --file test.py --lines 60

# Check if should trigger
python monitor_session.py --check-triggers

# Perform review
python guardian.py review --file test.py --focus security

# View session health
python guardian.py status

# View learning stats
python learning.py --stats
```

## Future Enhancements

- Integration with Claude Code Task tool for spawning Haiku agents
- Real-time monitoring via background process
- Web dashboard for session health visualization
- Team-wide learning (shared Guardian config via git)
- Integration with CI/CD pipelines
