import psycopg2

# Функція для отримання підключення
def get_connection():
    return psycopg2.connect(
        dbname="erp_diplom",
        user="postgres",
        password="4568",
        host="localhost",
        port="5432"
    )

# ---------------- PRODUCTS ----------------

def create_products_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price NUMERIC NOT NULL,
            quantity INT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def drop_products_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS products CASCADE")
    conn.commit()
    cur.close()
    conn.close()

def insert_product(name, price, quantity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
    conn.commit()
    cur.close()
    conn.close()

def update_product(product_id, name=None, price=None, quantity=None):
    conn = get_connection()
    cur = conn.cursor()
    if name:
        cur.execute("UPDATE products SET name=%s WHERE id=%s", (name, product_id))
    if price:
        cur.execute("UPDATE products SET price=%s WHERE id=%s", (price, product_id))
    if quantity:
        cur.execute("UPDATE products SET quantity=%s WHERE id=%s", (quantity, product_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (product_id,))
    conn.commit()
    cur.close()
    conn.close()

def fetch_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()


# ---------------- USERS ----------------

def create_users_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            role VARCHAR(50) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def drop_users_table():
    conn = get_connection()
    cur = conn.cursor()
    # Використовуємо CASCADE, щоб видалити залежні об'єкти
    cur.execute("DROP TABLE IF EXISTS users CASCADE")
    conn.commit()
    cur.close()
    conn.close()

def insert_user(username, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, role) VALUES (%s, %s)", (username, role))
    conn.commit()
    cur.close()
    conn.close()

def update_user(user_id, username=None, role=None):
    conn = get_connection()
    cur = conn.cursor()
    if username:
        cur.execute("UPDATE users SET username=%s WHERE id=%s", (username, user_id))
    if role:
        cur.execute("UPDATE users SET role=%s WHERE id=%s", (role, user_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def fetch_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()