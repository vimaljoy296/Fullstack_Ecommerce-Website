import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('vjbazaar.db')
cursor = conn.cursor()

# Drop the existing categories table if it exists
print("Dropping the existing 'categories' table if it exists...")
cursor.execute('DROP TABLE IF EXISTS categories')

# Create the new categories table
print("Creating new 'categories' table...")
cursor.execute('''
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL,
        description TEXT,
        type_id INTEGER
    )
''')

# Commit and close connection
conn.commit()
conn.close()

print("Existing 'categories' table dropped and new table created successfully.")
