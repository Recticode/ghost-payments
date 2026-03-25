from db import Database

def main():
    database = Database("app.db")

    database.add_user("hi", "hi@hi.com")
    user_id = database.get_user_id("hi@hi.com")
    print(user_id)

    database.add_product("pro", 15.5)
    product_id = database.get_product_id("pro")

    database.buy_product(user_id, product_id)

    orders = database.get_user_all_orders(user_id)
    print(orders)

    entitlements = database.get_user_all_entitlements(user_id)
    print(entitlements)

    yes = database.does_user_have_entitlement(user_id, 1)
    print(yes)




if __name__ == '__main__':
     main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
