dev:
	docker compose up -d --build

migrate:
	docker compose run --rm api alembic upgrade head

seed:
	docker compose run --rm api python -m app.seeds

test:
	docker compose run --rm api pytest
	docker compose run --rm web npm test
