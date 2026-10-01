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
    connection.execute("DELETE FROM new_stock")
    connection.commit()
    connection.close()


def test_add_new_stock(client):
    clear_database()

    response = client.post(
        "/stock/add",
        data={
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "isbn": "9780261102217",
            "quantity": "5",
            "cost": "10",
            "price": "20",
            "location": "Front Shelf A",
        },
    )

    assert response.status_code == 302

    connection = get_connection()
    row = connection.execute(
        "SELECT * FROM new_stock WHERE title = ?", ("The Hobbit",)
    ).fetchone()
    connection.close()

    assert row is not None
    assert row["author"] == "J.R.R. Tolkien"
    assert row["quantity"] == 5
    assert row["location"] == "Front Shelf A"


def test_add_stock_without_title(client):
    clear_database()

    response = client.post(
        "/stock/add",
        data={
            "title": "",
            "author": "J.R.R. Tolkien",
            "isbn": "9780261102217",
            "quantity": "5",
            "cost": "10",
            "price": "20",
            "location": "Front Shelf A",
        },
    )

    assert response.status_code == 200
    assert b"Title, Author and Location are required." in response.data

    connection = get_connection()
    rows = connection.execute("SELECT * FROM new_stock").fetchall()
    connection.close()

    assert len(rows) == 0
