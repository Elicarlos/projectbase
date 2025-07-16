# Atalhos para comandos mais usados

run:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate

makemigrations:
	poetry run python manage.py makemigrations

createsuperuser:
	poetry run python manage.py createsuperuser

lint:
	poetry run ruff .
	poetry run black --check .

format:
	poetry run black .
	poetry run ruff --fix .

test:
	poetry run pytest

precommit:
	poetry run pre-commit run --all-files

shell:
	@poetry env info --path
	@echo "Ative o venv acima para rodar comandos manualmente"

# No Windows, use: make <alvo> (com Git Bash, MSYS2 ou WSL)
