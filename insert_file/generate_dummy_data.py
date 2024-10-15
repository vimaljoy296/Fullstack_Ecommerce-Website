import random

# Sample data for generation
first_names = ["John", "Jane", "Alex", "Emily", "Michael", "Sarah", "David", "Ashley", "Robert", "Jessica"]
last_names = ["Smith", "Doe", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson", "Moore"]
domains = ["email.com", "mail.com", "example.com", "test.com"]
streets = ["Oak St", "Maple St", "Pine St", "Cedar St", "Elm St", "Birch St"]
cities = ["Springfield", "Riverside", "Centerville", "Franklin", "Greenville", "Fairview"]
states = ["IL", "CA", "NY", "TX", "FL", "OH"]

# Function to generate a random phone number
def generate_phone_number():
    return f"{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

# Function to generate a random email address
def generate_email(first_name, last_name):
    domain = random.choice(domains)
    return f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{domain}"

# Function to generate random password
def generate_password():
    return f"pass{random.randint(100, 999)}"

# Script to generate SQL Insert statements
num_records = 1000
insert_statements = ""

for i in range(1, num_records + 1):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = generate_email(first_name, last_name)
    password = generate_password()
    phone_number = generate_phone_number()
    street_address = f"{random.randint(1, 999)} {random.choice(streets)}"
    city = random.choice(cities)
    state = random.choice(states)
    
    insert_statements += f"INSERT INTO customer (first_name, last_name, email, password, phone_number, street_address, city, state)\n"
    insert_statements += f"VALUES ('{first_name}', '{last_name}', '{email}', '{password}', '{phone_number}', '{street_address}', '{city}', '{state}');\n"

# Save to file
with open("customer_data.sql", "w") as file:
    file.write(insert_statements)

print("1000 rows of dummy data have been generated and saved to 'customer_data.sql'")
