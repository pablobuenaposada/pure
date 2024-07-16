DOCKER_IMAGE=pure

venv:
	poetry install --without dev

venv-dev:
	poetry install

format: venv-dev
	poetry run black src
	poetry run ruff check src --fix

format/check: venv-dev
	poetry run black --verbose src --check
	poetry run ruff check src

migrations/check:
	poetry run python src/manage.py makemigrations --check --dry-run

tests: venv-dev
	PYTHONPATH=src poetry run pytest src/tests

docker/build:
	docker build --no-cache	--tag=$(DOCKER_IMAGE) .

docker/format/check:
	 docker run $(DOCKER_IMAGE) /bin/sh -c 'make format/check'

docker/migrations/check:
	 docker run --env-file .env.local $(DOCKER_IMAGE) /bin/sh -c 'make migrations/check'

docker/tests:
	 docker compose up -d --force-recreate db django
	 docker exec pure-django-1 make tests

docker/run:
	docker compose -f docker-compose.yml up --force-recreate -d --build

docker/create-fake-chats:
	 docker exec pure-django-1 python src/manage.py create_fake_chats --total=$(total)