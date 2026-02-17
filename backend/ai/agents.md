# AI Agent Capabilities and Constraints

## Purpose
This document defines what AI agents can and cannot do when working on the RuleGuard codebase. It ensures system integrity while leveraging AI for productivity.

## AI Agent Capabilities

### ✅ Allowed Operations

1. **Code Generation**
   - Generate boilerplate code (models, schemas, routes)
   - Create unit tests
   - Write documentation and docstrings
   - Implement standard CRUD operations

2. **Data Operations**
   - Create seed data
   - Generate test fixtures
   - Write database migrations

3. **Analysis and Suggestions**
   - Code review and improvements
   - Performance optimization suggestions
   - Security vulnerability identification
   - Best practice recommendations

## AI Agent Restrictions

### ❌ Forbidden Operations

1. **Dynamic Code Execution**
   - **NEVER** use `eval()` or `exec()`
   - **NEVER** use `compile()` for user input
   - **NEVER** execute arbitrary code strings
   - **WHY**: Security risk, unpredictable behavior

2. **Bypassing Validation**
   - **NEVER** skip schema validation
   - **NEVER** directly insert unvalidated data into database
   - **NEVER** trust user input without validation
   - **WHY**: Data integrity, security

3. **Production Deployment**
   - **NEVER** deploy code without human review
   - **NEVER** modify production database directly
   - **NEVER** change configuration without approval
   - **WHY**: Risk management, accountability

4. **Breaking Changes Without Review**
   - **NEVER** modify core business logic without human review
   - **NEVER** change API contracts without discussion
   - **NEVER** alter database schema without migration plan
   - **WHY**: System stability, backward compatibility

## AI Agent Role Definition

**Think of AI as a Junior Developer:**
- Can write code, but needs review
- Can suggest improvements, but needs approval
- Can identify issues, but needs guidance on fixes
- Should ask questions when uncertain

## Critical Code Sections (Require Human Review)

1. **Rule Evaluation Logic** (`services/rule_engine.py`)
   - Core business logic
   - Must be deterministic
   - Security-sensitive

2. **Decision Generation** (`services/decision_service.py`)
   - Orchestrates critical flow
   - Affects all requests
   - Must be correct

3. **Validation Schemas** (`schemas/`)
   - Guards system integrity
   - Prevents invalid states
   - Must be comprehensive

4. **Database Models** (`models/`)
   - Defines data structure
   - Changes affect entire system
   - Must maintain relationships

## AI Workflow

### For New Features:
1. AI generates initial implementation
2. **Human reviews** for correctness
3. AI generates tests
4. **Human verifies** test coverage
5. AI updates documentation
6. **Human approves** before merge

### For Bug Fixes:
1. AI identifies issue
2. **Human confirms** root cause
3. AI suggests fix
4. **Human reviews** fix
5. AI adds regression test
6. **Human verifies** test

### For Refactoring:
1. AI suggests improvement
2. **Human evaluates** tradeoffs
3. AI implements change
4. **Human ensures** tests still pass
5. AI updates documentation

## Safety Constraints

### Input Validation
- **ALWAYS** validate user input through schemas
- **ALWAYS** sanitize data before database operations
- **ALWAYS** use parameterized queries (SQLAlchemy handles this)

### Error Handling
- **ALWAYS** return user-friendly error messages
- **NEVER** expose internal system details in errors
- **ALWAYS** log errors for debugging

### Testing
- **ALWAYS** write tests for new code
- **ALWAYS** ensure existing tests pass
- **NEVER** commit code that breaks tests

## Example: Safe vs Unsafe Code

### ❌ UNSAFE (DO NOT GENERATE):
```python
# NEVER DO THIS - eval is dangerous
def evaluate_rule(rule_string):
    return eval(rule_string)  # Security vulnerability!
```

### ✅ SAFE (CORRECT APPROACH):
```python
# Use predefined operator mapping
OPERATORS = {
    '>': lambda a, b: a > b,
    '<': lambda a, b: a < b,
}

def evaluate_rule(field_value, operator, rule_value):
    op_func = OPERATORS.get(operator)
    if not op_func:
        raise ValueError(f"Invalid operator: {operator}")
    return op_func(field_value, rule_value)
```

## Review Checklist

Before accepting AI-generated code, verify:

- [ ] No `eval()`, `exec()`, or `compile()` usage
- [ ] All input validated through schemas
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Follows project coding standards
- [ ] Error handling implemented
- [ ] No breaking changes to API

## Escalation

**When to involve a human immediately:**
- Security concerns
- Architectural decisions
- Breaking changes
- Production issues
- Unclear requirements
- Test failures

## Summary

AI is a powerful tool for productivity, but **human oversight is essential** for:
- System integrity
- Security
- Correctness
- Maintainability

This document ensures AI enhances development without compromising quality.
