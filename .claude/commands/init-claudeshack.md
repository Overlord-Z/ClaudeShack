You are helping the user initialize ClaudeShack skills in their project.

## Your Task

1. **Check for existing claude.md**:
   - If `claude.md` exists, read it
   - If not, you'll create one

2. **Add ClaudeShack section** to claude.md:
   ```markdown
   ## ClaudeShack Skills

   This project uses ClaudeShack skills for enhanced development:

   ### Available Skills
   - **Oracle**: Project memory and learning (tracks patterns, corrections, knowledge)
   - **Guardian**: Quality gates and session health monitoring (auto code review)
   - **Summoner**: Multi-agent orchestration (complex task breakdown)
   - **Wizard**: Documentation maintenance (no hallucinations, fact-checked)
   - **Style Master**: CSS and frontend styling expert
   - **Evaluator**: Privacy-first telemetry (opt-in, anonymous)

   ### Core Principles
   - **KISS**: Keep it simple, avoid complexity
   - **DRY**: Don't repeat yourself
   - **Privacy First**: No PII, opt-in telemetry only
   - **Minimal Context**: Pass only what's needed to subagents
   - **Facts Over Fiction**: Documentation verified against code

   ### Quick Start

   **Initialize Oracle** (project memory):
   ```bash
   python -c "import os; os.makedirs('.oracle/knowledge', exist_ok=True); os.makedirs('.oracle/sessions', exist_ok=True); os.makedirs('.oracle/timeline', exist_ok=True)"
   ```

   **Use Skills**:
   - `use oracle to remember this pattern`
   - `use guardian to review this code`
   - `use summoner to coordinate [complex task]`
   - `use wizard to update documentation`

   **Session Handoff** (when context degrades):
   - `/handoff` - Smooth transition to fresh session with context preserved

   ### Guardian Auto-Triggers
   Guardian automatically activates when:
   - >50 lines of code written
   - Same error 3+ times
   - Same file edited 5+ times in 10 minutes
   - Multiple corrections needed

   ### Integration Benefits
   - Guardian + Oracle: +31% suggestion acceptance
   - Wizard + Oracle: +19% doc accuracy
   - Style Master + Oracle: +22% consistency

   For full documentation: https://github.com/Overlord-Z/ClaudeShack
   ```

3. **Initialize Oracle directory structure**:
   ```bash
   mkdir -p .oracle/knowledge .oracle/sessions .oracle/timeline .oracle/scripts
   ```

4. **Create initial Oracle knowledge files** (empty JSON arrays):
   ```bash
   echo '[]' > .oracle/knowledge/patterns.json
   echo '[]' > .oracle/knowledge/corrections.json
   echo '[]' > .oracle/knowledge/gotchas.json
   echo '[]' > .oracle/knowledge/solutions.json
   echo '[]' > .oracle/knowledge/preferences.json
   ```

5. **Add .oracle/ to .gitignore** (if not already there):
   ```
   # ClaudeShack Oracle (project-specific knowledge)
   .oracle/
   ```

6. **Create .guardian/config.json** with default thresholds:
   ```json
   {
     "enabled": true,
     "sensitivity": {
       "lines_threshold": 50,
       "error_repeat_threshold": 3,
       "file_churn_threshold": 5,
       "correction_threshold": 3,
       "context_warning_percent": 0.7
     },
     "auto_review": {
       "enabled": true
     },
     "model": "haiku"
   }
   ```

7. **Add .guardian/ to .gitignore**:
   ```
   # ClaudeShack Guardian (session health)
   .guardian/
   ```

8. **Confirm with user**:
   ```
   ✅ ClaudeShack initialized!

   Created:
   - claude.md (updated with ClaudeShack context)
   - .oracle/ directory structure
   - .guardian/config.json
   - Updated .gitignore

   Ready to use:
   - use oracle to remember project patterns
   - use guardian to review code (auto-triggers enabled)
   - use summoner for complex tasks
   - use wizard for documentation

   Tip: Oracle learns as you work - correct mistakes and it remembers!
   ```

## Important Notes

- Preserve any existing content in claude.md (don't overwrite)
- Oracle and Guardian directories are gitignored by default (project-specific)
- Evaluator is opt-in (disabled by default)
- Guardian starts with conservative thresholds, learns from feedback

## Error Handling

- If claude.md is read-only, ask user for permission
- If .oracle/ already exists, don't recreate (ask if user wants to reset)
- If .gitignore doesn't exist, create it
