# Software Engineering Practices

A hands-on reference repository for improving software engineering skills, focused on **Unit & Integration Testing** with Pytest and **CI/CD** with GitHub Actions — all in Python.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Testing](#testing)
  - [Unit Tests](#unit-tests)
  - [Integration Tests](#integration-tests)
  - [Running Tests](#running-tests)
- [CI/CD with GitHub Actions](#cicd-with-github-actions)
- [References](#references)

---

## Overview

This repository is a practical playground to study and apply essential software engineering practices:

| Practice | Tool / Approach |
|---|---|
| Unit Tests | Pytest |
| Integration Tests | Pytest |
| CI/CD Pipeline | GitHub Actions |

Each topic is organized in its own directory with focused examples and corresponding tests.

---

## Project Structure

```
Software-Engineering-Practices/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline
├── app/
│   └── services.py             # Example application logic
├── tests/
│   ├── unit/
│   │   └── test_services.py    # Unit tests
│   └── integration/
│       └── test_integration.py # Integration tests
├── requirements.txt
└── README.md
```

---

## Setup

**Prerequisites:** Python 3.10+

```bash
# Clone the repository
git clone https://github.com/mathyc0de/Software-Engineering-Practices.git
cd Software-Engineering-Practices

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

`requirements.txt` example:

```
pytest
pytest-cov
```

---

## Testing

### Unit Tests

Unit tests verify individual functions or classes in **isolation**. External dependencies (databases, APIs, file systems) are replaced with mocks or fakes.

```python
# tests/unit/test_services.py
from app.services import calculate_total

def test_calculate_total_with_tax():
    assert calculate_total(100.0, 0.1) == 110.0
```

Key characteristics:
- **Fast** — no I/O, no network calls
- **Isolated** — one unit under test
- **Deterministic** — same input always yields the same output

---

### Integration Tests

Integration tests verify that multiple components work correctly **together** — e.g., a service interacting with a real database or another module.

```python
# tests/integration/test_integration.py
from app.services import create_order, save_order_to_db

def test_order_creation_and_persistence():
    order = create_order(amount=100.0)
    saved_order = save_order_to_db(order)
    assert saved_order["amount"] == 100.0
```

Key characteristics:
- **Slower** than unit tests — may involve real dependencies
- **Broader scope** — tests component interactions
- **Useful for catching contract mismatches** between modules

---

### Running Tests

```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run with verbose output
pytest -v
```

---

## CI/CD with GitHub Actions

The pipeline defined in `.github/workflows/ci.yml` automatically runs on every push and pull request to the `main` branch.

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests with coverage
        run: pytest --cov=. --cov-report=term-missing
```

### Pipeline stages

| Stage | Description |
|---|---|
| **Checkout** | Fetches the source code |
| **Setup Python** | Installs the specified Python version |
| **Install dependencies** | Installs packages from `requirements.txt` |
| **Run tests** | Executes the full test suite and shows coverage |

Every green pipeline run confirms that the codebase is in a working state before merging.

---

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
