from flask import Flask, render_template, request, redirect, url_for
from database.database import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/stock/add", methods=["GET", "POST"])
def add_stock():
    if request.method == "POST":
        title = request.form["title"].strip()
        author = request.form["author"].strip()
        isbn = request.form["isbn"].strip()
        quantity = request.form["quantity"]
        cost = request.form["cost"]
        price = request.form["price"]
        location = request.form["location"].strip()

        if not title or not author or not location:
            return "Title, Author and Location are required."

        connection = get_connection()

        connection.execute(
            """
            INSERT INTO new_stock
            (title, author, isbn, quantity, cost, price, location)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (title, author, isbn, quantity, cost, price, location),
        )

        connection.commit()
        connection.close()

        return "Stock added successfully."

    return render_template("add_stock.html")


if __name__ == "__main__":
    app.run(debug=True)
