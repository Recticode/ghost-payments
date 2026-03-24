from db import Database
from payment import PaymentGateway

def main():
    database = Database("app.db")

    database.add_user("hi", "hi@hi.com")

    email = database.get_user_email(1)

    database.add_product("pro", 15.5)

    print(email)


if __name__ == '__main__':
     main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
