from pathlib import Path

from app.services import create_order, list_orders, save_order_to_db


def test_order_creation_and_persistence(tmp_path: Path):
    db_file = tmp_path / "orders.json"

    order = create_order(amount=100.0, tax_rate=0.1)
    saved_order = save_order_to_db(order, db_path=db_file)
    all_orders = list_orders(db_path=db_file)

    assert saved_order["amount"] == 100.0
    assert saved_order["total"] == 110.0
    assert db_file.exists()
    assert len(all_orders) == 1
    assert all_orders[0]["id"] == order["id"]


def test_persistence_appends_multiple_orders(tmp_path: Path):
    db_file = tmp_path / "orders.json"

    first = create_order(amount=50.0, tax_rate=0.1)
    second = create_order(amount=75.0, tax_rate=0.2)

    save_order_to_db(first, db_path=db_file)
    save_order_to_db(second, db_path=db_file)

    all_orders = list_orders(db_path=db_file)
    assert len(all_orders) == 2
    assert all_orders[0]["id"] == first["id"]
    assert all_orders[1]["id"] == second["id"]


def test_list_orders_returns_empty_when_file_does_not_exist(tmp_path: Path):
    db_file = tmp_path / "missing-orders.json"
    assert list_orders(db_path=db_file) == []
