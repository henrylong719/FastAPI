# Issue Tracker API

Production-ready CRUD API for issue tracking, built with FastAPI.

## Project Structure

```
├── app/
│   ├── main.py            # App factory & startup
│   ├── config.py          # Settings via pydantic-settings
│   ├── exceptions.py      # Global exception handlers
│   ├── security.py        # JWT auth, password hashing, dependencies
│   ├── storage.py         # JSON file persistence
│   ├── schemas/
│   │   ├── auth.py        # Token, User, UserInDB models
│   │   └── issues.py      # IssueCreate, IssueUpdate, IssueOut models
│   ├── middleware/
│   │   └── timer.py       # X-Process-Time header
│   └── routes/
│       ├── auth.py        # POST /api/v1/auth/token
│       ├── health.py      # GET /health
│       └── issues.py      # CRUD /api/v1/issues (protected)
├── tests/
│   ├── conftest.py        # Fixtures (isolated data, auth header)
│   └── test_issues.py     # API tests
├── pyproject.toml         # Deps, ruff, pytest config
└── .env.example           # Environment variable template
```

## Setup

```bash
# Install dependencies (requires uv)
uv sync --group dev

# Copy and configure environment
cp .env.example .env
```

Set `SECRET_KEY` in `.env` to a securely generated random string:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Running

```bash
# Development
fastapi dev app/main.py

# Production
fastapi run app/main.py
```

## Testing

```bash
uv run pytest
```

## Authentication

The API uses **JWT Bearer tokens** (OAuth2 password flow).

**1. Get a token:**

```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -d "username=johndoe&password=secret"
```

**2. Use the token:**

```bash
curl http://localhost:8000/api/v1/issues/ \
  -H "Authorization: Bearer <access_token>"
```

All `/api/v1/issues/*` endpoints require a valid token. The `/health` and `/api/v1/auth/token` endpoints are public.

## API Endpoints

| Method   | Path                        | Auth | Description         |
|----------|-----------------------------|------|---------------------|
| `GET`    | `/health`                   |      | Health check        |
| `POST`   | `/api/v1/auth/token`        |      | Login, get JWT      |
| `GET`    | `/api/v1/issues/`           | ✓    | List all issues     |
| `POST`   | `/api/v1/issues/`           | ✓    | Create an issue     |
| `GET`    | `/api/v1/issues/{id}`       | ✓    | Get issue by ID     |
| `PUT`    | `/api/v1/issues/{id}`       | ✓    | Update an issue     |
| `DELETE` | `/api/v1/issues/{id}`       | ✓    | Delete an issue     |

Interactive docs available at `/docs` (Swagger UI — supports login) and `/redoc`.
