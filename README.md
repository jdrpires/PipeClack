# Clack Project Control

Monorepo with FastAPI backend and React frontend.

## Setup

Requirements: Docker and Docker Compose.

To bring up the full stack with the database migrated and seeded, run:

```
docker-compose up --build
```

This builds and starts every service. During startup, the `api-migrate` service
executes `alembic upgrade head` so all database migrations are applied before
the API container begins serving requests.

To apply migrations manually without bringing up the full stack, run:

```
docker compose run --rm api alembic upgrade head
```
This is the same command executed by the `make migrate` shortcut shown below.

```
make dev       # build and run containers
make migrate   # run alembic migrations
make seed      # populate initial data
make test      # run API and Web tests
```

API available at http://localhost:8000, Web at http://localhost:5173.

## Environment

- DB_URL (api)
- JWT_SECRET (api)
- CORS_ORIGINS (api)
- UPLOAD_DIR (api)

## Test Users

- admin@clack.com / Admin@123 (ADMIN)
- sales@clack.com / Sales@123 (COMMERCIAL)
- po@clack.com / Po@123 (PO)
- dev@clack.com / Dev@123 (DEV)
- qa@clack.com / Qa@123 (QA)

## Structure

```
/api
  /alembic
  /app
    /core
    /models
    /schemas
    /routes
    /tests
/web
  /src
    /pages
    /components
    /stores
    /tests
/postman
```
