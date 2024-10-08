import sqlite3
import random

# Connect to the SQLite database
conn = sqlite3.connect('vjbazaar.db')
cursor = conn.cursor()

# Sample data for reviews
reviews = [
    "Excellent product! Exceeded my expectations.",
    "Good value for the price.",
    "Decent quality but could be better.",
    "Not satisfied with this purchase.",
    "Highly recommend this product!",
    "Amazing! Will buy again.",
    "Average, nothing special.",
    "Quality is okay, but delivery was late.",
    "Very happy with this purchase.",
    "Terrible experience, do not recommend."
]

# Assume product_id and customer_id are already in the database
# Adjust these numbers based on the IDs available in your `products` and `customers` tables
product_id_range = (1, 500)  # Replace 500 with the max product_id in your database
customer_id_range = (1, 500)  # Replace 500 with the max customer_id in your database

# Insert 1000 rows of dummy data into the reviews table
for _ in range(1000):
    product_id = random.randint(*product_id_range)
    customer_id = random.randint(*customer_id_range)
    rating = random.randint(1, 5)  # Rating between 1 and 5
    text_review = random.choice(reviews)
    
    # Insert data into the reviews table
    cursor.execute('''
        INSERT INTO reviews (product_id, customer_id, rating, text_review)
        VALUES (?, ?, ?, ?)
    ''', (product_id, customer_id, rating, text_review))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("1000 rows of dummy data have been added to the 'reviews' table.")
