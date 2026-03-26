from src.db import Database

def main():
    # this database and its methods are used in the frontend where the user can see their orders and entitlements

    database = Database("../app.db")
    database.recreate_db()

    # if you manage to erase the database, use database.recreate_db()

if __name__ == '__main__':
     main()
