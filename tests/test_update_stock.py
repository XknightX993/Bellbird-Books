import pytest

from app import app
from database.database import get_connection


def clear_database():
    connection = get_connection()
    connection.execute("DELETE FROM new_stock")
    connection.commit()
    connection.close()


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_update_new_stock(client):
    clear_database()

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO new_stock
        (title, author, isbn, quantity, cost, price, location)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "The Hobbit",
            "J.R.R. Tolkien",
            "9780261102217",
            5,
            10,
            20,
            "Front Shelf A",
        ),
    )

    stock_id = cursor.lastrowid

    connection.commit()
    connection.close()

    response = client.post(
        f"/stock/edit/{stock_id}",
        data={
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "isbn": "9780261102217",
            "quantity": "8",
            "cost": "10",
            "price": "20",
            "location": "Front Shelf B",
        },
    )

    assert response.status_code == 302

    connection = get_connection()

    stock = connection.execute(
        "SELECT * FROM new_stock WHERE id = ?",
        (stock_id,),
    ).fetchone()

    connection.close()

    assert stock["quantity"] == 8
    assert stock["location"] == "Front Shelf B"


def test_update_new_stock_without_required_field(client):
    clear_database()

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO new_stock
        (title, author, isbn, quantity, cost, price, location)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "The Hobbit",
            "J.R.R. Tolkien",
            "9780261102217",
            5,
            10,
            20,
            "Front Shelf A",
        ),
    )

    stock_id = cursor.lastrowid

    connection.commit()
    connection.close()

    response = client.post(
        f"/stock/edit/{stock_id}",
        data={
            "title": "",
            "author": "J.R.R. Tolkien",
            "isbn": "9780261102217",
            "quantity": "8",
            "cost": "10",
            "price": "20",
            "location": "Front Shelf B",
        },
    )

    assert response.status_code == 200
    assert b"Title, Author and Location are required." in response.data
