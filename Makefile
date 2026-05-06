.PHONY: up down logs migrate seed dev-backend dev-frontend

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f backend

migrate:
	cd backend && USE_SQLITE=1 ./.venv/bin/python manage.py migrate

seed:
	cd backend && USE_SQLITE=1 ./.venv/bin/python manage.py seed_demo

dev-backend:
	cd backend && USE_SQLITE=1 python manage.py runserver

dev-frontend:
	cd frontend && npm run dev
