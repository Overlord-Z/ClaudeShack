# Mission Control: [TASK NAME]

**Created**: [DATE]
**Status**: [Planning | In Progress | Integration | Complete]
**Summoner**: [Agent/User Name]

---

## Executive Summary

[Provide a concise 1-2 paragraph overview of the entire initiative. Include:
- What is being built/changed
- Why it's important
- High-level approach
- Expected impact]

---

## Success Criteria

Define what "done" looks like:

- [ ] **Criterion 1**: [Specific, measurable success indicator]
- [ ] **Criterion 2**: [Specific, measurable success indicator]
- [ ] **Criterion 3**: [Specific, measurable success indicator]
- [ ] **All tests passing**: Unit, integration, and e2e tests pass
- [ ] **Documentation complete**: All changes documented
- [ ] **Quality gates passed**: DRY, CLEAN, SOLID principles followed

---

## Context & Constraints

### Technical Context

**Current Architecture:**
[Brief description of relevant architecture, tech stack, patterns in use]

**Relevant Existing Implementations:**
- `path/to/file.ts:123` - [What this does and why it's relevant]
- `path/to/other/file.ts:456` - [What this does and why it's relevant]

**Technology Stack:**
- [Framework/Library 1]
- [Framework/Library 2]
- [Database/Store]
- [Other relevant tech]

### Business Context

**User Impact:**
[How this affects end users]

**Priority:**
[High/Medium/Low and why]

**Stakeholders:**
[Who cares about this and why]

### Constraints

**Performance:**
- [Specific performance requirements]

**Compatibility:**
- [Browser support, API versions, etc.]

**Security:**
- [Security considerations and requirements]

**Timeline:**
- [Any time constraints]

**Other:**
- [Any other constraints or limitations]

---

## Task Index

### Phase 1: [PHASE NAME - e.g., "Foundation & Setup"]

#### Task 1.1: [Specific Task Name]

**Agent Type**: [e.g., Backend Engineer, Frontend Specialist, DevOps]

**Responsibility**:
[Clear, bounded description of what this agent is responsible for. Use active voice.]

**Context Needed**:
```
[ONLY the specific context this agent needs. Reference sections above or external docs.
DO NOT duplicate large amounts of text - point to it instead.]
```

**Inputs**:
- [What must exist before this task can start]
- [Files, data, decisions, or outputs from other tasks]

**Outputs**:
- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] [Tests for this component]

**Validation Criteria**:
```
How to verify this task is complete and correct:
- [ ] Validation point 1
- [ ] Validation point 2
- [ ] Tests pass
- [ ] Code review checklist items
```

**Dependencies**:
- None (for first task) OR
- Requires: Task X.Y to be complete
- Blocked by: [What's blocking this if anything]

**Estimated Complexity**: [Low/Medium/High]

---

#### Task 1.2: [Next Task Name]

[Repeat structure above]

---

### Phase 2: [NEXT PHASE NAME]

[Continue with tasks for next phase]

---

## Quality Gates

### Code Quality Standards

- [ ] **DRY (Don't Repeat Yourself)**
  - No duplicated logic or code blocks
  - Shared functionality extracted into reusable utilities
  - Configuration centralized

- [ ] **CLEAN Code**
  - Meaningful variable and function names
  - Functions do one thing well
  - Comments explain WHY, not WHAT
  - Consistent formatting and style

- [ ] **SOLID Principles**
  - Single Responsibility: Each module/class has one reason to change
  - Open/Closed: Open for extension, closed for modification
  - Liskov Substitution: Subtypes are substitutable for base types
  - Interface Segregation: No client forced to depend on unused methods
  - Dependency Inversion: Depend on abstractions, not concretions

- [ ] **Security**
  - No injection vulnerabilities (SQL, XSS, Command, etc.)
  - Proper authentication and authorization
  - Sensitive data properly handled
  - Dependencies checked for vulnerabilities

- [ ] **Performance**
  - Meets stated performance requirements
  - No unnecessary computations or renders
  - Efficient algorithms and data structures
  - Proper resource cleanup

### Process Quality Standards

- [ ] **Testing**
  - Unit tests for all new functions/components
  - Integration tests for component interactions
  - E2E tests for critical user paths
  - Edge cases covered
  - All tests passing

- [ ] **Documentation**
  - Public APIs documented
  - Complex logic explained
  - README updated if needed
  - Migration guide if breaking changes

- [ ] **Integration**
  - No breaking changes (or explicitly documented with migration path)
  - Backwards compatible where possible
  - All integrations tested
  - Dependencies updated

- [ ] **Code Review**
  - Self-review completed
  - Peer review if applicable
  - All review comments addressed

---

## Agent Roster

### [Agent Role/Name 1]

**Specialization**: [What domain expertise this agent brings]

**Assigned Tasks**:
- Task 1.1
- Task 2.3

**Context Provided**:
- Section: [Reference to MCD sections this agent needs]
- Files: [Key files this agent will work with]
- External Docs: [Any external documentation needed]

**Communication Protocol**:
- Reports to: [Who/what]
- Updates: [When and how to provide status updates]
- Blockers: [How to escalate blockers]

---

### [Agent Role/Name 2]

[Repeat structure above]

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk description] | Low/Med/High | Low/Med/High | [How we're mitigating this] |
| [Risk description] | Low/Med/High | Low/Med/High | [How we're mitigating this] |

---

## Progress Tracking

### Phase 1: [PHASE NAME]
- [x] Task 1.1: [Name] - ✅ Complete
- [ ] Task 1.2: [Name] - 🔄 In Progress
- [ ] Task 1.3: [Name] - ⏸️ Blocked by X
- [ ] Task 1.4: [Name] - ⏳ Pending

### Phase 2: [PHASE NAME]
- [ ] Task 2.1: [Name] - ⏳ Pending

---

## Decision Log

| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| [DATE] | [What was decided] | [Why this decision] | [What this affects] |

---

## Integration Checklist

Final integration before marking complete:

- [ ] All tasks completed and validated
- [ ] All tests passing (unit, integration, e2e)
- [ ] No breaking changes or migration guide provided
- [ ] Performance benchmarks met
- [ ] Security review passed
- [ ] Documentation complete
- [ ] Quality gates all green
- [ ] Stakeholder acceptance (if applicable)

---

## Lessons Learned

[To be filled at completion - what went well, what could improve for next time]

---

## References

- [Link to relevant docs]
- [Link to design docs]
- [Link to related issues/PRs]
