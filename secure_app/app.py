import sqlite3
import hashlib
import secrets

DATABASE = "secure_users.db"

def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    return salt.hex() + ":" + password_hash.hex()

def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def register():
    username = input("Enter username: ")
    password = input("Enter password: ")

    password_hash = hash_password(password)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
        INSERT INTO users (username, password_hash)
        VALUES (?, ?)
    """

    try:
        cursor.execute(query, (username, password_hash))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.close()


def login():
    username = input("Username: ")
    password = input("Password: ")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
        SELECT password_hash FROM users
        WHERE username = ?
    """

    cursor.execute(query, (username,))
    user = cursor.fetchone()

    conn.close()

    if user:
        stored_salt, stored_hash = user[0].split(":")

        salt = bytes.fromhex(stored_salt)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            100000
        ).hex()

        if password_hash == stored_hash:
            print("Login successful!")
            return

    print("Invalid username or password.")

def main():
    create_database()

    while True:
        print("\n=== Secure Login System ===")
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
