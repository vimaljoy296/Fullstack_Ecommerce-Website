CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    product_name TEXT NOT NULL,
    description TEXT,
    price REAL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
