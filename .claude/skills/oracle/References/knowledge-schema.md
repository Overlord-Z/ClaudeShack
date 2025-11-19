# Oracle Knowledge Schema

This document defines the structure and schema for Oracle knowledge entries.

## Knowledge Entry Structure

### JSON Format

```json
{
  "id": "unique-identifier",
  "category": "pattern|preference|gotcha|solution|correction",
  "priority": "critical|high|medium|low",
  "title": "Brief descriptive title (max 100 chars)",
  "content": "Detailed information about this knowledge",
  "context": "When this knowledge applies",
  "examples": [
    "Example 1",
    "Example 2"
  ],
  "learned_from": "session-id or source",
  "created": "2025-11-19T10:30:00Z",
  "last_used": "2025-11-19T10:30:00Z",
  "use_count": 0,
  "tags": ["tag1", "tag2", "tag3"]
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string (UUID) | Yes | Unique identifier for this entry |
| `category` | enum | Yes | Category: pattern, preference, gotcha, solution, or correction |
| `priority` | enum | Yes | Priority level: critical, high, medium, or low |
| `title` | string | Yes | Brief, descriptive title (max 100 characters) |
| `content` | string | Yes | Detailed information, explanation, or description |
| `context` | string | No | When/where this knowledge applies |
| `examples` | array[string] | No | Concrete examples demonstrating the knowledge |
| `learned_from` | string | No | Session ID or source where this was learned |
| `created` | ISO 8601 | Yes | When this entry was created |
| `last_used` | ISO 8601 | No | When this knowledge was last recalled/used |
| `use_count` | integer | No | Number of times this knowledge has been used |
| `tags` | array[string] | No | Tags for categorization and search |

## Categories Explained

### Pattern

**Purpose**: Capture code patterns, architectural decisions, and conventions

**When to use**:
- Established coding patterns in the project
- Architecture decisions
- Design patterns being used
- Coding conventions and style

**Example**:
```json
{
  "category": "pattern",
  "title": "Use factory pattern for database connections",
  "content": "All database connections should be created through DatabaseFactory.create() which handles connection pooling, configuration, and error handling.",
  "context": "When creating new database connections",
  "examples": [
    "const db = DatabaseFactory.create('postgres')",
    "const cache = DatabaseFactory.create('redis')"
  ],
  "priority": "high",
  "tags": ["database", "factory-pattern", "architecture"]
}
```

### Preference

**Purpose**: Capture user/team preferences and stylistic choices

**When to use**:
- Team coding style preferences
- Tool choices
- Workflow preferences
- Naming conventions

**Example**:
```json
{
  "category": "preference",
  "title": "Prefer functional programming over OOP",
  "content": "Team prefers functional programming style with pure functions, immutability, and composition over object-oriented approaches.",
  "context": "When designing new features or refactoring code",
  "examples": [
    "Use map/filter/reduce instead of for loops",
    "Use pure functions without side effects"
  ],
  "priority": "medium",
  "tags": ["coding-style", "functional-programming"]
}
```

### Gotcha

**Purpose**: Capture known issues, pitfalls, edge cases, and things to avoid

**When to use**:
- Known bugs or quirks
- Common mistakes
- Platform-specific issues
- Performance pitfalls
- Security concerns

**Example**:
```json
{
  "category": "gotcha",
  "title": "Database connection pool must be explicitly closed",
  "content": "The database connection pool doesn't close automatically. Failing to call pool.close() in shutdown handlers causes memory leaks and prevents clean exits.",
  "context": "When setting up application lifecycle hooks",
  "examples": [
    "process.on('SIGTERM', () => pool.close())",
    "app.on('shutdown', async () => await pool.close())"
  ],
  "priority": "critical",
  "tags": ["database", "memory-leak", "lifecycle"]
}
```

### Solution

**Purpose**: Capture proven solutions to specific problems

**When to use**:
- Solutions to problems encountered
- Best practices discovered
- Successful implementations
- Recommended approaches

**Example**:
```json
{
  "category": "solution",
  "title": "Use cursor-based pagination for large datasets",
  "content": "For datasets with millions of records, use cursor-based pagination instead of offset-based to avoid performance degradation and inconsistencies.",
  "context": "When implementing pagination for large tables",
  "examples": [
    "?cursor=xyz&limit=100 instead of ?page=1&limit=100",
    "SELECT * FROM users WHERE id > $cursor LIMIT $limit"
  ],
  "priority": "high",
  "tags": ["pagination", "performance", "database"]
}
```

### Correction

**Purpose**: Capture mistakes Claude made and the correct approach

**When to use**:
- User corrected Claude's approach
- Wrong assumptions were made
- Incorrect implementations
- Learning from mistakes

**Example**:
```json
{
  "category": "correction",
  "title": "Don't use innerHTML for user content",
  "content": "❌ Wrong: element.innerHTML = userInput\n✓ Right: element.textContent = userInput\n\nReason: innerHTML allows XSS attacks when used with user input.",
  "context": "When displaying user-generated content",
  "examples": [
    "// Correct: element.textContent = comment.body",
    "// Correct: element.appendChild(document.createTextNode(input))"
  ],
  "priority": "critical",
  "tags": ["security", "xss", "dom"]
}
```

## Priority Levels

### Critical

- Security vulnerabilities
- Data loss risks
- Production-breaking issues
- Must be remembered and applied

**Examples**:
- Security best practices
- Data integrity rules
- Critical gotchas

### High

- Important patterns
- Frequent corrections
- Performance considerations
- Should be remembered and applied

**Examples**:
- Core architectural patterns
- Common gotchas
- Team preferences

### Medium

- Helpful solutions
- General preferences
- Nice-to-know patterns
- Could be remembered

**Examples**:
- Helper patterns
- Coding style details
- Useful solutions

### Low

- Optional information
- Rare cases
- Historical context
- Reference only

**Examples**:
- Deprecated approaches
- Rarely-used patterns
- Historical decisions

## Tags Best Practices

### Effective Tags

**Technology/Framework**:
- `react`, `typescript`, `python`, `postgres`, `redis`

**Domain**:
- `authentication`, `api`, `database`, `testing`, `deployment`

**Type**:
- `security`, `performance`, `bug`, `refactoring`

**Component**:
- `frontend`, `backend`, `database`, `infrastructure`

### Tag Naming Conventions

- Use lowercase
- Use hyphens for multi-word tags (`cursor-based-pagination`)
- Be specific but not too granular
- Reuse existing tags when possible
- Limit to 3-5 tags per entry

## Index Schema

The `index.json` file maintains metadata for quick access:

```json
{
  "created": "2025-11-19T10:00:00Z",
  "last_updated": "2025-11-19T15:30:00Z",
  "total_entries": 42,
  "categories": {
    "patterns": 10,
    "preferences": 5,
    "gotchas": 8,
    "solutions": 15,
    "corrections": 4
  },
  "sessions": [
    "2025-11-19_session_001",
    "2025-11-19_session_002"
  ],
  "version": "1.0"
}
```

## Migration and Versioning

If the schema changes in future versions:

1. Update `version` field in index
2. Provide migration scripts
3. Maintain backward compatibility where possible
4. Document breaking changes

## Validation

When adding entries programmatically, validate:

1. **Required fields**: id, category, priority, title, content, created
2. **Valid enums**: category and priority must be from allowed values
3. **Type checking**: Ensure correct data types
4. **UUID format**: id should be valid UUID
5. **ISO 8601 dates**: created and last_used should be valid ISO 8601

## Best Practices

### Writing Good Titles

✅ Good:
- "Use bcrypt for password hashing"
- "Database connections must use connection pool"
- "API responses include timestamp and request_id"

❌ Bad:
- "Passwords" (too vague)
- "This is how we handle database connections and everything related to databases" (too long)
- "Thing about APIs" (not descriptive)

### Writing Good Content

✅ Good:
- Clear, concise explanation
- Includes the "why" not just "what"
- Provides enough detail to apply the knowledge

❌ Bad:
- Just restating the title
- Too verbose or includes irrelevant details
- Missing the rationale

### Choosing Priority

Ask yourself:
- **Critical**: Would ignoring this cause security issues, data loss, or production failures?
- **High**: Would ignoring this cause bugs, poor performance, or violate team standards?
- **Medium**: Would ignoring this make code harder to maintain or less optimal?
- **Low**: Is this just nice to know or historical context?

### When to Create New Entry vs Update Existing

**Create new entry** when:
- The knowledge is distinct and separate
- Different context or use case
- Different priority level

**Update existing entry** when:
- Adding examples to existing knowledge
- Clarifying existing content
- Updating outdated information

## Example: Complete Entry

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "category": "gotcha",
  "priority": "critical",
  "title": "Redis client must handle connection failures",
  "content": "Redis connections can fail intermittently in production. The client must implement exponential backoff retry logic and circuit breaker pattern to handle connection failures gracefully. Without this, the application will crash on Redis unavailability.",
  "context": "When initializing Redis client or any external service connection",
  "examples": [
    "redisClient.on('error', handleError)",
    "Use ioredis with retry_strategy option",
    "Implement circuit breaker with state: closed, open, half-open"
  ],
  "learned_from": "2025-11-19_session_003",
  "created": "2025-11-19T14:30:00Z",
  "last_used": "2025-11-19T15:45:00Z",
  "use_count": 3,
  "tags": ["redis", "error-handling", "resilience", "circuit-breaker"]
}
```

---

**Schema Version**: 1.0
**Last Updated**: 2025-11-19
