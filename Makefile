# TODO : exe 消す
exe :
	@echo "Hello World"

all : venv run

venv:
	python3 -m venv venv
	venv/bin/activate
	pip install Flask

run :
	flask run

stop :
	deactivate