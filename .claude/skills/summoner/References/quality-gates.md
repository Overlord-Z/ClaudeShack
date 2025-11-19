# Quality Gates Checklist

This document provides detailed quality gates for validating work at task, phase, and project levels.

---

## Task-Level Quality Gates

Run these checks after completing each individual task:

### ✅ Functional Requirements
- [ ] All specified outputs delivered
- [ ] Functionality works as described
- [ ] Edge cases handled
- [ ] Error cases handled gracefully
- [ ] No regression in existing functionality

### ✅ Code Quality
- [ ] Code is readable and self-documenting
- [ ] Variable/function names are meaningful
- [ ] No magic numbers or strings
- [ ] No commented-out code (unless explicitly documented why)
- [ ] Consistent code style with project

### ✅ DRY (Don't Repeat Yourself)
- [ ] No duplicated logic
- [ ] Shared functionality extracted to utilities
- [ ] Constants defined once, referenced everywhere
- [ ] No copy-paste code blocks

### ✅ Testing
- [ ] Unit tests written for new code
- [ ] Tests cover happy path
- [ ] Tests cover edge cases
- [ ] Tests cover error conditions
- [ ] All tests pass
- [ ] Test names clearly describe what they test

### ✅ Documentation
- [ ] Complex logic has explanatory comments
- [ ] Public APIs documented (JSDoc, docstrings, etc.)
- [ ] README updated if user-facing changes
- [ ] Breaking changes documented

---

## Phase-Level Quality Gates

Run these checks after completing a phase (group of related tasks):

### ✅ Integration
- [ ] All components integrate correctly
- [ ] Data flows between components as expected
- [ ] No integration bugs
- [ ] APIs between components are clean
- [ ] Interfaces are well-defined

### ✅ CLEAN Principles
- [ ] **C**lear: Code is easy to understand
- [ ] **L**imited: Functions/methods have single responsibility
- [ ] **E**xpressive: Naming reveals intent
- [ ] **A**bstracted: Proper level of abstraction
- [ ] **N**eat: Organized, well-structured code

### ✅ Performance
- [ ] No obvious performance issues
- [ ] Efficient algorithms used
- [ ] No unnecessary computations
- [ ] Resources properly managed (memory, connections, etc.)
- [ ] Meets stated performance requirements

### ✅ Security
- [ ] No injection vulnerabilities (SQL, XSS, Command, etc.)
- [ ] Input validation in place
- [ ] Output encoding where needed
- [ ] Authentication/authorization checked
- [ ] Sensitive data not logged or exposed
- [ ] Dependencies have no known vulnerabilities

---

## Project-Level Quality Gates

Run these checks before marking the entire project complete:

### ✅ SOLID Principles

#### Single Responsibility Principle
- [ ] Each class/module has one reason to change
- [ ] Each function does one thing well
- [ ] No god objects or god functions
- [ ] Responsibilities clearly separated

