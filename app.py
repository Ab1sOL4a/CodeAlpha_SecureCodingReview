import sqlite3

DATABASE = "users.db"


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


def register():
    username = input("Enter username: ")
    password = input("Enter password: ")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
    cursor.execute(query)

    conn.commit()
    conn.close()

    print("Registration successful!")


def login():
    username = input("Username: ")
    password = input("Password: ")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)

    user = cursor.fetchone()

    conn.close()

    if user:
        print("Login successful!")
    else:
        print("Invalid username or password.")


def main():
    create_database()

    while True:
        print("\n=== Simple Login System ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()