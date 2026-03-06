from database.connection import Database

if __name__ == "__main__":
    db = Database()
    db.clear_data()
    print("Database cleared and recreated successfully!")
