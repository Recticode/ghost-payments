import sqlite3
from payment import PaymentGateway

class Database:
    def __init__(self, file_name):
        self.file_name = file_name
        try:
            conn = sqlite3.connect(file_name)

            conn.execute("PRAGMA foreign_keys = ON;")

            # users
            conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name VARCHAR,
                email VARCHAR
            )
            """)

            # products
            conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name VARCHAR,
                price FLOAT
            )
            """)

            # orders
            conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                status VARCHAR,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
            """)

            # entitlements
            conn.execute("""
            CREATE TABLE IF NOT EXISTS entitlements (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
            """)

            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def add_user(self, name, email):
        try:
            conn = sqlite3.connect(self.file_name)

            conn.execute(f"""
            INSERT INTO users(name, email) VALUES (?, ?)
            """,
            (name, email))

            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def add_product(self, name, price):
        try:
            conn = sqlite3.connect(self.file_name)

            conn.execute("""
            INSERT INTO products(name, price) VALUES (?, ?)
            """,
            (name, price))

            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_user_email(self, id):
        try:
            conn = sqlite3.connect(self.file_name)

            cursor = conn.execute("SELECT email FROM users WHERE id = ?", (id,))

            row = cursor.fetchone()
            email = row[0] if row else None

            conn.close()
            return email
        except Exception as e:
            print("get error")
            print(e)
        finally:
            conn.close()