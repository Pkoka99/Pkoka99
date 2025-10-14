# Build & Test

- Build: `pip install -e .`
- Test: `pytest`

# Run Locally

- `uvicorn app.main:app --reload`

# Conventions

- Config via Pydantic settings (`settings.py`)
- CELERY tasks live in `tasks/`
