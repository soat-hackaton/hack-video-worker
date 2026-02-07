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
	PYTHONPATH=. pytest --cov=. --cov-report=xml --cov-report=term-missing

test-coverage:
	pytest --cov=. --cov-report html
