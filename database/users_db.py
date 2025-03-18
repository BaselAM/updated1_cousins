import sqlite3
import os

class UsersDB:
    def __init__(self, db_path="users.db"):
        # Create the database file in the same directory as this file.
        self.db_path = os.path.join(os.path.dirname(__file__), db_path)
        self.connection = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def add_user(self, username, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            # Username already exists
            return False

    def check_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return cursor.fetchone() is not None

    def close(self):
        self.connection.close()
