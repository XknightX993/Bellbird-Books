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