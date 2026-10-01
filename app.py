from flask import Flask, render_template, request, redirect, url_for
from database.database import get_connection

app = Flask(__name__)


# =========================================================
# HOME
# =========================================================


@app.route("/")
def home():
    connection = get_connection()

    new_stock_count = connection.execute("SELECT COUNT(*) FROM new_stock").fetchone()[0]

    second_hand_count = connection.execute(
        "SELECT COUNT(*) FROM second_hand_stock"
    ).fetchone()[0]

    order_count = connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0]

    outstanding_orders = connection.execute(
        """
        SELECT COUNT(*)
        FROM orders
        WHERE status != 'Collected'
        AND status != 'Cancelled'
        """
    ).fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        new_stock_count=new_stock_count,
        second_hand_count=second_hand_count,
        order_count=order_count,
        outstanding_orders=outstanding_orders,
    )


# =========================================================
# NEW STOCK - ADD
# =========================================================


@app.route("/stock/add", methods=["GET", "POST"])
def add_stock():

    if request.method == "GET":
        return render_template("add_stock.html")

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

    return redirect(url_for("search_stock", keyword=title))


# =========================================================
# NEW STOCK - SEARCH
# =========================================================


@app.route("/stock/search")
def search_stock():

    keyword = request.args.get("keyword", "").strip()

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            title,
            author,
            isbn,
            quantity,
            cost,
            price,
            location
        FROM new_stock
        WHERE title LIKE ?
        OR author LIKE ?
        ORDER BY title
        """,
        (f"%{keyword}%", f"%{keyword}%"),
    ).fetchall()

    connection.close()

    return render_template("search_stock.html", stocks=rows, keyword=keyword)


# =========================================================
# NEW STOCK - EDIT
# =========================================================


@app.route("/stock/edit/<int:stock_id>", methods=["GET", "POST"])
def edit_stock(stock_id):

    connection = get_connection()

    if request.method == "POST":
        title = request.form["title"].strip()
        author = request.form["author"].strip()
        isbn = request.form["isbn"].strip()
        quantity = request.form["quantity"]
        cost = request.form["cost"]
        price = request.form["price"]
        location = request.form["location"].strip()

        if not title or not author or not location:
            connection.close()
            return "Title, Author and Location are required."

        connection.execute(
            """
            UPDATE new_stock
            SET
                title = ?,
                author = ?,
                isbn = ?,
                quantity = ?,
                cost = ?,
                price = ?,
                location = ?
            WHERE id = ?
            """,
            (title, author, isbn, quantity, cost, price, location, stock_id),
        )

        connection.commit()
        connection.close()

        return redirect(url_for("search_stock", keyword=title))

    stock = connection.execute(
        """
        SELECT *
        FROM new_stock
        WHERE id = ?
        """,
        (stock_id,),
    ).fetchone()

    connection.close()

    if stock is None:
        return "Stock record not found."

    return render_template("edit_stock.html", stock=stock)


# =========================================================
# NEW STOCK - DELETE
# =========================================================


@app.route("/stock/delete/<int:stock_id>", methods=["POST"])
def delete_stock(stock_id):

    connection = get_connection()

    connection.execute(
        """
        DELETE FROM new_stock
        WHERE id = ?
        """,
        (stock_id,),
    )

    connection.commit()
    connection.close()

    return redirect(url_for("search_stock"))


# =========================================================
# SECOND-HAND STOCK - LIST / SEARCH
# =========================================================


@app.route("/second-hand")
def second_hand():

    keyword = request.args.get("keyword", "").strip()

    connection = get_connection()

    if keyword:
        stocks = connection.execute(
            """
            SELECT *
            FROM second_hand_stock
            WHERE title LIKE ?
            OR author LIKE ?
            OR location LIKE ?
            OR condition LIKE ?
            ORDER BY id DESC
            """,
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        ).fetchall()

    else:
        stocks = connection.execute(
            """
            SELECT *
            FROM second_hand_stock
            ORDER BY id DESC
            """
        ).fetchall()

    connection.close()

    return render_template("second_hand.html", stocks=stocks, keyword=keyword)


# =========================================================
# SECOND-HAND STOCK - ADD
# =========================================================


@app.route("/second-hand/add", methods=["GET", "POST"])
def add_second_hand():

    if request.method == "GET":
        return render_template("add_second_hand.html")

    title = request.form["title"].strip()
    author = request.form["author"].strip()
    condition = request.form["condition"]
    source = request.form["source"].strip()
    cost = request.form["cost"]
    price = request.form["price"]
    location = request.form["location"].strip()
    notes = request.form["notes"].strip()

    if not title or not author or not condition or not location:
        return "Title, Author, Condition and Location are required."

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO second_hand_stock
        (
            title,
            author,
            condition,
            source,
            cost,
            price,
            location,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (title, author, condition, source, cost, price, location, notes),
    )

    connection.commit()
    connection.close()

    return redirect(url_for("second_hand"))


# =========================================================
# SECOND-HAND STOCK - EDIT
# =========================================================


@app.route("/second-hand/edit/<int:stock_id>", methods=["GET", "POST"])
def edit_second_hand(stock_id):

    connection = get_connection()

    if request.method == "POST":
        title = request.form["title"].strip()
        author = request.form["author"].strip()
        condition = request.form["condition"]
        source = request.form["source"].strip()
        cost = request.form["cost"]
        price = request.form["price"]
        location = request.form["location"].strip()
        notes = request.form["notes"].strip()

        if not title or not author or not condition or not location:
            connection.close()
            return "Title, Author, Condition and Location are required."

        connection.execute(
            """
            UPDATE second_hand_stock
            SET
                title = ?,
                author = ?,
                condition = ?,
                source = ?,
                cost = ?,
                price = ?,
                location = ?,
                notes = ?
            WHERE id = ?
            """,
            (title, author, condition, source, cost, price, location, notes, stock_id),
        )

        connection.commit()
        connection.close()

        return redirect(url_for("second_hand"))

    stock = connection.execute(
        """
        SELECT *
        FROM second_hand_stock
        WHERE id = ?
        """,
        (stock_id,),
    ).fetchone()

    connection.close()

    if stock is None:
        return "Second-hand stock record not found."

    return render_template("edit_second_hand.html", stock=stock)


# =========================================================
# SECOND-HAND STOCK - DELETE
# =========================================================


@app.route("/second-hand/delete/<int:stock_id>", methods=["POST"])
def delete_second_hand(stock_id):

    connection = get_connection()

    connection.execute(
        """
        DELETE FROM second_hand_stock
        WHERE id = ?
        """,
        (stock_id,),
    )

    connection.commit()
    connection.close()

    return redirect(url_for("second_hand"))


# =========================================================
# CUSTOMER ORDER - ADD
# =========================================================


@app.route("/orders/add", methods=["GET", "POST"])
def add_order():

    if request.method == "GET":
        return render_template("add_order.html")

    name = request.form["name"].strip()
    phone = request.form["phone"].strip()
    contact_preference = request.form["contact_preference"]

    title = request.form["title"].strip()
    author = request.form["author"].strip()
    quantity = request.form["quantity"]
    deposit = request.form["deposit"]
    order_date = request.form["order_date"]
    arrival_date = request.form["arrival_date"]

    if not name or not phone or not title or not author or not order_date:
        return "Customer name, phone, title, author and order date are required."

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO customers
        (
            name,
            phone,
            contact_preference
        )
        VALUES (?, ?, ?)
        """,
        (name, phone, contact_preference),
    )

    customer_id = connection.execute("SELECT last_insert_rowid()").fetchone()[0]

    connection.execute(
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
        (customer_id, title, author, quantity, deposit, order_date, arrival_date),
    )

    connection.commit()
    connection.close()

    return redirect(url_for("view_orders"))


