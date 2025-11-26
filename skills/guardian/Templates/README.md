# Guardian Templates

This directory contains templates for different Guardian review and planning tasks. Templates provide structured, consistent prompts for Haiku subagents with appropriate constraints and output formats.

## Available Templates

### security_review.json
**Focus**: Security vulnerabilities and OWASP Top 10

**Best For:**
- Authentication/authorization code
- Cryptographic implementations
- Input validation
- API endpoints
- Payment processing
- Sensitive data handling

**Output Format**: Suggestions with severity, CWE references, exploit scenarios

### performance_review.json
**Focus**: Performance optimization and efficiency

**Best For:**
- Database queries
- API performance
- Algorithm complexity
- Memory usage
- Async operations
- Caching opportunities

**Output Format**: Suggestions with complexity analysis and estimated improvements

### feature_planning.json
**Focus**: Breaking down complex features into subtasks

**Best For:**
- Large feature implementations
- Multi-component systems
- Complex refactoring
- Integration projects

**Output Format**: Subtasks with dependencies, estimates, risks, and acceptance criteria

## Using Templates

### Via Command Line

```bash
# List available templates
python guardian/scripts/template_loader.py --list

# Load a template
python guardian/scripts/template_loader.py --template security_review

# Show template configuration
python guardian/scripts/template_loader.py --template security_review --show-config
```

### Via Guardian Skill

```bash
# Use a template for review
python guardian/scripts/guardian.py review --file auth.py --template security_review

# Use a template for planning
python guardian/scripts/guardian.py plan --task "Build REST API" --template feature_planning
```

### In Code

```python
from template_loader import load_template, apply_template_to_context

# Load template
template = load_template('security_review')

# Apply to context
prompt = apply_template_to_context(template, minimal_context)

# Get configuration for context_filter.py
config = get_template_config(template)
```

## Creating Custom Templates

### Option 1: Base on Existing Template

```bash
python guardian/scripts/template_loader.py \
    --create my_security_review \
    --based-on security_review \
    --description "Custom security review for our codebase"
```

This creates `my_security_review.json` which you can then customize.

### Option 2: Create from Scratch

```bash
python guardian/scripts/template_loader.py \
    --create my_custom_review \
    --description "Custom review template"
```

This creates a minimal template you can build on.

### Option 3: Manual Creation

Create a JSON file with this structure:

```json
{
  "name": "my_review",
  "description": "My custom review template",
  "task_type": "review",
  "focus": "my_focus_keywords",
  "agent_prompt_template": "You are a READ-ONLY code reviewer...\n\n{context}\n\nReturn JSON array...",
  "oracle_categories": ["patterns", "gotchas"],
  "oracle_tags_required": ["tag1", "tag2"],
  "max_oracle_patterns": 5,
  "max_oracle_gotchas": 5,
  "always_include_files": [],
  "validation_rules": {
    "min_confidence": 0.5,
    "block_contradictions": true
  }
}
```

## Template Structure

### Required Fields

- `name`: Unique template identifier
- `description`: Human-readable description
- `task_type`: "review", "plan", or "debug"
- `agent_prompt_template`: Prompt template with `{context}` placeholder

### Optional Fields

- `focus`: Keywords for context filtering (e.g., "security performance")
- `oracle_categories`: Oracle knowledge categories to load ["patterns", "gotchas", "corrections", "solutions"]
- `oracle_tags_required`: Tags to filter Oracle knowledge by
- `max_oracle_patterns`: Maximum Oracle patterns to include (default: 5)
- `max_oracle_gotchas`: Maximum Oracle gotchas to include (default: 5)
- `always_include_files`: Additional files to always include (e.g., config files)
- `validation_rules`: Rules for validating subagent suggestions

### Validation Rules

```json
{
  "min_confidence": 0.5,           // Minimum confidence score to present
  "block_contradictions": true,     // Block suggestions that contradict Oracle
  "require_severity": false,        // Require severity field in suggestions
  "require_impact": false,          // Require impact field in suggestions
  "require_dependencies": false     // Require dependencies field (for planning)
}
```

## Prompt Template Guidelines

### Critical Constraints Section

Always include:

```
CRITICAL CONSTRAINTS:
- DO NOT use Write, Edit, NotebookEdit, or Bash tools
- DO NOT modify any files
- DO NOT execute any code
- ONLY read the provided context and return suggestions
```

### Context Placeholder

Include `{context}` where minimal context should be inserted:

```
Your task: Review this code for security issues.

{context}

Return your findings...
```

### Output Format

Specify clear JSON output format:

```json
[
  {
    "text": "Clear description of the issue",
    "category": "security|performance|style|bugs",
    "file": "file path",
    "line": line_number (if applicable, otherwise null)
  }
]
```

### Reminder Section

End with:

```
Remember: You are READ-ONLY. Only analyze and suggest, never modify.
```

## Best Practices

### For Review Templates

1. **Be Specific**: Focus on particular types of issues (security, performance, style)
2. **Provide Examples**: Show what good/bad code looks like
3. **Reference Standards**: OWASP, CWE, language style guides
4. **Request Details**: Ask for line numbers, severity, remediation steps

### For Planning Templates

1. **Encourage Decomposition**: Break large tasks into small, testable pieces
2. **Request Dependencies**: Ask for task ordering and prerequisites
3. **Ask for Risks**: Identify potential issues early
4. **Require Estimates**: Time and complexity estimates help prioritization

### For All Templates

1. **Minimal Context**: Only request what's needed for the task
2. **Read-Only Focus**: Emphasize analysis over action
3. **Structured Output**: Request JSON for easy parsing
4. **Oracle Integration**: Leverage Oracle knowledge for context

## Template Versioning

Templates follow semantic versioning via filename suffixes:

- `security_review.json` - Latest version
- `security_review_v2.json` - Explicit version 2
- `security_review_legacy.json` - Deprecated version

When updating templates, create a new version and mark old ones as legacy.

## Contributing Templates

To contribute a new template:

1. Create your template following the structure above
2. Test it with real code reviews
3. Document what it's best for
4. Submit a PR with:
   - Template JSON file
   - Example usage
   - Test results

Good templates help the entire community!

## Examples

### Example: Security Review

```bash
# Run security review on auth file
python guardian/scripts/guardian.py review \
    --file src/auth.py \
    --template security_review

# Guardian will:
# 1. Load security_review.json template
# 2. Extract minimal context (auth.py + security Oracle patterns)
# 3. Apply template to context
# 4. Spawn Haiku agent with structured prompt
# 5. Validate suggestions against Oracle
# 6. Present results with confidence scores
```

### Example: Performance Review

```bash
# Run performance review on database queries
python guardian/scripts/guardian.py review \
    --file src/database/queries.py \
    --template performance_review

# Focuses on:
# - Query complexity
# - N+1 problems
# - Missing indexes
# - Caching opportunities
```

### Example: Feature Planning

```bash
# Plan a new REST API
python guardian/scripts/guardian.py plan \
    --task "Build REST API with auth and rate limiting" \
    --template feature_planning

# Returns:
# - Subtask breakdown
# - Dependencies
# - Estimates
# - Risk assessment
```
