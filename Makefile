up:
	docker compose -f docker-compose-local.yaml up -d

down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force

logs:
	docker compose -f docker-compose-local.yaml logs -f

logs-web:
	docker compose -f docker-compose-local.yaml logs -f web

logs-db:
	docker compose -f docker-compose-local.yaml logs -f db

logs-bot:
	docker compose -f docker-compose-local.yaml logs -f bot