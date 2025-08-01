# Project Agents Guide for OpenAI Codex

This file describes how AI agents should work with this repository.

## Project Overview

`email-agent` is a Python project that uses **LangGraph** and **LangChain** to
classify and summarize Gmail messages. The repository contains several modules
that define nodes, tools and prompt templates for the agent workflow.

## Repository Layout

- `nodes/` – LangGraph nodes (e.g., `classifier.py`, `summarizer.py`,
  `authenticator.py`)
- `tools/` – Gmail integration tools (`get_emails.py`, `add_to_label.py`,
  `gmail_authenticate.py`)
- `prompts/` – Prompt templates for the agents
- `utils/` – Helper utilities (`auth.py`, `print.py`)
- `graph.py` – Builds the LangGraph workflow
- `state.py` – Defines the graph state object
- `run_graph.py` – CLI entry point to run the graph for one or more users
- `.github/workflows/` – GitHub Actions workflow for scheduled runs
- `requirements.txt` – Python dependencies

## Coding Conventions

- Target **Python 3.11** or newer
- Follow **PEP 8** style guidelines
- Include **type hints** and short docstrings for all public functions
- Keep functions small and focused; prefer composition over large monolithic
  functions
- When editing prompts, keep them inside triple quoted strings

## Testing Guidelines

- Place tests under a top‑level `tests/` directory (create it if it does not
  exist)
- Use **pytest** for all test cases
- Run the full test suite with:

  ```bash
  pytest
  ```

- To run with coverage:

  ```bash
  pytest --cov
  ```

## Programmatic Checks

Before opening a pull request, run the following commands locally:

```bash

# Lint code
ruff .
ruff format
```

All code should be formatted and pass **Ruff** linting.

## Pull Request Requirements

1. Provide a clear description of the changes
2. Reference any related issues if applicable
3. Ensure programmatic checks and tests pass
4. Keep PRs focused on a single concern
5. Include screenshots if the change affects output formatting or user
   interaction
