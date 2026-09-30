import pytest

from app import app
from database.database import get_connection


# Create a Flask test client for automated testing
@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# Clear customer and order data before each test
def clear_database():
    connection = get_connection()

    connection.execute("DELETE FROM orders")
    connection.execute("DELETE FROM customers")

    connection.commit()
    connection.close()


# Test creating a customer order successfully
def test_create_customer_order(client):
    clear_database()

    response = client.post(
        "/orders/add",
        data={
            "name": "John Smith",
            "phone": "0400123456",
            "contact_preference": "Text",
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "quantity": "1",
            "deposit": "10",
            "order_date": "2026-10-01",
            "arrival_date": "",
        },
    )

    assert response.status_code == 200
    assert b"Customer order created successfully." in response.data

    connection = get_connection()

    customer = connection.execute(
        "SELECT * FROM customers WHERE name = ?",
        ("John Smith",),
    ).fetchone()

    order = connection.execute(
        "SELECT * FROM orders WHERE title = ?",
        ("The Hobbit",),
    ).fetchone()

    connection.close()

    assert customer is not None
    assert order is not None
    assert order["quantity"] == 1
    assert order["deposit"] == 10


# Test that required fields are validated
def test_create_customer_order_without_required_field(client):
    clear_database()

    response = client.post(
        "/orders/add",
        data={
            "name": "",
            "phone": "0400123456",
            "contact_preference": "Text",
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "quantity": "1",
            "deposit": "10",
            "order_date": "2026-10-01",
            "arrival_date": "",
        },
    )

    assert response.status_code == 200

    assert (
        b"Customer name, phone, title, author and order date are required."
        in response.data
    )

    connection = get_connection()

    customers = connection.execute("SELECT * FROM customers").fetchall()

    orders = connection.execute("SELECT * FROM orders").fetchall()

    connection.close()

    assert len(customers) == 0
    assert len(orders) == 0