#### Open/Closed Principle
- [ ] Open for extension (can add new behavior)
- [ ] Closed for modification (don't change existing code)
- [ ] Use abstractions (interfaces, base classes) for extension points
- [ ] Configuration over hardcoding

#### Liskov Substitution Principle
- [ ] Subtypes can replace base types without breaking
- [ ] Derived classes don't weaken preconditions
- [ ] Derived classes don't strengthen postconditions
- [ ] Inheritance is "is-a" relationship, not "has-a"

#### Interface Segregation Principle
- [ ] Interfaces are focused and cohesive
- [ ] No client forced to depend on methods it doesn't use
- [ ] Many small interfaces > one large interface
- [ ] Clients see only methods they need

#### Dependency Inversion Principle
- [ ] High-level modules don't depend on low-level modules
- [ ] Both depend on abstractions
- [ ] Abstractions don't depend on details
- [ ] Details depend on abstractions
- [ ] Dependencies injected, not hardcoded

### ✅ Architecture Quality
- [ ] Architecture supports future growth
- [ ] Clear separation of concerns
- [ ] Proper layering (presentation, business logic, data)
- [ ] No architectural violations
- [ ] Design patterns used appropriately

### ✅ Testing Coverage
- [ ] Unit test coverage meets threshold (e.g., 80%)
- [ ] Integration tests for key workflows
- [ ] E2E tests for critical user paths
- [ ] All tests passing consistently
- [ ] No flaky tests

### ✅ Documentation Completeness
- [ ] README is current and accurate
- [ ] API documentation complete
- [ ] Architecture documented
- [ ] Setup/installation instructions clear
- [ ] Troubleshooting guide if applicable
- [ ] Inline documentation for complex code

### ✅ Production Readiness
- [ ] No breaking changes (or migration guide provided)
- [ ] Error handling comprehensive
- [ ] Logging appropriate (not too much, not too little)
- [ ] Monitoring/observability in place
- [ ] Configuration externalized
- [ ] Secrets/credentials properly managed

### ✅ User Impact
- [ ] User-facing features work as expected
- [ ] UX is intuitive
- [ ] Error messages are helpful
- [ ] Performance is acceptable to users
- [ ] Accessibility considerations addressed (if applicable)

---

## Quality Gate Severity Levels

When a quality gate fails, assess severity:

### 🔴 Critical (MUST FIX)
- Security vulnerabilities
- Data loss or corruption
- Breaking changes without migration path
- Production crashes or errors
- Major performance degradation

### 🟡 Warning (SHOULD FIX)
- SOLID principle violations
- Missing tests for complex logic
- Poor performance (but not critical)
- Missing documentation
- Code duplication

### 🟢 Info (NICE TO FIX)
- Minor style inconsistencies
- Optimization opportunities
- Refactoring suggestions
- Documentation enhancements

---

## Remediation Process

When quality gates fail:

1. **Document the Issue**
   - What gate failed
   - Severity level
   - Impact assessment

2. **Create Remediation Task**
   - Add to task index
   - Assign to appropriate agent
   - Provide context and acceptance criteria

3. **Revalidate**
   - After fix, re-run quality gate
   - Ensure no new issues introduced
   - Update MCD with results

4. **Learn**
   - Why did this get through?
   - How to prevent in future?
   - Update checklist if needed

---

## Automated Checks

Where possible, automate quality gates:

### Recommended Tools

**Linting:**
- ESLint (JavaScript/TypeScript)
- Pylint/Flake8 (Python)
- RuboCop (Ruby)
- Clippy (Rust)

**Testing:**
- Jest, Vitest (JavaScript)
- pytest (Python)
- RSpec (Ruby)
- cargo test (Rust)

**Security:**
- npm audit, yarn audit
- Snyk
- OWASP Dependency-Check
- Trivy

**Coverage:**
- Istanbul/nyc (JavaScript)
- Coverage.py (Python)
- SimpleCov (Ruby)
- Tarpaulin (Rust)

**Type Checking:**
- TypeScript
- mypy (Python)
- Sorbet (Ruby)

---

## Sign-Off Template

```markdown
## Quality Gate Sign-Off

**Task/Phase/Project**: [Name]
**Date**: [Date]
**Reviewed By**: [Agent/Person]

### Results
- ✅ Functional Requirements: PASS
- ✅ Code Quality: PASS
- ✅ DRY: PASS
- ✅ Testing: PASS
- ✅ Documentation: PASS
- ✅ SOLID Principles: PASS
- ✅ Security: PASS
- ✅ Performance: PASS

### Issues Found
- [None] OR
- [Issue 1 - Severity - Status]
- [Issue 2 - Severity - Status]

### Recommendation
- [ ] Approved - Ready to proceed
- [ ] Approved with conditions - [List conditions]
- [ ] Rejected - [List blockers]

### Notes
[Any additional notes or observations]
```

---

**Remember: Quality is not negotiable. It's faster to build it right than to fix it later.**
