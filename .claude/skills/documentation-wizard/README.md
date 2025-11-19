# Documentation Wizard

**Living Documentation Expert - Always in Sync**

Documentation Wizard keeps your documentation perfectly synchronized with code, decisions, and learnings. It integrates with Oracle, Summoner, and Style Master to create comprehensive, up-to-date documentation automatically.

## What It Does

### 📝 Auto-Generate Documentation
- README files from code + Oracle knowledge
- API documentation from code comments
- Architecture Decision Records (ADRs) from decisions
- Onboarding guides from Oracle sessions
- Changelogs from git history + Oracle

### 🔄 Continuous Synchronization
- Detects code changes and updates docs
- Pulls patterns from Oracle knowledge
- Extracts decisions from Summoner MCDs
- Syncs Style Master style guides
- Validates examples still work

### ✅ Documentation Validation
- Detects stale documentation
- Finds broken links
- Validates code examples
- Identifies missing documentation
- Checks for inconsistencies

### 🔗 Integration Powerhouse
- **Oracle**: Leverage learnings and decisions
- **Summoner**: Extract design docs from MCDs
- **Style Master**: Sync style guide documentation
- **Git**: Track evolution and changes

## Quick Start

```bash
# Generate initial documentation
python .claude/skills/documentation-wizard/Scripts/generate_docs.py

# Validate documentation
python .claude/skills/documentation-wizard/Scripts/validate_docs.py

# Sync from Oracle knowledge
python .claude/skills/documentation-wizard/Scripts/sync_docs.py --source oracle

# Generate changelog
python .claude/skills/documentation-wizard/Scripts/generate_changelog.py
```

## Use Cases

### 1. Initial Documentation Setup
```
Use the documentation wizard to set up documentation for our project.

[Analyzes codebase]
[Loads Oracle knowledge]
[Generates README, API docs, contributing guide]
[Creates documentation structure]
```

### 2. Keep Docs in Sync
```
Update documentation based on recent changes.

[Checks git diff]
[Identifies affected docs]
[Updates API documentation]
[Generates changelog entry]
```

### 3. Create ADRs from Decisions
```
Create ADR for our decision to use PostgreSQL over MongoDB.

[Loads Oracle decision entry]
[Reads Summoner MCD rationale]
[Generates ADR-015-database-choice.md]
[Links to Oracle and Summoner references]
```

## Documentation Types

### Generated Documentation

| Type | Source | Output |
|------|--------|--------|
| **README** | Code + Oracle + Summoner | README.md |
| **API Docs** | JSDoc/TypeDoc comments | docs/api/ |
| **ADRs** | Oracle decisions + Summoner MCDs | docs/adr/ |
| **Style Guide** | Style Master | docs/STYLEGUIDE.md |
| **Onboarding** | Oracle sessions | docs/ONBOARDING.md |
| **Changelog** | Git + Oracle | CHANGELOG.md |

## Integration Examples

### With Oracle 🧠

**Oracle knows**: "Use factory pattern for DB connections"

**Docs generated**:
```markdown
## Database Connections

All database connections use the factory pattern:
\`\`\`typescript
const db = DatabaseFactory.create('postgres');
\`\`\`
This ensures proper connection pooling. See Oracle entry #42.
```

### With Summoner 🧙

**Summoner MCD**: Microservices migration decision

**ADR generated**:
```markdown
# ADR-023: Migrate to Microservices Architecture

Context: From Summoner Mission "Microservices Migration"
Decision: Extract auth service first, then user service
Rationale: [From Summoner MCD]
```

### With Style Master 🎨

**Style Master style guide**: Design tokens

**Docs synced**:
```markdown
# Theme Customization

Override design tokens in your CSS:
\`\`\`css
:root {
  --color-primary: #your-color;
}
\`\`\`

See [Style Guide](./STYLEGUIDE.md) for all tokens.
```

## Scripts Reference

### generate_docs.py
Generates initial documentation from code and knowledge.

**Options**:
- `--type readme|api|adr|onboarding|all`
- `--output docs/`
- `--include-oracle` (include Oracle knowledge)

### validate_docs.py
Validates documentation for staleness and issues.

**Checks**:
- Stale documentation
- Broken links
- Invalid examples
- Missing documentation

### sync_docs.py
Synchronizes documentation from various sources.

**Sources**:
- `--source oracle` (Oracle knowledge)
- `--source summoner` (Summoner MCDs)
- `--source style-master` (Style guides)
- `--source code` (Code comments)

### generate_changelog.py
Generates changelog from git history and Oracle.

**Format**: Semantic (Added/Changed/Fixed/Deprecated/Removed)

## Best Practices

### 1. Document WHY, Not Just WHAT
Use Oracle to capture the reasoning behind decisions.

### 2. Keep Examples Executable
All code examples should be tested and copy-pasteable.

### 3. Link Everything
Connect documentation to Oracle, Summoner, code, and external resources.

### 4. Automate Updates
Set up hooks to update docs on code changes.

### 5. Validate Regularly
Run validation as part of CI/CD.

## Workflow

```bash
# Daily: After development session
python .claude/skills/documentation-wizard/Scripts/generate_docs.py --type api
python .claude/skills/documentation-wizard/Scripts/validate_docs.py

# Weekly: Comprehensive sync
python .claude/skills/documentation-wizard/Scripts/sync_docs.py --source all
python .claude/skills/documentation-wizard/Scripts/generate_changelog.py

# Before release: Full documentation review
python .claude/skills/documentation-wizard/Scripts/validate_docs.py --strict
```

## Templates Available

- **README**: Project and package READMEs
- **ADR**: Architecture Decision Records
- **API**: API documentation
- **Onboarding**: New developer guides
- **Contributing**: Contribution guidelines

See `References/` directory for all templates.

---

**Documentation Wizard v1.0** - Documentation that stays alive
