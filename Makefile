PYFILES=app tests

# Dependencies
shell:
	poetry shell

# Formatting
lint:
	ruff check --fix $(PYFILES)

format:
	ruff format $(PYFILES)

check:
	ruff check $(PYFILES)
	ruff format --check $(PYFILES)

scan:
	bandit -r . -lll # Show 3 lines of context
	safety check

# Docker
up:
	docker-compose -f ./docker-compose.yml build
	docker-compose -f ./docker-compose.yml up -d --force-recreate

down:
	docker-compose -f ./docker-compose.yml down --remove-orphans

integration: down up
	docker-compose -f ./docker-compose.yml up --exit-code-from integration_tests integration_tests

# Testing
unit:
	set -a; . ./dev.env; pytest -vv tests/unit/

int:
	./wait-for.sh http://service_name:8000/healthz pytest -vv tests/integration --capture=tee-sys --asyncio-mode=auto

# Git Hooks
pre-commit: check scan unit