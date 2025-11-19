# ClaudeShack Installation Guide

Complete guide to installing and setting up ClaudeShack skills marketplace.

## Installation Methods

### Method 1: Plugin System (Recommended)

Use Claude Code's plugin system to install skills:

```bash
# Install individual skills
/plugin install summoner@claudeshack
/plugin install oracle@claudeshack
/plugin install style-master@claudeshack
/plugin install documentation-wizard@claudeshack

# Or install all skills at once
/plugin install all@claudeshack
```

### Method 2: Git Clone

Clone the repository for local use:

```bash
# Clone repository
git clone https://github.com/Overlord-Z/ClaudeShack.git
cd ClaudeShack

# Verify installation
python marketplace/scripts/claudeshack verify

# Optional: Set up CLI tool
export CLAUDESHACK_HOME="$(pwd)"
export PATH="$PATH:$(pwd)/marketplace/scripts"
```

### Method 3: Manual Download

Download and extract:

1. Download latest release from [GitHub Releases](https://github.com/Overlord-Z/ClaudeShack/releases)
2. Extract to desired location
3. Set `CLAUDESHACK_HOME` environment variable

## Post-Installation

### Verify Installation

```bash
# Using CLI tool
cd ClaudeShack
python marketplace/scripts/claudeshack verify

# Or manually check
ls -la .claude/skills/
```

Expected output:
```
✅ Summoner: OK
✅ Oracle: OK
✅ Style Master: OK
✅ Documentation Wizard: OK
```

### Set Up Environment

Add to your `.bashrc` or `.zshrc`:

```bash
# ClaudeShack
export CLAUDESHACK_HOME="$HOME/ClaudeShack"
export PATH="$PATH:$CLAUDESHACK_HOME/marketplace/scripts"
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Verify CLI Tool

```bash
claudeshack version
claudeshack list
```

## Skill-Specific Setup

### Oracle Skill

Initialize Oracle for a project:

```bash
cd your-project
python $CLAUDESHACK_HOME/.claude/skills/oracle/Scripts/init_oracle.py
```

This creates `.oracle/` directory for knowledge management.

### Style Master

Analyze your project styles:

```bash
cd your-project
python $CLAUDESHACK_HOME/.claude/skills/style-master/Scripts/analyze_styles.py --detailed
```

### Documentation Wizard

Generate documentation:

```bash
cd your-project
python $CLAUDESHACK_HOME/.claude/skills/documentation-wizard/Scripts/generate_docs.py
```

## Updating

### Via Plugin System

```bash
/plugin update @claudeshack
```

### Via Git

```bash
cd ClaudeShack
git pull origin main
python marketplace/scripts/claudeshack verify
```

## Troubleshooting

### Skills Not Found

**Problem**: Claude Code doesn't detect skills

**Solution**:
```bash
# Verify installation
claudeshack verify

# Check plugin.json
cat .claude/plugin.json

# Ensure you're in ClaudeShack directory
pwd
```

### CLI Tool Not Found

**Problem**: `claudeshack: command not found`

**Solution**:
```bash
# Set environment variables
export CLAUDESHACK_HOME="/path/to/ClaudeShack"
export PATH="$PATH:$CLAUDESHACK_HOME/marketplace/scripts"

# Or use full path
python /path/to/ClaudeShack/marketplace/scripts/claudeshack version
```

### Permission Denied

**Problem**: Scripts not executable

**Solution**:
```bash
chmod +x marketplace/scripts/claudeshack
chmod +x .claude/skills/*/Scripts/*.py
```

## Uninstallation

### Remove via Plugin System

```bash
/plugin uninstall summoner@claudeshack
/plugin uninstall oracle@claudeshack
/plugin uninstall style-master@claudeshack
/plugin uninstall documentation-wizard@claudeshack
```

### Remove Manual Installation

```bash
rm -rf ~/ClaudeShack
# Remove from .bashrc/.zshrc
# Remove CLAUDESHACK_HOME and PATH additions
```

## Platform-Specific Notes

### macOS

```bash
# Install location
/usr/local/share/claudeshack

# Or user directory
~/ClaudeShack
```

### Linux

```bash
# System-wide
/opt/claudeshack

# Or user directory
~/.claudeshack
```

### Windows

```powershell
# Install location
C:\Program Files\ClaudeShack

# Or user directory
%USERPROFILE%\ClaudeShack
```

Set environment variables via System Properties > Environment Variables.

## Next Steps

After installation:

1. **Read Documentation**: `cat MARKETPLACE.md`
2. **Try a Skill**: `claudeshack info summoner`
3. **Initialize Oracle**: For project memory across sessions
4. **Analyze Styles**: For frontend projects
5. **Generate Docs**: Keep documentation in sync

## Getting Help

- **CLI Help**: `claudeshack --help`
- **Skill Info**: `claudeshack info <skill-name>`
- **GitHub Issues**: [Report Issues](https://github.com/Overlord-Z/ClaudeShack/issues)
- **Documentation**: See individual skill README files

---

**Welcome to ClaudeShack!** 🏛️
