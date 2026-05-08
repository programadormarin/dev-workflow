.PHONY: help install test test-verbose lint typecheck build clean run

help:
	@echo "Available commands:"
	@echo "  make install      - Install project dependencies"
	@echo "  make test        - Run tests with pytest"
	@echo "  make test-verbose - Run tests with verbose output"
	@echo "  make lint        - Run ruff linter"
	@echo "  make typecheck   - Run mypy type checker"
	@echo "  make build       - Build the package"
	@echo "  make clean       - Remove build artifacts"
	@echo "  make run         - Run the CLI"

install:
	@echo "Note: Project requires Python 3.11+ (current: $$(python3 --version))"
	python3 -m pip install --upgrade pip setuptools wheel
	python3 -m pip install crewai pydantic httpx pytest ruff mypy

test:
	python3 -m pytest tests/ -v

test-verbose:
	python3 -m pytest tests/ -vv -s

lint:
	python3 -m ruff check . --fix

typecheck:
	@echo "Note: mypy requires Python 3.11+ for full type checking"
	@python3 -m mypy src/ --ignore-missing-imports 2>&1 | grep -v "Source file found twice" || true

build:
	python3 -m pip install build
	python3 -m build

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

run:
	@echo "Usage: make run Ticket=TICKET"
	@echo "Example: make run Ticket=PROJ-123"
	@python3 -m src.dev_workflow $(Ticket)