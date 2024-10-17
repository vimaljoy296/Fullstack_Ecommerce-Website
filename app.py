from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database helper functions
def execute_query(query):
    """Execute a SELECT query and return the results."""
    conn = sqlite3.connect('/workspaces/VJBazaar/vjbazaar.db')
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def execute_insert(query):
    """Execute an INSERT/UPDATE query."""
    conn = sqlite3.connect('/workspaces/VJBazaar/vjbazaar.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()  # Commit the changes to the database
    conn.close()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# 1. SIGN UP
@app.route('/sign_up', methods=["POST"])
def sign_up():
    """REGISTER A NEW USER."""
    data = request.get_json()  # Parse the JSON body of the request
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    # Check if the email is already registered
    existing_user = execute_query(f"SELECT * FROM customer WHERE email = '{email}'")
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    # Insert new user data into the customer table
    insert_query = f"""
    INSERT INTO customer (first_name, last_name, email, password) 
    VALUES ('{first_name}', '{last_name}', '{email}', '{password}')
    """
    execute_insert(insert_query)

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

    # Execute the query
    top_rated_products = execute_query(query)

    # Format the top-rated products for JSON output
    homepage_content["top_rated_products"] = [
        {
            "product_id": product[0], 
            "product_name": product[1], 
            "description": product[2], 
            "price": float(product[3]),  # Convert price to float for JSON compatibility
            "average_rating": round(product[4], 1)  # Round to one decimal place
        }
        for product in top_rated_products
    ]

    # Return as JSON
    return jsonify(homepage_content), 200

# 3. USER PROFILE
@app.route('/customer/<int:customer_id>', methods=["GET"])
def get_customer_by_id(customer_id):
    """GET A CUSTOMER BY THEIR ID."""
    customerid = execute_query(f"SELECT first_name, last_name, customer_id FROM customer WHERE customer_id = {customer_id}")
    if customerid:
        return jsonify(customerid), 200
    return jsonify({"error": "Customer not found"}), 404

# 4. PRODUCT DETAILS
@app.route('/product/<int:product_id>', methods=["GET"])
def get_product_by_id(product_id):
    """GET A PRODUCT BY ITS ID."""
    product = execute_query(f"SELECT * FROM products WHERE product_id = {product_id}")
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

# 5. PRODUCT SEARCH
@app.route('/products/search', methods=["GET"])
def search_products():
    """SEARCH FOR PRODUCTS BASED ON QUERY PARAMETERS."""
    # Get query parameters
    product_id = request.args.get('id')
    name = request.args.get('name')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    # Start building the query
    query = "SELECT * FROM products WHERE 1=1"
    
    # Add conditions based on available query parameters
    if product_id:
        query += f" AND product_id = {product_id}"
    if name:
        query += f" AND product_name LIKE '%{name}%'"
    if min_price:
        query += f" AND price >= {min_price}"
    if max_price:
        query += f" AND price <= {max_price}"
    
    # Execute query
    products = execute_query(query)
    
    # Check if any products were found
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

# 6. ADD TO CART
@app.route('/cart/<customer_id>', methods=["POST"])
def add_to_cart(customer_id):
    """ADD AN ITEM TO THE CART."""
    # Get data from the request
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)  # Default quantity to 1 if not provided
    
    # Find or create the cart for this customer
    cart_query = f"SELECT cart_id, total_amount FROM cart WHERE customer_id = {customer_id}"
    cart = execute_query(cart_query)
    
    if not cart:
        # If the customer doesn't have a cart, create a new one with total_amount initialized to 0
        insert_cart_query = f"INSERT INTO cart (customer_id, total_amount) VALUES ({customer_id}, 0)"
        execute_insert(insert_cart_query)
        cart = execute_query(cart_query)
        
    cart_id = cart[0][0]  # Get the cart ID for this customer
    
    # Check if the product is already in the cart items
    existing_cart_item = execute_query(f"SELECT * FROM cart_items WHERE cart_id = {cart_id} AND product_id = {product_id}")
    
    if existing_cart_item:
        # If the product is already in the cart, update the quantity
        update_query = f"""
        UPDATE cart_items 
        SET quantity = quantity + {quantity}
        WHERE cart_id = {cart_id} AND product_id = {product_id}
        """
        execute_query(update_query)
        message = "Cart item quantity updated successfully."
    else:
        # If the product is not in the cart, add it
        insert_query = f"""
        INSERT INTO cart_items (cart_id, product_id, quantity) 
        VALUES ({cart_id}, {product_id}, {quantity})
        """
        execute_insert(insert_query)
        message = "Item added to cart successfully."
    
    # Update the total amount in the cart
    product_price_query = f"SELECT price FROM products WHERE product_id = {product_id}"
    product_price_result = execute_query(product_price_query)
    
    if not product_price_result:
        return jsonify({"error": "Product not found"}), 404  # Handle case where product does not exist
    
    product_price = product_price_result[0][0]
    new_total_amount = cart[0][1] + (product_price * quantity)
    update_total_query = f"UPDATE cart SET total_amount = {new_total_amount} WHERE cart_id = {cart_id}"
    execute_insert(update_total_query)
    
    return jsonify({"message": message}), 200


