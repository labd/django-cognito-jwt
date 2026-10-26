.PHONY: install format lint test retest coverage docs release


install:
	uv sync --all-groups

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

lint:
	uv run ruff format --check src tests
	uv run ruff check src tests

test:
	uv run pytest

retest:
	uv run pytest -vvv --lf

coverage:
	uv run pytest --cov=django_cognito_jwt --cov-report=term-missing --cov-report=html

docs:
	uv run --group docs $(MAKE) -C docs html

release:
	rm -rf dist/*
	uv build
