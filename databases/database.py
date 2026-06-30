import sqlite3
from contextlib import closing


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "databases" / "railway.db"

class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH

    def connect(self):
        return sqlite3.connect(self.db_path)

    def execute(self, query, params=()):
        with closing(self.connect()) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()

    def fetch_one(self, query, params=()):
        with closing(self.connect()) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query, params=()):
        with closing(self.connect()) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_many(self, query, data):
        with closing(self.connect()) as connection:
            cursor = connection.cursor()
            cursor.executemany(query, data)
            connection.commit()


db = Database()