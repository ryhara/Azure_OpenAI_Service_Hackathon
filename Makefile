usage :
	@echo "\033[31mUsage: make clean → write .env → make all → . venv/bin/activate → make run\033[0m"

all : env init

env:
	cp .env.example .env

init:
	python3 -m venv venv
	. ./venv/bin/activate; pip install -r requirements.txt

run :
	flask run

clean :
	rm -rf .env
	rm -rf venv
	rm -rf __pycache__

pylint :
	-pylint --rcfile ./pylintrc ./**/*.py

pycodestyle :
	-pycodestyle --config=./pycodestyle ./**/*.py

.PHONY: usage all env init run clean pylint pycodestyle