# 7. VIEW CART
@app.route('/cart/<customer_id>', methods=["GET"])
def view_cart(customer_id):
    """VIEW THE CART DETAILS FOR A SPECIFIC CUSTOMER."""
    # Query to get the cart details for a specific customer
    cart_query = f"""
    SELECT cart.cart_id, cart.total_amount 
    FROM cart 
    WHERE cart.customer_id = {customer_id}
    """
    cart = execute_query(cart_query)

    if not cart:
        return jsonify({"message": "Cart not found for this customer"}), 404
    
    cart_id = cart[0][0]
    total_amount = cart[0][1]

    # Query to get all items in the cart
    cart_items_query = f"""
    SELECT products.product_id, products.product_name, products.description, 
           products.price, cart_items.quantity
    FROM cart_items
    JOIN products ON cart_items.product_id = products.product_id
    WHERE cart_items.cart_id = {cart_id}
    """
    cart_items = execute_query(cart_items_query)

    # Format the data into a structured JSON response
    items = []
    for item in cart_items:
        items.append({
            "product_id": item[0],
            "product_name": item[1],
            "description": item[2],
            "price": item[3],
            "quantity": item[4],
            "total_price": item[4] * item[3]  # Price multiplied by quantity
        })

    response = {
        "cart_id": cart_id,
        "total_amount": total_amount,
        "items": items
    }

    return jsonify(response), 200

# 8. PLACE ORDER
# Place Order with Address Details
@app.route('/place_order/<customer_id>', methods=["POST"])
def place_order(customer_id):
    # Parse the JSON request data for address information
    data = request.get_json()
    street_address = data.get('street_address')
    city = data.get('city')
    state = data.get('state')
    zip_code = data.get('zip_code')
    
    # Step 1: Retrieve the cart details for the customer
    cart_query = f"""
    SELECT cart_id, total_amount FROM cart WHERE customer_id = {customer_id}
    """
    cart = execute_query(cart_query)
    
    if not cart:
        return jsonify({"message": "No cart found for this customer"}), 404
    
    cart_id = cart[0][0]
    total_amount = cart[0][1]
    
    # Step 2: Insert a new order entry into the orders table with address details
    order_date = datetime.now().strftime('%Y-%m-%d')  # Current date
    order_insert_query = f"""
    INSERT INTO orders (customer_id, order_date, total_amount, status, street_address, city, state, zip_code) 
    VALUES ({customer_id}, '{order_date}', {total_amount}, 'Pending', '{street_address}', '{city}', '{state}', '{zip_code}')
    """
    execute_insert(order_insert_query)
 
    # Step 4: Clear the cart (remove items from cart_items and reset cart total_amount)
    clear_cart_items_query = f"DELETE FROM cart_items WHERE cart_id = {cart_id}"
    execute_insert(clear_cart_items_query)

    reset_cart_total_query = f"UPDATE cart SET total_amount = 0 WHERE cart_id = {cart_id}"
    execute_insert(reset_cart_total_query)

    return jsonify({
        "message": "Order placed successfully",
        "total_amount": total_amount,
        "customer_id": customer_id,
        "address": {
            "street_address": street_address,
            "city": city,
            "state": state,
            "zip_code": zip_code
        }
    }), 201

# 9. GET ALL CUSTOMERS
@app.route('/customers', methods=["GET"])
def get_all_customers():
    """GET ALL CUSTOMER DETAILS."""
    query = "SELECT customer_id, first_name, last_name, email FROM customer"
    customers = execute_query(query)
    
    if not customers:
        return jsonify({"message": "No customers found."}), 404
    
    customer_list = [
        {
            "customer_id": customer[0],
            "first_name": customer[1],
            "last_name": customer[2],
            "email": customer[3]
        }
        for customer in customers
    ]
    
    return jsonify(customer_list), 200

# 10. GET ALL PRODUCTS
@app.route('/products', methods=["GET"])
def get_all_products():
    """GET ALL PRODUCT DETAILS."""
    query = "SELECT product_id, product_name, description, price FROM products"
    products = execute_query(query)
    
    if not products:
        return jsonify({"message": "No products found."}), 404
    
    product_list = [
        {
            "product_id": product[0],
            "product_name": product[1],
            "description": product[2],
            "price": float(product[3])  # Ensure price is a float for JSON compatibility
        }
        for product in products
    ]
    
    return jsonify(product_list), 200



if __name__ == '__main__':
    app.run(debug=True)
