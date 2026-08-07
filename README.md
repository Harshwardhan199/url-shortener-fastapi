# URL Shortener API

A RESTful URL shortening service built with FastAPI, PostgreSQL, SQLAlchemy, and Docker Compose.


## Features

- Shorten any long URL to a compact, shareable short link
- Redirect short codes to their original URLs (HTTP 307)
- Automatic table creation on startup via SQLAlchemy
- Interactive API documentation via Swagger UI
- Fully containerised with Docker Compose — no manual database setup required
- Environment-based configuration with `pydantic-settings`


## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Framework    | FastAPI                             |
| ORM          | SQLAlchemy 2.x                      |
| Database     | PostgreSQL 17                       |
| Validation   | Pydantic v2 / pydantic-settings     |
| Server       | Uvicorn                             |
| Packaging    | uv / pyproject.toml                 |
| Containers   | Docker & Docker Compose             |


## Project Structure

```
url-shortener-fastapi/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API route handlers
│   ├── config/              # Database engine, session, settings
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business logic
│   └── main.py              # FastAPI application entry point
├── .env.example             # Environment variable template
├── .env.docker              # Environment variables for Docker Compose
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```


## Quick Start (Recommended — Docker Compose)

Docker Compose is the recommended way to run this project. It automatically provisions a PostgreSQL database and starts the application — no manual database creation required.

```bash
docker compose up --build
```

Once running:

| Service     | URL                        |
|-------------|----------------------------|
| API         | http://localhost:8000      |
| Swagger UI  | http://localhost:8000/docs |


## Running Locally with uv

This is an alternative for local development. You must have PostgreSQL running and create the database manually before starting the app.

1. Copy the example environment file and edit it as needed:

   ```bash
   cp .env.example .env
   ```

2. Create the PostgreSQL database:

   ```sql
   CREATE DATABASE url_shortener;
   ```

3. Install dependencies:

   ```bash
   uv sync
   ```

4. Start the development server:

   ```bash
   uv run uvicorn app.main:app --reload
   ```


## Running Locally without uv (pip)

This is another alternative if you prefer plain pip over uv.

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv

   # macOS / Linux
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

2. Install the project:

   ```bash
   pip install -e .
   ```

3. Start the development server:

   ```bash
   uvicorn app.main:app --reload
   ```

> **Note:** You still need to create the PostgreSQL database manually (see step 2 in the uv section above) and configure your `.env` file before running.

## Environment Variables

Copy `.env.example` to `.env` and update the values for your environment.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/url_shortener
BASE_URL=http://localhost:8000
```

| Variable       | Description                                                            |
|----------------|------------------------------------------------------------------------|
| `DATABASE_URL` | Full PostgreSQL connection string used by SQLAlchemy                   |
| `BASE_URL`     | Public base URL of the service, prepended to short codes in responses  |


## API Endpoints

### `POST /shorten` — Create a short URL

**Request**

```http
POST /shorten
Content-Type: application/json

{
  "original_url": "https://www.example.com/some/very/long/path?with=query&params=true"
}
```

**Response** `201 Created`

```json
{
  "original_url": "https://www.example.com/some/very/long/path?with=query&params=true",
  "short_code": "a1b2c3",
  "short_url": "http://localhost:8000/a1b2c3"
}
```

---

### `GET /{short_code}` — Redirect to original URL

**Request**

```http
GET /a1b2c3
```

**Response** `307 Temporary Redirect`

```
Location: https://www.example.com/some/very/long/path?with=query&params=true
```

Returns `404 Not Found` if the short code does not exist.


## API Documentation

Interactive Swagger UI is available at:

**http://localhost:8000/docs**


## Design Decisions

### Layered Architecture

The codebase is organised into distinct layers — `api`, `services`, `models`, `schemas`, and `config` — keeping routing, business logic, and persistence cleanly separated and independently testable.

### SQLAlchemy ORM

SQLAlchemy 2.x is used for database access. Tables are created automatically at startup via `Base.metadata.create_all`, so no manual migration step is needed for local development.

### Environment-Based Configuration

All configuration (database URL, base URL) is loaded from environment variables using `pydantic-settings`. The `.env.example` file documents every required variable, and a separate `.env.docker` file is provided for Docker Compose to avoid overwriting local settings.

### Docker Compose as the Recommended Deployment Method

Docker Compose orchestrates both the API and PostgreSQL services. The `api` service waits for the `postgres` service to pass a health check before starting, ensuring reliable cold starts with a single command and no manual setup.

### Separation of Routing, Business Logic, and Persistence

- **`api/routes.py`** handles HTTP concerns only (parsing requests, returning responses, raising HTTP exceptions).
- **`services/`** contains all business logic (short-code generation, look-up).
- **`models/`** defines the database schema via SQLAlchemy ORM models.
- **`schemas/`** defines Pydantic models for input validation and response serialisation.
