import sqlite3
import random

# Connect to the database
conn = sqlite3.connect('vjbazaar.db')
cursor = conn.cursor()

# Sample product names and descriptions
product_names = [
    "Soccer Ball", "Basketball", "Tennis Racket", "Baseball Glove", "Yoga Mat",
    "Running Shoes", "Boxing Gloves", "Hiking Boots", "Golf Club", "Dumbbell"
]
descriptions = [
    "A high-quality soccer ball suitable for all weather conditions.",
    "A durable basketball for indoor and outdoor use.",
    "Lightweight tennis racket with improved control.",
    "Leather baseball glove for an excellent grip.",
    "Non-slip yoga mat for all types of exercises.",
    "Comfortable running shoes with breathable fabric.",
    "High-density foam boxing gloves for training.",
    "Sturdy hiking boots with waterproof lining.",
    "A professional golf club for all skill levels.",
    "Adjustable weight dumbbell for home workouts."
]
categories = list(range(1, 11))  # Assuming 10 categories

# Insert 500 rows of dummy data into products table
for _ in range(1000):
    category_id = random.choice(categories)
    product_name = random.choice(product_names)
    description = random.choice(descriptions)
    price = round(random.uniform(10, 100), 2)  # Random price between 10 and 100
    
    # Insert data into products table
    cursor.execute('''
        INSERT INTO products (category_id, product_name, description, price)
        VALUES (?, ?, ?, ?)
    ''', (category_id, product_name, description, price))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("1000 rows of dummy data have been added to the 'products' table.")
