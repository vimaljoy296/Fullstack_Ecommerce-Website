-- drop table customers;

CREATE TABLE customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    phone_number TEXT,
    street_address TEXT,
    city TEXT,
    state TEXT
);