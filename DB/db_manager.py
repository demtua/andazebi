import sqlite3
import datetime


class DB:
    def __init__(self, db_name="DB/andaza.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def insert_date(self, date, andaza):
        self.cursor.execute(f'''
            INSERT INTO andaza (last_date) VALUES (?) WHERE andaza = {andaza}
        ''', (date,))
        self.connection.commit()

    def get_all_andaza(self):
        self.cursor.execute('SELECT * FROM andaza')
        all = self.cursor.fetchall()
        return all

    def close(self):
        self.connection.close()

    def get_random_andaza(self):
        self.cursor.execute('SELECT andaza FROM andaza ORDER BY last_date ASC LIMIT 1')
        all = self.cursor.fetchone()
        return all

    def update_last_date(self, andaza):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            UPDATE andaza SET last_date = ? WHERE andaza = ?
        ''', (date, andaza))
        self.connection.commit()
    

# db = DB()
# andazebi = db.get_random_andaza()
# db.close()
# print(andazebi)


