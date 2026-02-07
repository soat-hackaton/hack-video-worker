install:
	pipenv install

start:
	python main.py

black:
	black . --line-length 79

flake8:
	flake8 .

isort:
	isort .

test:
	pytest --cov=.

test-coverage:
	pytest --cov=. --cov-report html
