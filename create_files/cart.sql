-- cart.sql
CREATE TABLE IF NOT EXISTS cart (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
