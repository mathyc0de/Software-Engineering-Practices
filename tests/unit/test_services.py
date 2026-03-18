import pytest

from app.services import calculate_total, create_order


def test_calculate_total_with_tax():
    assert calculate_total(100.0, 0.1) == 110.0


def test_calculate_total_rounds_to_two_decimal_places():
    assert calculate_total(99.99, 0.0875) == 108.74


def test_calculate_total_rejects_negative_amount():
    with pytest.raises(ValueError, match="amount"):
        calculate_total(-1.0, 0.1)


def test_calculate_total_rejects_negative_tax_rate():
    with pytest.raises(ValueError, match="tax_rate"):
        calculate_total(100.0, -0.1)


def test_create_order_contains_required_fields():
    order = create_order(amount=100.0, tax_rate=0.1)
    assert set(order.keys()) == {"id", "amount", "tax_rate", "total", "created_at"}
    assert order["amount"] == 100.0
    assert order["tax_rate"] == 0.1
    assert order["total"] == 110.0
    assert isinstance(order["id"], str) and order["id"]
    assert isinstance(order["created_at"], str) and order["created_at"]