# =========================================================
# CUSTOMER ORDER - UPDATE STATUS
# =========================================================


@app.route("/orders/status/<int:order_id>", methods=["POST"])
def update_order_status(order_id):

    status = request.form["status"].strip()

    allowed_statuses = ["Ordered", "Arrived", "Notified", "Collected", "Cancelled"]

    if status not in allowed_statuses:
        return "Invalid order status."

    connection = get_connection()

    order = connection.execute(
        """
        SELECT *
        FROM orders
        WHERE id = ?
        """,
        (order_id,),
    ).fetchone()

    if order is None:
        connection.close()
        return "Order not found."

    connection.execute(
        """
        UPDATE orders
        SET status = ?
        WHERE id = ?
        """,
        (status, order_id),
    )

    connection.commit()
    connection.close()

    return redirect(url_for("view_orders"))


# =========================================================
# CUSTOMER ORDERS - VIEW / SEARCH
# =========================================================


@app.route("/orders")
def view_orders():
    keyword = request.args.get("keyword", "").strip()
    status_filter = request.args.get("status", "").strip()

    connection = get_connection()

    query = """
        SELECT
            orders.id,
            customers.name,
            customers.phone,
            customers.contact_preference,
            orders.title,
            orders.author,
            orders.quantity,
            orders.deposit,
            orders.order_date,
            orders.arrival_date,
            orders.status
        FROM orders
        JOIN customers
        ON orders.customer_id = customers.id
        WHERE 1 = 1
    """

    parameters = []

    if keyword:
        query += """
            AND (
                customers.name LIKE ?
                OR orders.title LIKE ?
            )
        """

        parameters.extend(
            [
                f"%{keyword}%",
                f"%{keyword}%",
            ]
        )

    if status_filter:
        query += " AND orders.status = ?"
        parameters.append(status_filter)

    query += " ORDER BY orders.id DESC"

    orders = connection.execute(
        query,
        parameters,
    ).fetchall()

    connection.close()

    return render_template(
        "orders.html",
        orders=orders,
        keyword=keyword,
        status_filter=status_filter,
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
