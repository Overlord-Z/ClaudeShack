# ClaudeShack Marketplace Infrastructure

This directory contains the marketplace infrastructure for ClaudeShack skills.

## Contents

### Scripts

**`claudeshack` CLI Tool**
- List available skills
- Show skill information
- Verify installation
- Version management

Usage:
```bash
claudeshack list                # List all skills
claudeshack info summoner       # Show skill details
claudeshack verify              # Verify installation
claudeshack version             # Show version
```

### Registry

**`skills.json`** - Complete skill catalog with:
- Detailed metadata for all skills
- Category organization
- Integration mappings
- Installation instructions
- Skill bundles

### Documentation

**`INSTALL.md`** - Complete installation guide:
- Multiple installation methods
- Post-installation setup
- Skill-specific configuration
- Troubleshooting

## Quick Start

### Install ClaudeShack CLI

```bash
# Add to PATH
export CLAUDESHACK_HOME="/path/to/ClaudeShack"
export PATH="$PATH:$CLAUDESHACK_HOME/marketplace/scripts"

# Verify
claudeshack version
```

### List Available Skills

```bash
claudeshack list
```

Output:
```
📦 ClaudeShack Skills

Skill                     Version    Category         Status
──────────────────────────────────────────────────────────────────────
Summoner                  1.0.0      orchestration    ✅ Installed
Oracle                    1.0.0      knowledge        ✅ Installed
Style Master              1.0.0      frontend         ✅ Installed
Documentation Wizard      1.0.0      documentation    ✅ Installed

Total: 4 skills
```

### Get Skill Information

```bash
claudeshack info oracle
```

Output:
```
📚 Oracle (v1.0.0)

ID: oracle
Category: knowledge
Author: ClaudeShack

Description:
  Project memory and learning system...

Tags: memory, learning, automation, knowledge-base, context

Integrations: summoner, style-master, documentation-wizard

Install command:
  /plugin install oracle@claudeshack
```

### Verify Installation

```bash
claudeshack verify
```

Output:
```
🔍 Verifying ClaudeShack installation...

✅ Summoner: OK
✅ Oracle: OK
✅ Style Master: OK
✅ Documentation Wizard: OK

✅ ClaudeShack installation is valid!
```

## Marketplace Features

### Skill Categorization

Skills are organized by category:
- **Orchestration**: Complex task coordination
- **Knowledge**: Memory and learning systems
- **Frontend**: Styling and design systems
- **Documentation**: Documentation generation and sync

### Skill Bundles

Pre-configured bundles for common use cases:

**All Bundle**: All four skills
```bash
/plugin install all@claudeshack
```

**Core Bundle**: Summoner + Oracle
```bash
/plugin install core@claudeshack
```

**Frontend Bundle**: Style Master + Doc Wizard + Oracle
```bash
/plugin install frontend@claudeshack
```

### Integration Tracking

The registry tracks which skills integrate with each other:
- Oracle integrates with all other skills
- Summoner uses Oracle for context
- Style Master syncs with Doc Wizard
- Documentation Wizard leverages all skills

## Development

### Adding a New Skill

1. Create skill directory in `.claude/skills/`
2. Add skill definition to `.claude/plugin.json`
3. Add skill to `marketplace/registry/skills.json`
4. Update documentation
5. Run `claudeshack verify`

### Updating Skills

1. Update version in `plugin.json`
2. Update version in `registry/skills.json`
3. Update CHANGELOG
4. Tag release

## API

### Plugin Manifest (`.claude/plugin.json`)

Used by Claude Code plugin system:
```json
{
  "name": "claudeshack",
  "version": "1.0.0",
  "skills": [...]
}
```

### Skill Registry (`registry/skills.json`)

Extended metadata for marketplace:
```json
{
  "skills": [
    {
      "id": "skill-id",
      "name": "Skill Name",
      "version": "1.0.0",
      "category": "category",
      "features": [...],
      "useCases": [...]
    }
  ]
}
```

## Future Enhancements

- [ ] Web-based marketplace UI
- [ ] Automatic update checking
- [ ] Skill rating and reviews
- [ ] Community skill submissions
- [ ] Dependency management
- [ ] Version conflict resolution

---

**ClaudeShack Marketplace v1.0.0**
