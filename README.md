# Movie Management API (FastAPI)

A clean, testable Movie CRUD API using FastAPI + SQLModel (SQLite), with layered architecture (Handler/Service/DAO), validation, pagination, and auto-generated Swagger.

## Tech Stack
- FastAPI (OpenAPI/Swagger auto)
- SQLModel (SQLAlchemy + Pydantic)
- SQLite
- Pytest
- Docker

## Run Locally
```bash
python -m venv .venv
# mac/linux: source .venv/bin/activate
# windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload