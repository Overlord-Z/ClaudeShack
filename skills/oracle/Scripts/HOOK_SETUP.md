# Oracle SessionStart Hook Setup

This guide explains how to configure Claude Code to automatically load Oracle context when sessions start.

## Overview

The SessionStart hook automatically injects Oracle knowledge into every new or resumed Claude Code session, ensuring Claude always has access to:
- Critical gotchas and warnings
- Recent corrections
- High-priority patterns and solutions
- Project-specific preferences

## Quick Setup

### 1. Add Hook to Claude Code Settings

Edit your Claude Code settings file (location varies by platform):
- **macOS**: `~/Library/Application Support/Claude/settings.json`
- **Linux**: `~/.config/Claude/settings.json`
- **Windows**: `%APPDATA%\Claude\settings.json`

Add this configuration to the `hooks` section:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "python /full/path/to/ClaudeShack/skills/oracle/Scripts/session_start_hook.py"
          }
        ]
      }
    ]
  }
}
```

**Important**: Replace `/full/path/to/ClaudeShack` with the actual absolute path to your ClaudeShack directory.

### 2. Test the Hook

Test that the hook works by running it manually:

```bash
cd /path/to/your/project
python /path/to/ClaudeShack/skills/oracle/Scripts/session_start_hook.py --debug
```

You should see Oracle context output to stderr. If you see "Oracle: Not initialized", run:

```bash
python /path/to/ClaudeShack/skills/oracle/Scripts/init_oracle.py
```

### 3. Start a New Session

Start a new Claude Code session. Oracle context should automatically be injected!

You'll see something like:

```markdown
# Oracle Project Knowledge

Knowledge Base: 25 entries | 5 sessions recorded

## Key Knowledge

### Gotchas (Watch Out!)

- **[CRITICAL]** Database connections must be closed explicitly
- **API rate limit is 100 req/min**

### Recent Corrections

- Use textContent instead of innerHTML for user input (XSS prevention)
- Always use async/await, not callbacks
```

## Configuration Options

### Context Tier Levels

Control how much context is loaded using the `ORACLE_CONTEXT_TIER` environment variable:

```bash
# In your shell profile (.bashrc, .zshrc, etc.):
export ORACLE_CONTEXT_TIER=1  # Default: Critical + High priority only
export ORACLE_CONTEXT_TIER=2  # Include Medium priority
export ORACLE_CONTEXT_TIER=3  # All knowledge
```

Or pass it directly in the hook configuration:

```json
{
  "type": "command",
  "command": "ORACLE_CONTEXT_TIER=2 python /path/to/session_start_hook.py"
}
```

Or use the CLI argument:

```json
{
  "type": "command",
  "command": "python /path/to/session_start_hook.py --tier 2"
}
```

### Maximum Context Length

Limit context size to avoid overwhelming the session:

```bash
export ORACLE_MAX_CONTEXT_LENGTH=5000  # Default: 5000 characters
export ORACLE_MAX_CONTEXT_LENGTH=10000 # More context
export ORACLE_MAX_CONTEXT_LENGTH=2000  # Less context
```

Or via CLI:

```json
{
  "type": "command",
  "command": "python /path/to/session_start_hook.py --max-length 10000"
}
```

## Advanced Configuration

### Hook on Resume Only

To load Oracle context only when resuming sessions (not on new sessions):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "resume",
        "hooks": [
          {
            "type": "command",
            "command": "python /path/to/session_start_hook.py --source resume"
          }
        ]
      }
    ]
  }
}
```

### Hook on Both Startup and Resume

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "python /path/to/session_start_hook.py --source startup"
          }
        ]
      },
      {
        "matcher": "resume",
        "hooks": [
          {
            "type": "command",
            "command": "python /path/to/session_start_hook.py --source resume"
          }
        ]
      }
    ]
  }
}
```

### Per-Project Configuration

If you work with multiple projects, you can use different configurations:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "pathPattern": "**/my-critical-project/**",
        "hooks": [
          {
            "type": "command",
            "command": "ORACLE_CONTEXT_TIER=1 python /path/to/session_start_hook.py"
          }
        ]
      },
      {
        "matcher": "startup",
        "pathPattern": "**/my-casual-project/**",
        "hooks": [
          {
            "type": "command",
            "command": "ORACLE_CONTEXT_TIER=3 python /path/to/session_start_hook.py"
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting

### Hook Not Running

1. **Check settings file syntax**: Ensure valid JSON (no trailing commas, proper quotes)
2. **Check paths**: Use absolute paths, not relative
3. **Check permissions**: Ensure script is executable (`chmod +x session_start_hook.py`)
4. **Test manually**: Run the script from your project directory

### No Context Showing

1. **Verify Oracle is initialized**: Run `ls -la .oracle/` in your project
2. **Check if knowledge exists**: Run `python /path/to/query_knowledge.py --summary`
3. **Test hook in debug mode**: `python session_start_hook.py --debug`

### Context Too Large

Reduce context with:
- Lower tier level (`ORACLE_CONTEXT_TIER=1`)
- Smaller max length (`ORACLE_MAX_CONTEXT_LENGTH=3000`)
- Prioritize your knowledge entries (set priority to `low` for less critical items)

### Context Not Relevant

The SessionStart hook loads critical/high priority items only. To get task-specific context:

1. Use the oracle skill manually: `/oracle` (if available)
2. Run: `python /path/to/generate_context.py --task "your task description"`
3. Query specific knowledge: `python /path/to/query_knowledge.py "keywords"`

## Best Practices

1. **Keep critical items truly critical**: Only mark security, data loss, and breaking issues as critical
2. **Regular cleanup**: Review and remove outdated knowledge monthly
3. **Use tags**: Tag knowledge for better organization
4. **Record sessions**: Use `record_session.py` after important sessions
5. **Analyze history**: Run `analyze_history.py --auto-populate` weekly to mine conversation history

## Hook Output Format

The hook outputs JSON in this format:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "# Oracle Project Knowledge\n\n..."
  }
}
```

Claude Code reads the `additionalContext` field and injects it into the session context.

## Verification

To verify the hook is working:

1. Start a new session
2. Ask Claude: "What do you know about this project from Oracle?"
3. Claude should reference the injected knowledge

## Disable Hook Temporarily

To temporarily disable the hook without removing configuration:

1. Add a condition to the matcher that won't match
2. Or comment out the hook in settings (use `//` in JSONC format if supported)
3. Or set environment variable: `export ORACLE_HOOK_DISABLED=1`

## Related Scripts

- `init_oracle.py` - Initialize Oracle for a project
- `record_session.py` - Record session learnings
- `query_knowledge.py` - Query knowledge base
- `generate_context.py` - Generate context summaries
- `analyze_history.py` - Mine conversation history

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Claude Code hooks documentation
3. Test the script manually with `--debug` flag
4. Check Claude Code logs for hook execution errors
