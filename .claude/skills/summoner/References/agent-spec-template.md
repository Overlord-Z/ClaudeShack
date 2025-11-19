# Agent Specification Template

Use this template when summoning specialized agents to ensure they have exactly what they need - no more, no less.

---

## Agent Specification: [AGENT NAME/ID]

**Created**: [DATE]
**Summoner**: [Who summoned this agent]
**Status**: [Active | Complete | Blocked]

---

## Agent Profile

### Specialization
[What this agent is expert in - e.g., "Frontend React Developer", "Database Optimization Specialist", "Security Auditor"]

### Assigned Tasks
- Task 1.2: [Task Name]
- Task 1.3: [Task Name]
- [List all tasks assigned to this agent]

### Expected Completion
[Date/time or "After Task X.Y completes"]

---

## Context Package

### What This Agent Needs to Know

[Provide ONLY the context necessary for their tasks. Link to full docs rather than duplicating.]

**Project Overview (Brief)**:
[2-3 sentences about the overall project - just enough to understand their role]

**Their Role**:
[1-2 sentences about what they're responsible for in the bigger picture]

**Specific Context**:
```
[The actual detailed context needed for their tasks:
- Relevant architecture decisions
- Tech stack specifics
- Existing patterns to follow
- Constraints to respect
- Examples to reference]
```

### What This Agent Does NOT Need

[Explicitly list what context you're NOT providing to avoid bloat:]
- ❌ [Irrelevant context 1]
- ❌ [Irrelevant context 2]
- ❌ [Information they can look up themselves]

---

## Task Details

### Task [ID]: [Name]

**Objective**:
[Clear statement of what needs to be accomplished]

**Current State**:
```
[What exists now - relevant files, implementations, issues]
File: path/to/file.ts:123
Current implementation: [brief description]
Problem: [what needs to change]
```

**Desired End State**:
```
[What should exist after this task]
- Deliverable 1
- Deliverable 2
- Tests passing
- Documentation updated
```

**Acceptance Criteria**:
- [ ] Criterion 1 (specific, testable)
- [ ] Criterion 2 (specific, testable)
- [ ] All tests pass
- [ ] Quality gates pass
- [ ] Documentation complete

**Constraints**:
- Must: [Things that must be done]
- Must NOT: [Things to avoid]
- Should: [Preferences/best practices]

**Reference Files**:
- `path/to/relevant/file.ts` - [Why this is relevant]
- `path/to/example.ts:45-67` - [What pattern to follow]
- `docs/architecture.md` - [Link to full docs]

---

## Inputs & Dependencies

### Inputs Provided
[What this agent is receiving to start their work:]
- ✅ Input 1: [Description and location]
- ✅ Input 2: [Description and location]

### Dependencies
[What must be complete before this agent can start:]
- Task X.Y: [Name] - Status: [Complete/In Progress]
- Decision Z: [Description] - Status: [Decided/Pending]

### Blockers
[Current blockers if any:]
- ❌ [Blocker description] - Owner: [Who's resolving]
- OR: None - Ready to proceed

---

## Outputs Expected

### Primary Deliverables
1. **[Deliverable 1]**
   - Format: [e.g., "Modified file at path/to/file.ts"]
   - Requirements: [Specific requirements]
   - Validation: [How to verify it's correct]

2. **[Deliverable 2]**
   - Format: [...]
   - Requirements: [...]
   - Validation: [...]

### Secondary Deliverables
- [ ] Tests for new functionality
- [ ] Documentation updates
- [ ] Updated MCD if any changes to plan
- [ ] Quality gate sign-off

### Handoff Protocol
[How to hand off to next agent or back to summoner:]
```
1. Complete all deliverables
2. Run quality gate checklist
3. Document any deviations from plan
4. Update MCD progress tracking
5. Report completion with summary
```

---

## Quality Standards

### Code Quality
- [ ] Follows DRY principle
- [ ] Follows CLEAN code practices
- [ ] Follows SOLID principles (applicable ones)
- [ ] Consistent with project style
- [ ] Properly documented

### Testing
- [ ] Unit tests written
- [ ] Integration tests if applicable
- [ ] All tests passing
- [ ] Edge cases covered

### Security
- [ ] No vulnerabilities introduced
- [ ] Input validation
- [ ] Proper error handling
- [ ] No sensitive data exposed

### Performance
- [ ] Meets performance requirements
- [ ] No unnecessary operations
- [ ] Efficient algorithms
- [ ] Resources properly managed

---

## Communication Protocol

### Status Updates
**Frequency**: [e.g., "After each task completion" or "Daily"]
**Format**: [How to report - e.g., "Comment in MCD"]
**Content**: [What to include - progress, blockers, questions]

### Questions/Clarifications
**How to Ask**: [Process for getting clarifications]
**Response SLA**: [When to expect answers]
**Escalation**: [When and how to escalate]

### Completion Report
When done, provide:
```markdown
## Completion Report: [Agent Name]

### Summary
[1-2 sentences on what was accomplished]

### Deliverables
- ✅ Deliverable 1: [Location/description]
- ✅ Deliverable 2: [Location/description]

### Quality Gates
- ✅ Code Quality: PASS
- ✅ Testing: PASS
- ✅ Documentation: PASS

### Deviations from Plan
- [None] OR
- [Deviation 1 - why it happened - impact]

### Blockers Encountered
- [None] OR
- [Blocker 1 - how it was resolved]

### Recommendations
[Any suggestions for next phases or improvements]

### Next Steps
[What should happen next]
```

---

## Tools & Resources

### Tools Available
- [Tool/Framework 1]: [Purpose]
- [Tool/Framework 2]: [Purpose]
- [Testing framework]: [How to run tests]
- [Linter]: [How to check style]

### Reference Documentation
- [Link to tech docs]
- [Link to internal docs]
- [Link to examples]
- [Link to style guide]

### Example Code
[Paste or link to example code that shows the pattern to follow]
```typescript
// Example of preferred pattern
function examplePattern() {
  // This is how we do things in this project
}
```

---

## Emergency Contacts

**Summoner**: [How to reach the summoner]
**Technical Lead**: [If different from summoner]
**Domain Expert**: [For domain-specific questions]
**Blocker Resolution**: [Who to contact if blocked]

---

## Success Indicators

✅ **This agent is succeeding if:**
- Delivering on time
- No out-of-scope work
- Quality gates passing
- No blockers or blockers being resolved quickly
- Clear communication

❌ **Warning signs:**
- Asking for context that was already provided
- Scope creep
- Quality gate failures
- Long periods of silence
- Assumptions not validated

---

## Agent Activation

**Summoning Command**:
```
Using the Task tool with subagent_type="general-purpose":

"You are a [SPECIALIZATION] agent. Your mission is to [OBJECTIVE].

Context: [PROVIDE CONTEXT PACKAGE]

Your tasks:
[LIST TASKS WITH DETAILS]

Deliverables expected:
[LIST DELIVERABLES]

Quality standards:
[REFERENCE QUALITY GATES]

Report back when complete with a completion report."
```

**Estimated Duration**: [Time estimate]
**Complexity**: [Low/Medium/High]
**Priority**: [P0/P1/P2/P3]

---

## Notes

[Any additional notes, special considerations, or context that doesn't fit elsewhere]

---

**Template Version**: 1.0
**Last Updated**: [Date]
