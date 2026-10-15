# Bellbird Books

A Flask and SQLite prototype for a bookshop's new stock, second-hand copies, and customer special orders.

## Features

- Add, search, edit, and delete new-stock records.
- Track second-hand books as individual copies, including condition, source, cost, price, and shelf location.
- Record customer orders and search by customer name or book title.
- Update an order through Ordered, Arrived, Notified, Collected, or Cancelled.
- Manage data locally with SQLite.

## Development iterations

For the project presentation, the merged GitHub work is grouped into two product increments. This grouping summarizes the existing pull requests; it does not rewrite the original branch or pull-request history and does not represent GitHub Releases or tags.

| Iteration | Product increment | Merged GitHub work |
| --- | --- | --- |
| Iteration 1 | Inventory foundation: SQLite schema, new-stock entry and validation, title/author search, and stock editing. | PR #1–#4, merged 30 September 2026 |
| Iteration 2 | Customer orders: customer/order records, order creation, and order-status updates. | PR #5–#6, merged 30 September–1 October 2026 |

The repository retains the feature branches and six merged pull requests as the detailed change history. Teammate review screenshots can be added to the presentation after the group captures them from its GitHub workspace.

## Run locally

Requirements: Python 3.9 or later.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m database.init_db
python app.py
```

Open http://127.0.0.1:5000 in a browser. The local SQLite database is stored in `database/bellbird.db`.

## Project structure

- `app.py`: Flask routes and application entry point
- `database/schema.sql`: SQLite tables
- `templates/`: Jinja pages
- `static/style.css`: page styling
- `tests/`: automated feature tests

## Project boundary

This coursework prototype is intended for local use. The project plan lists public online sales, payment processing, supplier integrations, accounting integrations, and automated customer messaging outside the planned scope.
