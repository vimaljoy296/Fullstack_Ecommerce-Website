import sqlite3
import random

# Connect to the SQLite database
conn = sqlite3.connect('vjbazaar.db')
cursor = conn.cursor()

# Adjust customer_id_range based on the IDs available in your `customers` table
customer_id_range = (1, 500)  # Replace 500 with the max customer_id in your database

# Generate and insert 1,000 rows of dummy data into the cart table
for _ in range(1000):
    customer_id = random.randint(*customer_id_range)
    total_amount = round(random.uniform(10, 1000), 2)  # Random total amount between $10 and $1000
    
    # Insert data into the cart table
    cursor.execute('''
        INSERT INTO cart (customer_id, total_amount)
        VALUES (?, ?)
    ''', (customer_id, total_amount))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("1,000 rows of dummy data have been added to the 'cart' table.")
