import sqlite3
import random

# Connect to SQLite database
conn = sqlite3.connect('vjbazaar.db')
cursor = conn.cursor()

# Sample data for categories
category_names = ["Gym Sport", "Outdoor Sport", "Water Sport", "Team Sport", "Solo Sport"]
descriptions = [
    "Activities suitable for gym or home environments.",
    "Outdoor activities including hiking, running, and cycling.",
    "Water-based sports such as swimming, diving, and surfing.",
    "Sports played in teams such as soccer, basketball, and volleyball.",
    "Individual sports like tennis, golf, and wrestling."
]

# Insert 1000 rows of dummy data into categories table
for _ in range(1000):
    category_name = random.choice(category_names)
    description = random.choice(descriptions)
    type_id = random.randint(1, 5)  # Random type_id between 1 and 5
    
    # Insert data into categories table
    cursor.execute('''
        INSERT INTO categories (category_name, description, type_id)
        VALUES (?, ?, ?)
    ''', (category_name, description, type_id))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("1000 rows of dummy data have been added to 'categories' table.")
