.PHONY: dev backend frontend test docker stop

dev:
	docker compose up -d postgres redis
	cd backend && uvicorn app.main:app --reload --port 8000 &
	cd frontend && npm run dev

backend:
	cd backend && uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest -v

docker:
	docker compose up --build

stop:
	docker compose down
