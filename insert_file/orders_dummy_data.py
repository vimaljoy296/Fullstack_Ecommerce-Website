import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('vjbazaar.db')
cursor = conn.cursor()

# Sample data for order statuses and locations
statuses = ["Shipped", "Processing", "Delivered", "Cancelled", "Pending"]
street_addresses = ["45 Oak St", "23 Maple Ave", "78 Pine Rd", "100 Cedar Ln", "11 Birch Blvd"]
cities = ["Springfield", "Greenville", "Riverside", "Fairfield", "Madison"]
states = ["IL", "CA", "NY", "TX", "FL"]
zip_codes = ["62701", "90001", "10001", "73301", "33101"]

# Adjust customer_id_range based on the IDs available in your `customers` table
customer_id_range = (1, 500)  # Replace 500 with the max customer_id in your database

# Generate and insert 1,000 rows of dummy data into the orders table
for _ in range(1000):
    customer_id = random.randint(*customer_id_range)
    order_date = datetime.now() - timedelta(days=random.randint(0, 365))  # Random date within the past year
    order_date = order_date.strftime("%Y-%m-%d")
    total_amount = round(random.uniform(10, 1000), 2)  # Random total amount between $10 and $1000
    status = random.choice(statuses)
    street_address = random.choice(street_addresses)
    city = random.choice(cities)
    state = random.choice(states)
    zip_code = random.choice(zip_codes)
    
    # Insert data into the orders table
    cursor.execute('''
        INSERT INTO orders (customer_id, order_date, total_amount, status, street_address, city, state, zip_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (customer_id, order_date, total_amount, status, street_address, city, state, zip_code))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("1,000 rows of dummy data have been added to the 'orders' table.")
