# AI Prompting Rules and Coding Standards

## Purpose
This document defines coding standards, safety constraints, and testing requirements that AI agents must follow when generating code for RuleGuard.

## Coding Standards

### Python Style (Backend)

1. **PEP 8 Compliance**
   - Use 4 spaces for indentation
   - Maximum line length: 100 characters
   - Two blank lines between top-level functions/classes
   - One blank line between methods

2. **Type Hints**
   - **REQUIRED** for all function parameters and return values
   - Use `Optional[T]` for nullable values
   - Use `List[T]`, `Dict[K, V]` for collections
   
   ```python
   def evaluate_request(request_data: dict, rules: List[Rule]) -> Optional[Rule]:
       """Evaluate request against rules."""
       pass
   ```

3. **Docstrings**
   - **REQUIRED** for all public functions and classes
   - Use triple quotes `"""`
   - Include purpose, parameters, and return value
   
   ```python
   def create_decision(request: Request, rule: Optional[Rule]) -> Decision:
       """
       Create a decision based on request and matching rule.
       
       Args:
           request: The request being evaluated
           rule: Matching rule, or None if no match
       
       Returns:
           Decision object with outcome and explanation
       """
       pass
   ```

4. **Naming Conventions**
   - Classes: `PascalCase` (e.g., `RuleEngine`, `DecisionService`)
   - Functions/variables: `snake_case` (e.g., `evaluate_request`, `rule_id`)
   - Constants: `UPPER_SNAKE_CASE` (e.g., `OPERATORS`, `API_BASE_URL`)
   - Private methods: `_leading_underscore` (e.g., `_matches_rule`)

### TypeScript/React Style (Frontend)

1. **TypeScript Strict Mode**
   - Enable strict type checking
   - No `any` types unless absolutely necessary
   - Define interfaces for all data structures

2. **Component Structure**
   - Use functional components with hooks
   - Props interface defined above component
   - Export at bottom of file
   
   ```typescript
   interface RequestFormProps {
       onSubmit: (data: Request) => void;
   }
   
   export function RequestForm({ onSubmit }: RequestFormProps) {
       // Component logic
   }
   ```

3. **Naming Conventions**
   - Components: `PascalCase` (e.g., `RequestForm`, `DecisionResult`)
   - Functions/variables: `camelCase` (e.g., `handleSubmit`, `isLoading`)
   - Constants: `UPPER_SNAKE_CASE` (e.g., `API_BASE_URL`)
   - Types/Interfaces: `PascalCase` (e.g., `Request`, `Decision`)

## Safety Constraints

### 1. No Dynamic Code Execution

**NEVER generate code that uses:**
- `eval()`
- `exec()`
- `compile()`
- `__import__()`
- `globals()` or `locals()` for execution

**Why:** Security vulnerabilities, unpredictable behavior

### 2. Mandatory Input Validation

**ALWAYS validate input through:**
- Marshmallow schemas (backend)
- TypeScript types (frontend)
- Database constraints

**Example:**
```python
# CORRECT - validate before processing
schema = RequestSchema()
validated_data = schema.load(request_data)  # Raises error if invalid

# INCORRECT - direct database insertion
db.session.add(Request(**request_data))  # No validation!
```

### 3. Safe Database Operations

**ALWAYS:**
- Use SQLAlchemy ORM (parameterized queries)
- Validate data through schemas before insertion
- Handle database errors gracefully

**NEVER:**
- Use raw SQL with string formatting
- Trust user input in queries
- Ignore database errors

### 4. Error Handling

**ALWAYS:**
- Catch specific exceptions
- Return user-friendly error messages
- Log errors for debugging

**Example:**
```python
try:
    decision = DecisionService.create_decision(request)
except ValidationError as e:
    return jsonify({'error': 'Invalid input', 'details': e.messages}), 400
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return jsonify({'error': 'Internal server error'}), 500
```

## Testing Requirements

### 1. Unit Tests

**REQUIRED for:**
- All business logic (services)
- All validation schemas
- All API endpoints

**Test Structure:**
```python
class TestRuleEngine:
    def test_amount_greater_than(self):
        """Test that amount > value rule works correctly."""
        # Arrange
        rule = Rule(field='amount', operator='>', value='1000', ...)
        request_data = {'amount': 1500, 'category': 'travel'}
        
        # Act
        result = RuleEngine.evaluate_request(request_data, [rule])
        
        # Assert
        assert result is not None
        assert result.id == rule.id
```

### 2. Test Coverage

**MUST test:**
- Happy path (valid input, expected output)
- Edge cases (boundary values, empty inputs)
- Error cases (invalid input, missing data)
- Integration (multiple components working together)

### 3. Test Documentation

**Each test must have:**
- Descriptive name (`test_amount_greater_than_matches_rule`)
- Docstring explaining what it tests
- Clear arrange-act-assert structure

## Code Review Checklist

Before submitting AI-generated code, verify:

### Security
- [ ] No `eval()`, `exec()`, or dynamic code execution
- [ ] All user input validated
- [ ] No SQL injection vulnerabilities
- [ ] No sensitive data in logs or errors

### Correctness
- [ ] Logic matches requirements
- [ ] Edge cases handled
- [ ] Error cases handled
- [ ] Tests pass

### Code Quality
- [ ] Follows naming conventions
- [ ] Has type hints (Python) or types (TypeScript)
- [ ] Has docstrings/comments
- [ ] No code duplication
- [ ] Simple and readable

### Testing
- [ ] Unit tests written
- [ ] Tests cover happy path
- [ ] Tests cover edge cases
- [ ] Tests cover error cases
- [ ] All tests pass

### Documentation
- [ ] Docstrings updated
- [ ] README updated if needed
- [ ] API documentation updated if needed

## Specific Constraints for RuleGuard

### Rule Engine
- **MUST** use predefined operator mapping
- **MUST** evaluate rules in priority order
- **MUST** return first matching rule only
- **NEVER** use dynamic code execution

### Decision Service
- **MUST** validate request through schema first
- **MUST** generate clear explanations
- **MUST** persist decisions to database
- **MUST** handle "no matching rule" case

### API Routes
- **MUST** validate input through schemas
- **MUST** return appropriate HTTP status codes
- **MUST** return JSON responses
- **MUST** handle errors gracefully

### Frontend
- **MUST** validate input before submission
- **MUST** handle loading states
- **MUST** handle error states
- **MUST** use TypeScript types

## Example Prompts for AI

### Good Prompt:
```
Create a new API endpoint to get all decisions for a request.
Requirements:
- Validate request_id is a positive integer
- Return 404 if request not found
- Return decisions ordered by created_at descending
- Include tests for happy path and error cases
- Follow existing code style in api/request_routes.py
```

### Bad Prompt:
```
Add a feature to evaluate rules dynamically
```
(Too vague, might lead to `eval()` usage)

## Enforcement

These rules are **mandatory**. Code that violates them should be:
1. Rejected during review
2. Fixed before merging
3. Used as learning for future prompts

## Summary

AI-generated code must be:
- **Safe** (no security vulnerabilities)
- **Correct** (works as intended)
- **Tested** (has comprehensive tests)
- **Documented** (has clear documentation)
- **Maintainable** (follows coding standards)

Human review is the final checkpoint to ensure these standards are met.
