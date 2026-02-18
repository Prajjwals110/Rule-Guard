# RuleGuard

A rule-based request decision system built for technical assessment. Clean, well-structured, and easy to modify.

## Overview

RuleGuard evaluates requests (e.g., expense requests) against stored rules and returns decisions:
- **APPROVED** - Request meets approval criteria
- **REJECTED** - Request violates rejection criteria  
- **NEEDS_REVIEW** - No rule matches, manual review required

Every decision includes a clear explanation of why it was made.

## Architecture

### Core Principles

1. **Rules as Data** - Rules are stored in the database, not hardcoded
2. **Deterministic Evaluation** - Rules evaluated by priority (ascending order)
3. **First Match Wins** - First matching rule determines the outcome
4. **Safe Execution** - No `eval()` or `exec()`, uses safe operator mapping
5. **Schema Validation** - All input validated before processing

### Backend Structure

```
backend/
├── app.py                 # Flask application entry point
├── config.py              # Configuration settings
├── database.py            # Database initialization
├── models/                # SQLAlchemy models
│   ├── request.py         # Request model
│   ├── rule.py            # Rule model
│   └── decision.py        # Decision model
├── schemas/               # Marshmallow validation schemas
│   ├── request_schema.py
│   ├── rule_schema.py
│   └── decision_schema.py
├── services/              # Business logic layer
│   ├── rule_engine.py     # Core rule evaluation logic
│   └── decision_service.py # Decision orchestration
├── api/                   # API routes
│   ├── request_routes.py  # Request endpoints
│   └── rule_routes.py     # Rule management endpoints
└── tests/                 # Automated tests
    ├── test_rules.py
    ├── test_decisions.py
    └── test_invalid_states.py
```

### Frontend Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.ts      # Backend API client
│   ├── types/             # TypeScript interfaces
│   │   ├── Request.ts
│   │   ├── Decision.ts
│   │   └── Rule.ts
│   ├── components/        # React components
│   │   ├── RequestForm.tsx
│   │   ├── DecisionResult.tsx
│   │   └── RuleList.tsx
│   ├── pages/             # Page components
│   │   ├── SubmitRequest.tsx
│   │   └── ManageRules.tsx
│   └── App.tsx            # Main application
```

## Tech Stack

**Backend:**
- Python 3.x
- Flask (API framework)
- SQLAlchemy (ORM)
- Marshmallow (validation)
- SQLite (database)
- pytest (testing)

**Frontend:**
- React 18
- TypeScript
- Vite (build tool)

## Setup and Installation

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Backend will start on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will start on `http://localhost:5173`

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

Tests cover:
- Rule evaluation with all operators (<, <=, >, ==)
- Priority-based rule ordering
- Decision generation and persistence
- Invalid input rejection
- Edge cases (adding rules, no matching rules)

## API Endpoints

### Requests

- `POST /api/requests` - Submit new request
  ```json
  {
    "amount": 1500.00,
    "category": "travel",
    "description": "Conference trip"
  }
  ```

- `GET /api/requests` - List all requests
- `GET /api/requests/:id` - Get specific request with decision

### Rules

- `POST /api/rules` - Create new rule
  ```json
  {
    "field": "amount",
    "operator": ">",
    "value": "1000",
    "decision": "REVIEW",
    "priority": 1
  }
  ```

- `GET /api/rules` - List all rules (ordered by priority)
- `DELETE /api/rules/:id` - Delete rule

## Key Technical Decisions

### 1. Rules as Data, Not Code

**Decision:** Store rules in database instead of hardcoding logic.

**Rationale:** 
- Rules can be added/modified without code changes
- Non-developers can manage rules
- Easier to audit and track changes
- Safer than dynamic code execution

**Tradeoff:** Slightly more complex than simple if/else, but much more flexible.

### 2. Safe Operator Evaluation

**Decision:** Use dictionary mapping instead of `eval()`.

```python
OPERATORS = {
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    '>': lambda a, b: a > b,
    '==': lambda a, b: a == b,
}
```

**Rationale:**
- No security risks from code injection
- Predictable behavior
- Easy to test

**Tradeoff:** Limited to predefined operators, but that's a feature not a bug.

### 3. Priority-Based Evaluation

**Decision:** Evaluate rules in ascending priority order (0 = highest).

**Rationale:**
- Deterministic outcomes
- Clear precedence rules
- Easy to reason about
- Prevents rule conflicts

**Tradeoff:** Requires careful priority management, but makes behavior predictable.

### 4. Schema Validation

**Decision:** Use Marshmallow for all input validation.

**Rationale:**
- Centralized validation logic
- Clear error messages
- Type coercion
- Reusable schemas

**Tradeoff:** Extra dependency, but worth it for robustness.

### 5. No Authentication

**Decision:** No authentication system implemented.

**Rationale:**
- Keeps focus on core functionality
- Simpler for technical assessment
- Easier to test and demo

**Limitation:** Not production-ready. Would need auth before real deployment.

## Limitations and Future Improvements

### Current Limitations

1. **No Authentication** - Anyone can access all endpoints
2. **No Audit Trail** - Rule changes aren't tracked
3. **Limited Operators** - Only <, <=, >, == supported
4. **Single Database** - SQLite not suitable for high concurrency
5. **No Caching** - Rules fetched from DB on every request

### Potential Improvements

1. **Authentication & Authorization**
   - Add user accounts
   - Role-based access control
   - API keys for programmatic access

2. **Enhanced Rule Engine**
   - Support for AND/OR conditions
   - Date/time-based rules
   - Regular expressions for string matching
   - Rule versioning and rollback

3. **Audit & Compliance**
   - Track all rule changes
   - Log all decisions
   - Export audit reports

4. **Performance**
   - Cache rules in memory
   - Use PostgreSQL for production
   - Add database indexes
   - Implement rate limiting

5. **UI Enhancements**
   - Rule testing interface
   - Decision history view
   - Analytics dashboard
   - Bulk rule import/export

## Project Structure Rationale

### Separation of Concerns

- **Models** - Data structure only
- **Schemas** - Validation logic
- **Services** - Business logic
- **API** - HTTP handling
- **Tests** - Verification

This separation makes the code:
- Easy to test (mock dependencies)
- Easy to modify (change one layer without affecting others)
- Easy to understand (clear responsibilities)

### Why No Router Library?

Frontend uses simple state-based navigation instead of React Router.

**Rationale:**
- Only 2 pages
- Simpler to understand
- Fewer dependencies
- Easier to test

**Tradeoff:** Would need proper routing for larger apps.

## Development Workflow

1. **Add Feature**
   - Update models if needed
   - Add/update schemas
   - Implement in services
   - Create API endpoints
   - Write tests
   - Update frontend

2. **Run Tests**
   ```bash
   cd backend
   python -m pytest tests/ -v
   ```

3. **Manual Testing**
   - Start backend: `python app.py`
   - Start frontend: `npm run dev`
   - Test in browser

## License

This is a technical assessment project.

## Author

Built as a demonstration of clean architecture and test-driven development practices.

***********