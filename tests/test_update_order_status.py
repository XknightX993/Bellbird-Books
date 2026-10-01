import pytest

from app import app
from database.database import get_connection


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def clear_database():
    connection = get_connection()

    connection.execute("DELETE FROM orders")
    connection.execute("DELETE FROM customers")

    connection.commit()
    connection.close()


def test_update_order_status(client):
    clear_database()

    connection = get_connection()

    # Create a customer
    connection.execute(
        """
        INSERT INTO customers
        (name, phone, contact_preference)
        VALUES (?, ?, ?)
        """,
        ("John Smith", "0400123456", "Text"),
    )

    customer_id = connection.execute("SELECT last_insert_rowid()").fetchone()[0]

    # Create an order
    cursor = connection.execute(
        """
        INSERT INTO orders
        (
            customer_id,
            title,
            author,
            quantity,
            deposit,
            order_date,
            arrival_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            customer_id,
            "The Hobbit",
            "J.R.R. Tolkien",
            1,
            10,
            "2026-10-01",
            "",
        ),
    )

    order_id = cursor.lastrowid

    connection.commit()
    connection.close()

    # Update order status
    response = client.post(
        f"/orders/status/{order_id}",
        data={
            "status": "Arrived",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/orders")

    # Check the database
    connection = get_connection()

    order = connection.execute(
        "SELECT * FROM orders WHERE id = ?",
        (order_id,),
    ).fetchone()

    connection.close()

    assert order is not None
    assert order["status"] == "Arrived"


def test_update_order_status_order_not_found(client):
    clear_database()

    response = client.post(
        "/orders/status/99999",
        data={
            "status": "Arrived",
        },
    )

    assert response.status_code == 200
    assert b"Order not found." in response.data
