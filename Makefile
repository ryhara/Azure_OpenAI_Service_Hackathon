DOCKER_COMPOSE_YML = ./docker-compose.yml

usage :
	@echo "Usage [common]: make env → write .env(SEACRET_KEY, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)"
	@echo "\033[34mUsage [docker]: make build → make up → (make ps, make log) → make down\033[0m"
#	@echo "\033[31mUsage [venv]  : make init → . venv/bin/activate → make run → deactivate\033[0m"

env:
	cp .env.example .env

# init:
# 	python3 -m venv venv
# 	. ./venv/bin/activate; pip install -r ./docs/requirements.txt

# run :
# 	flask run
# 	@echo "\n====================================="
# 	@echo "access to http://localhost:5001"
# 	@echo "====================================="

# routes :
# 	flask routes

clean :
	rm -rf .env
	rm -rf venv
	rm -rf ./flask_app/__pycache__
	rm -rf ./flask_app/views/__pycache__

pylint :
	find . -name "*.py" | xargs pylint --rcfile ./linter/pylintrc

pycodestyle :
	find . -name "*.py" | xargs pycodestyle --config=./linter/pycodestyle

all : build up

build :
	docker compose -f $(DOCKER_COMPOSE_YML) build --no-cache

up :
	docker compose -f $(DOCKER_COMPOSE_YML) up -d
	@echo "\n====================================="
	@echo "access to http://localhost:5001"
	@echo "====================================="

stop :
	docker compose -f $(DOCKER_COMPOSE_YML) stop

down :
	docker compose -f $(DOCKER_COMPOSE_YML) down
	docker image rm -f flask:my
	docker volume rm -f flask

ps :
	docker container ls -a
	@echo "----------------------------------------"
	docker image ls -a
	@echo "----------------------------------------"
	docker volume ls
	@echo "----------------------------------------"
	docker network ls

log:
	docker logs flask

docker-rm:
	docker image rm -f flask:my
	docker volume rm -f flask
	docker network rm -f flask-network

bash:
	docker exec -it flask bash

.PHONY: usage all env init run clean pylint pycodestyle build up stop down ps docker-rm bash log