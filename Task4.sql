-- Register User
INSERT INTO customer (first_name,last_name, email, password) 
VALUES ('Vimal' , 'Joy', 'vimal@example.com', 'hashed_password');

-- Sign in
SELECT * 
FROM customer 
WHERE email = 'vimal@example.com' 
  AND password = 'hashed_password';


-- User Profile
SELECT first_name,last_name, email
FROM Customer 
WHERE customer_id = 1;

-- Product Details 
SELECT * 
FROM Products 
WHERE product_id = 101;

-- Product Search
SELECT * 
FROM Products
WHERE product_name LIKE '%keyword%' 
   OR description LIKE '%keyword%';

-- Add to cart

-- Ensure a cart exists for the customer
INSERT OR IGNORE INTO Cart (customer_id) 
VALUES (1);

-- Add the product to the cart
INSERT INTO cart_items (cart_id, product_id, quantity) 
VALUES (1, 101, 2);


-- View Cart
SELECT p.product_name, p.price, ci.quantity 
FROM cart_items ci 
JOIN products p ON ci.product_id = p.product_id 
WHERE ci.cart_id = (SELECT cart_id FROM Cart WHERE customer_id = 1);

-- Place order
-- Insert into Order table
INSERT INTO order (customer_id, order_date, total_amount) 
VALUES (1,
        (SELECT SUM(p.price * ci.quantity) 
         FROM cart_items ci 
         JOIN product p ON ci.product_id = p.product_id 
         WHERE ci.cart_id = (SELECT cart_id FROM Cart WHERE customer_id = 1)));

-- Retrieve the order_id
SELECT last_insert_rowid() AS order_id;

-- Transfer items from Cart_items to Order_items
INSERT INTO order_items (order_id, product_id, quantity) 
SELECT (SELECT order_id FROM Order WHERE order_id = last_insert_rowid()), product_id, quantity 
FROM Cart_items 
WHERE cart_id = (SELECT cart_id FROM Cart WHERE customer_id = 1);

-- Clear the user's cart
DELETE FROM cart_items 
WHERE cart_id = (SELECT cart_id FROM Cart WHERE customer_id = 1);

-- View Homepage
SELECT product_id, product_name,price
FROM Products
LIMIT 10;


-- Product Listing 
SELECT product_id, product_name, price
FROM Products 
WHERE category_id = 2 
LIMIT 20;

