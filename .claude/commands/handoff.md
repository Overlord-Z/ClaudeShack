You are assisting with a **session handoff** to prevent degradation from context compaction.

## Session Handoff Protocol

The previous session has become degraded (context bloat, repeated errors, or extended duration). We're starting fresh with critical context preserved.

### Your Task:

1. **Run the handoff script** to get context from the previous session:
   ```bash
   python skills/oracle/Scripts/session_handoff.py --import handoff_context.json
   ```

2. **Review the handoff context** displayed, which includes:
   - Critical Oracle patterns (things to remember)
   - Recent corrections (mistakes to avoid)
   - Active gotchas (known issues)
   - Active Summoner MCDs (ongoing complex tasks)
   - Guardian health metrics (why we're handing off)

3. **Confirm understanding** with the user:
   - Summarize what you understand from the handoff
   - Confirm the current task or objective
   - Ask for any clarifications needed

4. **Continue work** with the fresh context, avoiding the issues that caused degradation in the previous session.

## Key Principles:

- **KISS**: You now have a clean slate - don't overcomplicate
- **DRY**: Reuse the patterns from Oracle, don't reinvent
- **Learn**: The corrections show what went wrong before - don't repeat
- **Focus**: Guardian triggered handoff for a reason - stay focused

## Example Confirmation:

```
✅ Session handoff complete!

From the previous session, I understand:
- We're working on [summarize from MCD or context]
- Critical patterns: [list 2-3 key patterns from Oracle]
- Recent corrections: [list key mistakes to avoid]
- Session was degraded due to: [reason from Guardian]

Current objective: [confirm with user]

Ready to continue with a fresh, focused approach. What should we tackle first?
```
