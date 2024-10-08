-- orders.sql
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    status TEXT,
    street_address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
