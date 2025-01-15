import sqlite3
import random

# Connect to SQLite database
conn = sqlite3.connect('vjbazaar.db')
cursor = conn.cursor()

# Sample data for "Indoor" and "Outdoor" categories
category_names = ["Indoor", "Outdoor"]
descriptions = [
    "Activities suitable for indoor environments like gyms or homes.",
    "Outdoor activities including hiking, running, and cycling."
]

# Insert 1000 rows of dummy data into categories table with only "Indoor" and "Outdoor" categories
for _ in range(1000):
    category_name = random.choice(category_names)
    description = descriptions[0] if category_name == "Indoor" else descriptions[1]
    type_id = 1 if category_name == "Indoor" else 2  # Set type_id as 1 for Indoor and 2 for Outdoor
    
    # Insert data into categories table
    cursor.execute('''
        INSERT INTO categories (category_name, description, type_id)
        VALUES (?, ?, ?)
    ''', (category_name, description, type_id))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("1000 rows of dummy data have been added to 'categories' table with only 'Indoor' and 'Outdoor' categories.")
