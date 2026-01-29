import sqlite3
import datetime
import os
import sys
import shutil


def get_db_path():
    db_name = "andaza.db"
    
    # 1. Define where the bundled (read-only) DB is
    if hasattr(sys, '_MEIPASS'):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.abspath(".")
    
    source_db = os.path.join(bundle_dir, "DB", db_name)

    # 2. Define where the writable (persistent) DB should live
    # This creates a folder in C:\Users\Name\AppData\Roaming\YourAppName
    app_data_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), "YourGameName")
    os.makedirs(app_data_dir, exist_ok=True)
    
    dest_db = os.path.join(app_data_dir, db_name)

    # 3. If the writable DB doesn't exist yet, copy the bundled one there
    if not os.path.exists(dest_db):
        shutil.copy2(source_db, dest_db)
        
    return dest_db


class DB:
    def __init__(self):
        self.db_path = get_db_path()
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.migrate_database()
        self.setup_database()
        self.create_missing_tables()

    def create_missing_tables(self):
        cursor = self.connection.cursor()
        # This line checks the database. 
        # If 'liderboard' is missing, it creates it.
        # If 'liderboard' is already there, it does NOTHING (safe).
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS liderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                score INTEGER,
                time TEXT
            )
        """)
        self.connection.commit()


    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    


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
    

    def add_score(self, score, name, time):
        self.cursor.execute(f'''
            INSERT INTO liderboard (score, name, time) VALUES (?, ?, ?) 
        ''', (score, name, time ))
        self.connection.commit()

    def get_all_andaza(self):
        self.cursor.execute('SELECT * FROM andaza')
        all = self.cursor.fetchall()
        return all
    
    def get_selected_time(self):
        self.cursor.execute('SELECT time_choice FROM game')
        time = self.cursor.fetchone()[0]
        return time

    def close(self):
        self.connection.close()

    def get_random_andaza(self):
        self.cursor.execute('SELECT andaza FROM andaza ORDER BY last_date ASC LIMIT 1')
        all = self.cursor.fetchone()
        return all
    
    def get_liderboard(self):
        self.cursor.execute('SELECT * FROM liderboard')
        all = self.cursor.fetchone()
        return all

    def update_last_date(self, andaza):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            UPDATE andaza SET last_date = ? WHERE andaza = ?
        ''', (date, andaza))
        self.connection.commit()
 

    def clear_app_data(self):
        # Get the path to the AppData folder
        app_data_dir = os.path.join(os.environ.get('APPDATA'), "YourGameName")
        
        if os.path.exists(app_data_dir):
            try:
                # This deletes the folder and everything inside it
                shutil.rmtree(app_data_dir)
                print("App data cleared successfully!")
                # Restart or close the app here to avoid errors
            except Exception as e:
                print(f"Error clearing data: {e}")
    

    def migrate_database(self):
        cursor = self.connection.cursor()
        
        # This command creates the table ONLY if it's missing
        # Replace 'new_table_name' and columns with your actual data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                sound_enabled INTEGER DEFAULT 1
            )
        """)
        
        # If you just added a NEW COLUMN to an existing table:
        try:
            cursor.execute("ALTER TABLE scores ADD COLUMN difficulty TEXT DEFAULT 'easy'")
        except sqlite3.OperationalError:
            # If the column already exists, SQLite throws an error, which we ignore
            pass
            
        self.connection.commit()



    def setup_database(self):
        cursor = self.connection.cursor()

        # 1. Create the NEW table (e.g., game_history)
        # This tracks every single game played, not just the high scores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_played TEXT,
                result TEXT, -- 'Win' or 'Loss'
                date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Ensure the LIDERBOARD table is correct
        # We use IF NOT EXISTS so it doesn't crash if it's already there
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS liderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER DEFAULT 0,
                time TEXT, -- Stores how long it took to win
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 3. MIGRATION EXAMPLE:
        # If you wanted to move a specific player from a 'Guest' name 
        # to a specific name in your new structure:
        cursor.execute("UPDATE liderboard SET name = 'Champion' WHERE score > 1000 AND name = 'Guest'")

        self.connection.commit()
        print("Migration complete: 'liderboard' verified and 'game_history' added.")
    

# db = DB()
# # db.clear_app_data()
# db.add_score('johnny', 30, "3")
# print(db.get_liderboard())
# andazebi = db.get_random_andaza()
# db.close()
# print(andazebi)


