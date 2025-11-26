You are initializing the ClaudeShack skill ecosystem for the user's project.

## What This Does

The init-ecosystem script performs complete ClaudeShack initialization:

1. **Oracle Setup**: Creates `.oracle/` directory with knowledge, sessions, timeline
2. **Guardian Setup**: Creates `.guardian/config.json` with auto-review thresholds
3. **History Mining**: Extracts patterns, corrections, preferences from existing Claude conversations
4. **Context Generation**: Generates session-start context from Oracle knowledge
5. **claude.md Update**: Adds ClaudeShack section and Oracle context placeholder
6. **gitignore Update**: Adds `.oracle/`, `.guardian/`, etc.

## Run the Script

```bash
python .claude/skills/init-ecosystem.py
```

Or with options:
```bash
# Skip history mining (faster, if no existing conversations)
python .claude/skills/init-ecosystem.py --skip-history

# Verbose output
python .claude/skills/init-ecosystem.py --verbose
```

## After Initialization

1. **Skills are ready to use**:
   - `use oracle to remember this pattern`
   - `use guardian to review this code`
   - `use summoner to coordinate [task]`

2. **Optional: Set up SessionStart hook** (see output instructions)
   - Auto-loads Oracle context every session
   - See `.claude/skills/oracle/scripts/HOOK_SETUP.md`

3. **Record your first session**:
   ```bash
   python .claude/skills/oracle/scripts/record_session.py --interactive
   ```

4. **Update Oracle context in claude.md**:
   ```bash
   python .claude/skills/oracle/scripts/generate_context.py --output claude.md --update
   ```

## Troubleshooting

- **"Oracle not initialized"**: Run the init script again
- **No history mined**: Normal for new projects, Oracle learns as you work
- **Permissions error**: Check write access to project directory
