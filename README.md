# dev-workflow

A production-ready Python project that orchestrates a multi-agent workflow for Jira‑driven feature and bugfix execution using CrewAI.

## Overview
- Pulls Jira issues (key, JQL, queue) via Jira API or service abstraction
- Analyzes tickets and generates structured documentation artifacts
- Sequential agent handoffs: intake → analysis → design → implementation → QA → PR
- Enforces QA approval before PR creation
- Uses GitHub CLI for PR operations

## Project Structure
```
src/
  dev_workflow/
    __init__.py
    main.py
config/
agents/
tasks/
flows/
services/
tests/
artifacts/
docs/
.env.example
pyproject.toml
README.md
```

## Quickstart
```bash
# Install dependencies
python -m pip install -e ".[dev]"

# Run a ticket processing (dry‑run)
python -m dev_workflow.main dry-run --ticket ABC-123
```