from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database helper functions
def execute_query(query, params=()):
    """Execute a SELECT query and return the results."""
    conn = sqlite3.connect('vjbazaar.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def execute_insert(query, params=()):
    """Execute an INSERT/UPDATE query."""
    conn = sqlite3.connect('vjbazaar.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# 1. SIGN UP
@app.route('/sign_up', methods=["POST"])
def sign_up():
    """REGISTER A NEW USER."""
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    # Check if the email is already registered
    existing_user = execute_query("SELECT * FROM customer WHERE email = ?", (email,))
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    # Insert new user data into the customer table
    insert_query = """
    INSERT INTO customer (first_name, last_name, email, password) 
    VALUES (?, ?, ?, ?)
    """
    execute_insert(insert_query, (first_name, last_name, email, password))

    return jsonify({"message": "User registered successfully"}), 201

# 2. HOMEPAGE
@app.route('/homepage')
def homepage():
    """HOMEPAGE CONTENT."""
    homepage_content = {
        "title": "Welcome to VJBazaar",
        "tagline": "Your Ultimate Sports Item Selector",
        "message": "Discover our top-rated sports items selected by our customers!"
    }

    # Query for Top-Rated Products
    query = """
    SELECT p.product_id, p.product_name, p.description, p.price, AVG(r.rating) as avg_rating
    FROM products p
    JOIN reviews r ON p.product_id = r.product_id
    GROUP BY p.product_id, p.product_name, p.description, p.price
    HAVING avg_rating >= 4
    ORDER BY avg_rating DESC
    LIMIT 5
    """
    top_rated_products = execute_query(query)

    homepage_content["top_rated_products"] = [
        {
            "product_id": product[0], 
            "product_name": product[1], 
            "description": product[2], 
            "price": float(product[3]),  # Convert price to float for JSON compatibility
            "average_rating": round(product[4], 1)
        }
        for product in top_rated_products
    ]

    return jsonify(homepage_content), 200

# 3. USER PROFILE
@app.route('/customer/<int:customer_id>', methods=["GET"])
def get_customer_by_id(customer_id):
    """GET A CUSTOMER BY THEIR ID."""
    customer = execute_query("SELECT first_name, last_name, customer_id FROM customer WHERE customer_id = ?", (customer_id,))
    if customer:
        return jsonify({"customer": customer[0]}), 200
    return jsonify({"error": "Customer not found"}), 404

# 4. PRODUCT DETAILS
@app.route('/product/<int:product_id>', methods=["GET"])
def get_product_by_id(product_id):
    """GET A PRODUCT BY ITS ID."""
    product = execute_query("SELECT * FROM products WHERE product_id = ?", (product_id,))
    if product:
        return jsonify({"product": product[0]}), 200
    return jsonify({"error": "Product not found"}), 404

# 5. ALL PRODUCTS
@app.route('/products', methods=["GET"])
def get_all_products():
    """GET ALL PRODUCTS."""
    query = "SELECT product_id, product_name, description, price FROM products"
    products = execute_query(query)

    product_list = [
        {
            "product_id": product[0],
            "product_name": product[1],
            "description": product[2],
            "price": float(product[3])
        }
        for product in products
    ]

    return jsonify({"products": product_list}), 200

# 6. PRODUCT SEARCH
@app.route('/products/search', methods=["GET"])
def search_products():
    """SEARCH FOR PRODUCTS BASED ON QUERY PARAMETERS."""
    product_id = request.args.get('id')
    name = request.args.get('name')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if product_id:
        query += " AND product_id = ?"
        params.append(product_id)
    if name:
        query += " AND product_name LIKE ?"
        params.append(f"%{name}%")
    if min_price:
        query += " AND price >= ?"
        params.append(min_price)
    if max_price:
        query += " AND price <= ?"
        params.append(max_price)

    products = execute_query(query, tuple(params))

    if products:
        return jsonify({
            "status": "success",
            "message": "Products found.",
            "data": products
        }), 200
    else:
        return jsonify({
            "status": "success",
            "message": "No products found matching the criteria."
        }), 404

# 7. ADD TO CART
@app.route('/cart/<customer_id>', methods=["POST"])
def add_to_cart(customer_id):
    """ADD AN ITEM TO THE CART."""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    cart_query = "SELECT cart_id, total_amount FROM cart WHERE customer_id = ?"
    cart = execute_query(cart_query, (customer_id,))

    if not cart:
        insert_cart_query = "INSERT INTO cart (customer_id, total_amount) VALUES (?, 0)"
        execute_insert(insert_cart_query, (customer_id,))
        cart = execute_query(cart_query, (customer_id,))

    cart_id = cart[0][0]

    existing_cart_item = execute_query("SELECT * FROM cart_items WHERE cart_id = ? AND product_id = ?", (cart_id, product_id))

    if existing_cart_item:
        update_query = "UPDATE cart_items SET quantity = quantity + ? WHERE cart_id = ? AND product_id = ?"
        execute_insert(update_query, (quantity, cart_id, product_id))
        message = "Cart item quantity updated successfully."
    else:
        insert_query = "INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (?, ?, ?)"
        execute_insert(insert_query, (cart_id, product_id, quantity))
        message = "Item added to cart successfully."

    product_price_query = "SELECT price FROM products WHERE product_id = ?"
    product_price_result = execute_query(product_price_query, (product_id,))
    
    if not product_price_result:
        return jsonify({"error": "Product not found"}), 404

    product_price = product_price_result[0][0]
    new_total_amount = cart[0][1] + (product_price * quantity)
    update_total_query = "UPDATE cart SET total_amount = ? WHERE cart_id = ?"
    execute_insert(update_total_query, (new_total_amount, cart_id))

    return jsonify({"message": message}), 200

# 8. VIEW CART
@app.route('/cart/<customer_id>', methods=["GET"])
def view_cart(customer_id):
    """VIEW THE CART DETAILS FOR A SPECIFIC CUSTOMER."""
    cart_query = "SELECT cart_id, total_amount FROM cart WHERE customer_id = ?"
    cart = execute_query(cart_query, (customer_id,))

    if not cart:
        return jsonify({"message": "Cart not found for this customer"}), 404

    cart_id = cart[0][0]
    total_amount = cart[0][1]

    cart_items_query = """
    SELECT products.product_id, products.product_name, products.description, 
           products.price, cart_items.quantity
    FROM cart_items
    JOIN products ON cart_items.product_id = products.product_id
    WHERE cart_items.cart_id = ?
    """
    cart_items = execute_query(cart_items_query, (cart_id,))

    items = [
        {
            "product_id": item[0],
            "product_name": item[1],
            "description": item[2],
            "price": item[3],
            "quantity": item[4],
            "total_price": item[4] * item[3]
        }
        for item in cart_items
    ]

    response = {
        "cart_id": cart_id,
        "total_amount": total_amount,
        "items": items
    }

    return jsonify(response), 200

# 9. PLACE ORDER
@app.route('/place_order/<customer_id>', methods=["POST"])
def place_order(customer_id):
    data = request.get_json()
    street_address = data.get('street_address')
    city = data.get('city')
    state = data.get('state')
    zip_code = data.get('zip_code')

    cart_query = "SELECT cart_id, total_amount FROM cart WHERE customer_id = ?"
    cart = execute_query(cart_query, (customer_id,))

    if not cart:
        return jsonify({"error": "Cart not found for this customer"}), 404

    cart_id, total_amount = cart[0]
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    order_insert_query = """
    INSERT INTO orders (customer_id, order_date, total_amount, street_address, city, state, zip_code) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    execute_insert(order_insert_query, (customer_id, order_date, total_amount, street_address, city, state, zip_code))

    execute_insert("DELETE FROM cart_items WHERE cart_id = ?", (cart_id,))
    execute_insert("DELETE FROM cart WHERE cart_id = ?", (cart_id,))

    return jsonify({"message": "Order placed successfully"}), 201

# 10. GET ALL CUSTOMERS
@app.route('/customers', methods=["GET"])
def get_all_customers():
    """GET A LIST OF ALL CUSTOMERS."""
    customers = execute_query("SELECT customer_id, first_name, last_name, email FROM customer")
    customer_list = [
        {
            "customer_id": customer[0],
            "first_name": customer[1],
            "last_name": customer[2],
            "email": customer[3]
        }
        for customer in customers
    ]
    return jsonify({"customers": customer_list}), 200

if __name__ == "__main__":
    app.run(debug=True)
