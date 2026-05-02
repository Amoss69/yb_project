import sqlite3
import hashlib
import os

DB_NAME = "users.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = os.urandom(16).hex() # generate a random salt if none provided (new user)
    # stretches the password using the salt over 100k iterations, making brute force slow
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 100000).hex()
    return salt, hashed

def create_users_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            salt TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    salt, hashed = hash_password(password) # salt is random here, stored alongside the hash
    cursor.execute(
        "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
        (username, hashed, salt)
    )
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user  # (id, username, password_hash, salt)