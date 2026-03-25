from db import Database

def main():
    database = Database("app.db")

    database.add_user("hi", "hi@hi.com")
    email = database.get_user_email(1)
    print(email)

    database.add_product("pro", 15.5)
    database.buy_product(1, 1)
    orders = database.get_user_all_orders(1)

    print(orders)


if __name__ == '__main__':
     main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
