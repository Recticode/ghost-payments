import sqlite3
from payment import PaymentGateway

class Database:
    def __init__(self, file_name):
        self.file_name = file_name

    def _connect(self):
        conn = sqlite3.connect(self.file_name)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def recreate_db(self):
        try:
            conn = self._connect()

            conn.execute("DROP TABLE IF EXISTS entitlements;")
            conn.execute("DROP TABLE IF EXISTS orders;")
            conn.execute("DROP TABLE IF EXISTS products;")
            conn.execute("DROP TABLE IF EXISTS users;")

            # users
            conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name VARCHAR,
                email VARCHAR
            )
            """)

            users = [
                (f"user{i}", f"user{i}@example.com")
                for i in range(1, 101)
            ]

            conn.executemany(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                users
            )

            # products
            conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name VARCHAR,
                price FLOAT
            )
            """)

            products = [
                (f"product{i}", i * 9.99)
                for i in range(1, 6)
            ]

            conn.executemany(
                "INSERT INTO products (name, price) VALUES (?, ?)",
                products
            )

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

            for i in range(1, 101, 3):
                for j in range(2, 6, 2):
                    product_id = self.get_product_id(f"product{j}")
                    user_id = self.get_user_id(f"user{i}@example.com")
                    self.buy_product(user_id, product_id)
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def add_user(self, name, email):
        try:
            conn = self._connect()

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
            conn = self._connect()

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

    def get_user_id(self, email):
        try:
            conn = self._connect()

            cursor = conn.execute("SELECT id FROM users WHERE email = ?", (email,))

            row = cursor.fetchone()
            user_id = row[0] if row else None

            conn.close()
            return user_id
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_product_id(self, name):
        try:
            conn = self._connect()

            cursor = conn.execute("SELECT id FROM products WHERE name = ?",
                                  (name, ))

            row = cursor.fetchone()
            product_id = row[0] if row else None

            conn.close()
            return product_id
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def buy_product(self, user_id, product_id):
        try:
            conn = self._connect()

            conn.execute("""
            INSERT INTO orders (user_id, product_id, status) VALUES (?, ?, ?)""",
                         (user_id, product_id, "pending"))

            conn.commit()

            price = self.get_product_price(product_id)
            if price is None:
                return "Product does not exist"

            payment_gateway = PaymentGateway()
            payment_status = payment_gateway.charge(user_id, price)['status']

            if payment_status == "success":
                conn.execute("UPDATE orders SET status = ? WHERE product_id = ?",
                             ("paid", product_id))
                conn.execute("INSERT INTO entitlements (user_id, product_id) VALUES (?, ?)",
                             (user_id, product_id))
            else:
                conn.execute("UPDATE orders SET status = ? WHERE product_id = ?",
                             ("failed", product_id))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_user_all_orders(self, user_id):
        try:
            conn = self._connect()

            cursor = conn.execute("SELECT id, product_id, status FROM orders WHERE user_id = ?",
                                (user_id, ))

            rows = cursor.fetchall()

            conn.close()

            return rows
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_user_all_entitlements(self, user_id):
        try:
            conn = self._connect()

            cursor = conn.execute("SELECT id, product_id FROM entitlements WHERE user_id = ?",
                                  (user_id, ))

            rows = cursor.fetchall()

            conn.close()

            return rows
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def does_user_have_entitlement(self, user_id, product_id):
        try:
            conn = self._connect()

            cursor = conn.execute("SELECT id FROM entitlements WHERE user_id = ? AND product_id = ?",
                                  (user_id, product_id))

            row = cursor.fetchone()

            yes = row[0] if row else None

            conn.close()

            return yes is not None
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_product_all_orders(self, product_id):
        try:
            conn = self._connect()

            cursor = conn.execute("SELECT id, user_id FROM orders WHERE product_id = ?",
                                  (product_id, ))

            rows = cursor.fetchall()

            conn.close()

            return rows
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_product_all_entitlements(self, product_id):
        try:
            conn = self._connect()

            cursor = conn.execute("SELECT id, user_id FROM entitlements WHERE product_id = ?",
                                  (product_id, ))

            rows = cursor.fetchall()

            conn.close()

            return rows
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_product_price(self, product_id):
        try:
            conn = self._connect()

            cursor = conn.execute("SELECT price FROM products WHERE id = ?",
                                  (product_id, ))

            row = cursor.fetchone()

            price = row[0] if row else None

            conn.close()

            return price
        except Exception as e:
            print(e)
        finally:
            conn.close()