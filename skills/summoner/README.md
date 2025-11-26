# Summoner Skill

**Multi-Agent Orchestration for Complex Tasks**

The Summoner skill transforms Claude Code into a sophisticated project orchestrator, breaking down complex tasks into manageable units and coordinating specialized agents to deliver high-quality, production-ready code.

## What is the Summoner?

The Summoner is a meta-skill that excels at:

- **Task Decomposition**: Breaking complex requirements into atomic, well-defined tasks
- **Context Management**: Preserving all necessary context while avoiding bloat
- **Agent Orchestration**: Summoning and coordinating specialized agents
- **Quality Assurance**: Ensuring DRY, CLEAN, SOLID principles throughout
- **Risk Mitigation**: Preventing assumptions, scope creep, and breaking changes

## When to Use

### ✅ Use Summoner For:

- **Multi-component features** (3+ files/components)
- **Large refactoring projects** (architectural changes)
- **Migration projects** (API versions, frameworks, databases)
- **Complex bug fixes** (multiple related issues)
- **New system implementations** (auth, payments, etc.)

### ❌ Don't Use Summoner For:

- Single file changes
- Simple bug fixes
- Straightforward feature additions
- Routine maintenance
- Quick patches

## How It Works

```
1. Task Analysis
   ↓
2. Create Mission Control Document (MCD)
   ↓
3. Decompose into Phases & Tasks
   ↓
4. For Each Task:
   - Summon Specialized Agent
   - Provide Bounded Context
   - Monitor & Validate
   ↓
5. Integration & Quality Control
   ↓
6. Deliver Production-Ready Code
```

## Quick Start

### 1. Activate the Skill

Simply request it in Claude Code:

```
Use the summoner skill to implement user authentication with OAuth2
```

### 2. Or Explicitly Reference

```
I need to refactor our API layer to use GraphQL. This is a complex task that
will touch multiple services. Can you use the Summoner skill to orchestrate this?
```

## Components

### 📄 Templates

- **`mission-control-template.md`**: Master planning document
- **`agent-spec-template.md`**: Agent assignment specifications
- **`quality-gates.md`**: Comprehensive quality checklist

### 🔧 Scripts

- **`init_mission.py`**: Initialize new Mission Control Documents
- **`validate_quality.py`**: Interactive quality gate validation

### 📚 References

All templates and quality standards are in the `References/` directory.

## Directory Structure

```
summoner/
├── SKILL.md                    # Main skill definition
├── README.md                   # This file
├── scripts/
│   ├── init_mission.py        # MCD initializer
│   └── validate_quality.py    # Quality validator
├── References/
│   ├── mission-control-template.md
│   ├── agent-spec-template.md
│   └── quality-gates.md
└── Assets/
    └── (reserved for future templates)
```

## Example Workflow

### Scenario: Implement Real-Time Notifications

1. **Activate Summoner**
   ```
   Use the summoner skill to add real-time notifications to our app
   using WebSockets. This needs to work across web and mobile clients.
   ```

2. **Summoner Creates MCD**
   - Analyzes requirements
   - Creates `mission-real-time-notifications.md`
   - Breaks down into phases and tasks

3. **Phase 1: Backend Infrastructure**
   - Task 1.1: WebSocket server setup (Backend Agent)
   - Task 1.2: Message queue integration (Backend Agent)
   - Task 1.3: Authentication middleware (Security Agent)

4. **Phase 2: Client Integration**
   - Task 2.1: Web client WebSocket handler (Frontend Agent)
   - Task 2.2: Mobile client integration (Mobile Agent)
   - Task 2.3: Reconnection logic (Frontend/Mobile Agents)

5. **Phase 3: Testing & Polish**
   - Task 3.1: Integration tests (QA Agent)
   - Task 3.2: Load testing (Performance Agent)
   - Task 3.3: Documentation (Documentation Agent)

6. **Quality Control**
   - Validate all quality gates
   - Integration testing
   - Final review

## Key Features

### 🎯 Context Preservation

Every task in the MCD includes:
- Exact context needed (no more, no less)
- Clear inputs and outputs
- Explicit dependencies
- Validation criteria

### 🛡️ Quality Enforcement

Three levels of quality gates:
- **Task-level**: DRY, testing, documentation
- **Phase-level**: Integration, CLEAN, performance, security
- **Project-level**: SOLID, architecture, production readiness

### 📊 Progress Tracking

Mission Control Document provides:
- Real-time progress updates
- Risk register
- Decision log
- Integration checklist

### 🚫 Zero Slop Policy

The Summoner prevents:
- Assumption-driven development
- Context bloat
- Scope creep
- Breaking changes without migration paths
- Code duplication
- Untested code

## Using the Scripts

### Initialize a Mission

```bash
python .claude/skills/summoner/scripts/init_mission.py "Add User Authentication"
```

Creates `mission-add-user-authentication.md` ready for editing.

### Validate Quality

```bash
# Interactive validation
python .claude/skills/summoner/scripts/validate_quality.py --level task --interactive

# Print checklist for manual review
python .claude/skills/summoner/scripts/validate_quality.py --level project
```

## Quality Standards

### DRY (Don't Repeat Yourself)
- No code duplication
- Shared logic extracted
- Single source of truth for data

### CLEAN Code
- **C**lear: Easy to understand
- **L**imited: Single responsibility
- **E**xpressive: Intent-revealing names
- **A**bstracted: Proper abstraction levels
- **N**eat: Well-organized structure

### SOLID Principles
- **S**ingle Responsibility
- **O**pen/Closed
- **L**iskov Substitution
- **I**nterface Segregation
- **D**ependency Inversion

See `References/quality-gates.md` for complete checklists.

## Best Practices

### 1. Front-Load Planning

Spend time on the MCD before coding. A well-planned mission executes smoothly.

### 2. Bounded Context

Give each agent exactly what they need. Too much context is as bad as too little.

### 3. Validate Early, Validate Often

Run quality gates at task completion, not just at the end.

### 4. Document Decisions

Use the Decision Log in the MCD to record why choices were made.

### 5. Update the MCD

Keep the MCD current as the project evolves. It's a living document.

## Troubleshooting

### Agent Asking for Already-Provided Context

**Problem**: Agent requests information that's in the MCD.

**Solution**: The agent spec wasn't clear enough. Update the agent spec template to explicitly reference the MCD sections.

### Quality Gates Failing

**Problem**: Code doesn't pass quality checks.

**Solution**:
1. Identify which gate failed
2. Create a remediation task
3. Assign to appropriate agent
4. Revalidate after fix

### Scope Creep

**Problem**: Tasks growing beyond original boundaries.

**Solution**:
1. Pause execution
2. Review MCD success criteria
3. Either add new tasks or trim scope
4. Update MCD and proceed

### Integration Issues

**Problem**: Components don't work together.

**Solution**:
1. Review interface definitions in MCD
2. Check if agents followed specs
3. Add integration tests
4. Document the interface contract better

## Examples

See the `examples/` directory in the main ClaudeShack repo for:
- Complete Mission Control Documents
- Real-world orchestration scenarios
- Quality gate validation reports

## Contributing

Ideas for improving the Summoner skill?
- Suggest new templates
- Propose quality gates
- Share success stories
- Report issues

## Version History

- **v1.0** (2025-11-19): Initial release
  - Mission Control Document system
  - Quality gates framework
  - Agent orchestration workflows
  - Supporting scripts and templates

## License

Part of the ClaudeShack skill collection. See main repository for licensing.

---

**"Context is precious. Orchestration is power. Quality is non-negotiable."**
