import sqlite3
import random

# Connect to the database
conn = sqlite3.connect('vjbazaar.db')
cursor = conn.cursor()

# Generate 1000 rows of dummy data for cart_items
for _ in range(1000):
    cart_id = random.randint(1, 1000)  # assuming 1000 carts exist
    product_id = random.randint(1, 500)  # assuming 500 products exist
    quantity = random.randint(1, 10)  # random quantity between 1 and 10
    
    # Insert data into cart_items table
    cursor.execute('''
        INSERT INTO cart_items (cart_id, product_id, quantity)
        VALUES (?, ?, ?)
    ''', (cart_id, product_id, quantity))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("1000 rows of dummy data have been added to 'cart_items' table.")
