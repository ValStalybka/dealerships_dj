DIR_DOCKER = $(abspath $(DIR_REPO)/docker)
PYTHON := python
MANAGEMENT := $(PYTHON) -m management


.PHONY: run
run:
	pipenv run python3 src/manage.py runserver localhost:8001


.PHONY: migrations
migrations:
	pipenv run python3 src/manage.py makemigrations


.PHONY: migrate
migrate:
	pipenv run python3 src/manage.py migrate

.PHONY: su
su:
	pipenv run python src/manage.py createsuperuser


.PHONY: clean-docker
clean-docker:
	docker compose stop || true
	docker compose down || true
	docker compose rm --force || true
	docker system prune --force


.PHONY: superuser
superuser:
	pipenv run python src/manage.py createsuperuserwithpassword \
        --username admin \
        --password admin \
        --email admin@gmail.com \
        --preserve


.PHONY: loaddata
loaddata:
	pipenv run python src/manage.py loaddata fixtures/data.json


.PHONY: test
test:
	pipenv run python src/manage.py test applications.blog --verbosity 2


.PHONY: docker
docker:
	docker compose build


.PHONY: docker-run
docker-run: docker
	docker compose up