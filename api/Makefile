dc_dev = docker compose --env-file .env.dev -f docker-compose.dev.yml
dc_prod = docker compose --env-file .env.prod -f docker-compose.prod.yml
dc_exec_dev = ${dc_dev} exec ${OPTIONS}
dc_exec_prod= ${dc_prod} exec ${OPTIONS}

.SILENT:

CONTAINER ?= app
SHELL_CMD ?= bash
OPTIONS ?= -u root

# Docker
run-dev:
	${dc_dev} up -d --build

run-prod:
	${dc_prod} up -d --build

build-dev:
	${dc_dev} build --no-cache

build-prod:
	${dc_prod} build --no-cache

stop-dev:
	${dc_dev} stop

stop-prod:
	${dc_prod} stop

down-dev:
	${dc_dev} down

down-prod:
	${dc_prod} down

logs-dev:
	${dc_dev} logs -f $(CONTAINER)

logs-prod:
	${dc_prod} logs -f $(CONTAINER)

logs-all-dev:
	${dc_dev} logs -f

logs-all-prod:
	${dc_prod} logs -f

restart-dev:
	$(dc_dev) restart $(CONTAINER)

restart-prod:
	$(dc_prod) restart $(CONTAINER)

shell-dev:
	${dc_exec_dev} $(CONTAINER) $(SHELL_CMD)

shell-prod:
	${dc_exec_prod} $(CONTAINER) $(SHELL_CMD)

shell-dev-root:
	$(MAKE) shell-dev OPTIONS="-u root"

shell-prod-root:
	$(MAKE) shell-prod OPTIONS="-u root"

ps-dev:
	${dc_dev} ps

ps-prod:
	${dc_prod} ps

# Migrations
migration-dev:
	$(dc_dev) exec $(OPTIONS) $(CONTAINER) alembic revision --autogenerate -m "$(message)"

migration-dev-upgrade:
	$(dc_dev) exec $(OPTIONS) $(CONTAINER) alembic upgrade head

migration-dev-downgrade:
	$(dc_dev) exec $(OPTIONS) $(CONTAINER) alembic downgrade -1

migration-dev-current:
	$(dc_dev) exec $(OPTIONS) $(CONTAINER) alembic current

migration-dev-history:
	$(dc_dev) exec $(OPTIONS) $(CONTAINER) alembic history

migration-prod:
	$(dc_prod) exec $(OPTIONS) $(CONTAINER) alembic revision --autogenerate -m "$(message)"

migration-prod-upgrade:
	$(dc_prod) exec $(OPTIONS) $(CONTAINER) alembic upgrade head

migration-prod-downgrade:
	$(dc_prod) exec $(OPTIONS) $(CONTAINER) alembic downgrade -1

migration-prod-current:
	$(dc_prod) exec $(OPTIONS) $(CONTAINER) alembic current

migration-prod-history:
	$(dc_prod) exec $(OPTIONS) $(CONTAINER) alembic history

# Requirements
dev-pip-list:
	$(dc_dev) exec $(OPTIONS) $(CONTAINER) pip list

prod-pip-list:
	$(dc_prod) exec $(OPTIONS) $(CONTAINER) pip list