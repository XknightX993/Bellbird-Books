CREATE TABLE IF NOT EXISTS new_stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT,
    quantity INTEGER NOT NULL DEFAULT 0,
    cost REAL,
    price REAL,
    location TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    contact_preference TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    deposit REAL DEFAULT 0,
    order_date TEXT NOT NULL,
    arrival_date TEXT,
    status TEXT NOT NULL DEFAULT 'Unfulfilled',
    notified INTEGER NOT NULL DEFAULT 0,
    collected INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);