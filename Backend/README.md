# Arinar Backend

FastAPI service powering the Arinar LLM Council platform.

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI + Uvicorn |
| Data validation | Pydantic v2 |
| Database | PostgreSQL 16 + pgvector (via SQLAlchemy async) |
| Caching / pub-sub | Redis |
| Workflow engine | Temporal (Python SDK) |
| Model access | OpenRouter (via `model_gateway` service) |
| Auth | WorkOS / JWT |
| Observability | OpenTelemetry + Sentry |

## Project Structure

```
app/
  main.py           FastAPI app entry point
  config.py         Pydantic v2 BaseSettings (all env vars)
  api/v1/           Route handlers (one file per domain)
  services/         All business logic lives here
  workers/          Temporal activity/workflow workers
  models/           SQLAlchemy ORM models
  schemas/          Pydantic v2 request/response schemas
  db/               Database session and engine setup
tests/
  unit/             Unit tests for service logic
  integration/      API + DB integration tests
```

## Local Development

```bash
# 1. Copy env template
cp .env.example .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start backing services (Postgres, Redis, Temporal)
docker compose -f ../infra/docker/docker-compose.yml up -d

# 4. Run the API
uvicorn app.main:app --reload --port 8000
```

## Running Tests

```bash
pytest tests/ -v
```

## Key Engineering Rules

- No business logic in route files — all logic belongs in `services/`.
- No direct DB writes from outside `services/` or `workers/`.
- All env vars must be declared in `config.py` and documented in `.env.example`.
- File size limits: routes ≤ 500 lines, services ≤ 400 lines, UI components ≤ 300 lines.
- Naming: `<domain>_routes.py`, `<domain>_service.py`, `test_<domain>_service.py`.

See `../15-engineering-standards-and-anti-chaos-rules.md` for full standards.
