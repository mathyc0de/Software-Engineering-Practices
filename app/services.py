"""Core service functions for testing practice."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import uuid


@dataclass(frozen=True, slots=True)
class Order:
    """Simple order model used by service functions."""

    id: str
    amount: float
    tax_rate: float
    total: float
    created_at: str


def calculate_total(amount: float, tax_rate: float) -> float:
    """Calculate total value with tax.

    Args:
        amount: Base amount before tax.
        tax_rate: Tax percentage in decimal form (e.g. 0.1 for 10%).
    """
    if amount < 0:
        raise ValueError("amount must be greater than or equal to zero")
    if tax_rate < 0:
        raise ValueError("tax_rate must be greater than or equal to zero")

    return round(amount * (1 + tax_rate), 2)


def create_order(amount: float, tax_rate: float = 0.1) -> dict[str, str | float]:
    """Create an order payload with generated metadata."""
    total = calculate_total(amount, tax_rate)
    order = Order(
        id=str(uuid.uuid4()),
        amount=amount,
        tax_rate=tax_rate,
        total=total,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    return asdict(order)


def save_order_to_db(order: dict[str, str | float], db_path: str | Path = "orders.json") -> dict[str, str | float]:
    """Persist the order in a JSON file and return the same order."""
    file_path = Path(db_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.exists():
        raw_content = file_path.read_text(encoding="utf-8").strip()
        orders = json.loads(raw_content) if raw_content else []
    else:
        orders = []

    orders.append(order)
    file_path.write_text(json.dumps(orders, indent=2), encoding="utf-8")
    return order


def list_orders(db_path: str | Path = "orders.json") -> list[dict[str, str | float]]:
    """Read all persisted orders from the JSON file."""
    file_path = Path(db_path)
    if not file_path.exists():
        return []

    raw_content = file_path.read_text(encoding="utf-8").strip()
    return json.loads(raw_content) if raw_content else []
