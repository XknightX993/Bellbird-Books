CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    deposit REAL DEFAULT 0,
    order_date TEXT NOT NULL,
    arrival_date TEXT,
    status TEXT NOT NULL DEFAULT 'Unfulfilled'
);