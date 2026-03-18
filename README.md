# Software Engineering Practices

A hands-on reference repository for improving software engineering skills, covering **SOLID principles**, **Unit & Integration Testing** with Pytest, and **CI/CD** with GitHub Actions — all in Python.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [SOLID Principles](#solid-principles)
  - [S — Single Responsibility Principle (SRP)](#s--single-responsibility-principle-srp)
  - [O — Open/Closed Principle (OCP)](#o--openclosed-principle-ocp)
  - [L — Liskov Substitution Principle (LSP)](#l--liskov-substitution-principle-lsp)
  - [I — Interface Segregation Principle (ISP)](#i--interface-segregation-principle-isp)
  - [D — Dependency Inversion Principle (DIP)](#d--dependency-inversion-principle-dip)
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
| SOLID Principles | Python (OOP) |
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
├── solid/
│   ├── srp.py                  # Single Responsibility Principle
│   ├── ocp.py                  # Open/Closed Principle
│   ├── lsp.py                  # Liskov Substitution Principle
│   ├── isp.py                  # Interface Segregation Principle
│   └── dip.py                  # Dependency Inversion Principle
├── tests/
│   ├── unit/
│   │   └── test_solid.py       # Unit tests for SOLID examples
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

## SOLID Principles

SOLID is an acronym for five object-oriented design principles that make software easier to maintain, extend, and understand.

---

### S — Single Responsibility Principle (SRP)

> *A class should have only one reason to change.*

Each class handles one well-defined responsibility. If a class manages both business logic and data persistence, any change to one concern risks breaking the other.

```python
# ❌ Violates SRP — handles both order logic and report generation
class Order:
    def calculate_total(self): ...
    def generate_invoice_pdf(self): ...

# ✅ Respects SRP — responsibilities are separated
class Order:
    def calculate_total(self): ...

class InvoiceGenerator:
    def generate_pdf(self, order: Order): ...
```

---

### O — Open/Closed Principle (OCP)

> *Software entities should be open for extension but closed for modification.*

New behaviour is added by extending (e.g., subclassing or composing), not by editing existing code.

```python
from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def apply(self, price: float) -> float: ...

class NoDiscount(Discount):
    def apply(self, price: float) -> float:
        return price

class PercentageDiscount(Discount):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, price: float) -> float:
        return price * (1 - self.percent / 100)

# Adding a new discount type requires no changes to existing classes
class SeasonalDiscount(Discount):
    def apply(self, price: float) -> float:
        return price * 0.85
```

---

### L — Liskov Substitution Principle (LSP)

> *Subtypes must be substitutable for their base types without altering the correctness of the program.*

A derived class should honor the contract of the base class — it must not throw unexpected exceptions or weaken preconditions.

```python
class Bird:
    def move(self) -> str:
        return "moving"

class Sparrow(Bird):
    def move(self) -> str:
        return "flying"   # ✅ valid substitution

# ❌ Violates LSP — Penguin cannot fly, breaking callers that expect Bird.move()
class Penguin(Bird):
    def move(self) -> str:
        raise NotImplementedError("Penguins cannot fly")

# ✅ Redesign using more specific abstractions
class WalkingBird(Bird):
    def move(self) -> str:
        return "walking"

class Penguin(WalkingBird):
    pass
```

---

### I — Interface Segregation Principle (ISP)

> *Clients should not be forced to depend on interfaces they do not use.*

Prefer many small, focused interfaces over one large general-purpose one.

```python
from abc import ABC, abstractmethod

# ❌ Fat interface forces all implementors to provide every method
class Worker(ABC):
    @abstractmethod
    def work(self): ...
    @abstractmethod
    def eat(self): ...

# ✅ Segregated interfaces — each class implements only what it needs
class Workable(ABC):
    @abstractmethod
    def work(self): ...

class Eatable(ABC):
    @abstractmethod
    def eat(self): ...

class HumanWorker(Workable, Eatable):
    def work(self): return "working"
    def eat(self):  return "eating"

class RobotWorker(Workable):
    def work(self): return "working"
```

---

### D — Dependency Inversion Principle (DIP)

> *High-level modules should not depend on low-level modules. Both should depend on abstractions.*

Inject dependencies rather than instantiating them inside a class, making components independently testable and replaceable.

```python
from abc import ABC, abstractmethod

class MessageSender(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

class EmailSender(MessageSender):
    def send(self, message: str) -> None:
        print(f"Sending email: {message}")

class SMSSender(MessageSender):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")

# NotificationService depends on the abstraction, not a concrete implementation
class NotificationService:
    def __init__(self, sender: MessageSender):
        self._sender = sender

    def notify(self, message: str) -> None:
        self._sender.send(message)

# Swap implementations without touching NotificationService
service = NotificationService(EmailSender())
service.notify("Hello!")
```

---

## Testing

### Unit Tests

Unit tests verify individual functions or classes in **isolation**. External dependencies (databases, APIs, file systems) are replaced with mocks or fakes.

```python
# tests/unit/test_solid.py
from unittest.mock import MagicMock
from solid.dip import NotificationService

def test_notification_service_calls_sender():
    mock_sender = MagicMock()
    service = NotificationService(mock_sender)
    service.notify("test message")
    mock_sender.send.assert_called_once_with("test message")
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
from solid.ocp import PercentageDiscount, Order

def test_order_with_discount_integration():
    order = Order(total=100.0)
    discount = PercentageDiscount(10)
    final_price = discount.apply(order.total)
    assert final_price == 90.0
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

- [SOLID Principles — Wikipedia](https://en.wikipedia.org/wiki/SOLID)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python `unittest.mock`](https://docs.python.org/3/library/unittest.mock.html)

