import sqlite3
import datetime
import os
import sys
import shutil
from firebase import OnlineLeaderboard

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
    app_data_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), "Andaza")
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
        self.online_liderboard = OnlineLeaderboard()
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game (
                
                time_choice INTEGER DEFAULT  500
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
    

    def add_score(self, name, score, play_time):
        # 1. Check if name exists
        self.cursor.execute('SELECT score FROM liderboard WHERE name = ?', (name,))
        result = self.cursor.fetchone()

        if result:
            # 2. Update if score is higher
            if score > result[0]:
                self.cursor.execute('''
                    UPDATE liderboard 
                    SET score = ?, time = ?, is_synced = 0 
                    WHERE name = ?
                ''', (score, play_time, name))
        else:
            # 3. Insert if new
            self.cursor.execute('''
                INSERT INTO liderboard (name, score, time, is_synced) 
                VALUES (?, ?, ?, 0)
            ''', (name, score, play_time))
        
        self.connection.commit()

        if self.cursor.rowcount > 0:
            self.online_liderboard.sync_score(name, score, play_time, self.mark_as_synced)
            
    def get_all_andaza(self):
        self.cursor.execute('SELECT * FROM andaza')
        all = self.cursor.fetchall()
        return all
    
    def get_time_choice(self):
        self.cursor.execute('SELECT time_choice FROM game')
        time = self.cursor.fetchone()
        if time:
            return time[0]
        else:
            return 300
    
    def update_time_choice(self, time):
        self.cursor.execute('''
            UPDATE game SET time_choice = ? 
        ''', (time,))
        self.connection.commit()

    def close(self):
        self.connection.close()

    def get_random_andaza(self):
        self.cursor.execute('SELECT andaza FROM andaza ORDER BY last_date ASC LIMIT 1')
        all = self.cursor.fetchone()
        return all
    
    def get_liderboard(self):
        self.cursor.execute(
            "SELECT name, score, time FROM liderboard ORDER BY score DESC"
        )
        return self.cursor.fetchall()

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
    

   
    def get_unsynced_scores(self):
        """Finds scores that need to go to the cloud."""
        self.cursor.execute("SELECT name, score, time FROM liderboard WHERE is_synced = 0")
        return self.cursor.fetchall()

    def mark_as_synced(self, name):
        """Updates local DB so we don't sync this person again."""
        self.cursor.execute("UPDATE liderboard SET is_synced = 1 WHERE name = ?", (name,))
        self.connection.commit()
        print(f"Local DB: {name} marked as synced.")

    def setup_database(self):
        cursor = self.connection.cursor()

        # 1. Create the Liderboard with all necessary columns
        # We include UNIQUE(name) so the 'ON CONFLICT' logic works!
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS liderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                score INTEGER DEFAULT 0,
                time TEXT,
                is_synced INTEGER DEFAULT 0
            )
        """)

        # 2. Migration: Add 'is_synced' if user is updating from a very old version
        try:
            cursor.execute("ALTER TABLE liderboard ADD COLUMN is_synced INTEGER DEFAULT 0")
        except:
            pass # Column already exists, no problem

        # 3. Create the Game Settings table
        cursor.execute("CREATE TABLE IF NOT EXISTS game (time_choice INTEGER)")

        # 4. Ensure Game Settings has default data (Prevent IndexError on new PCs)
        cursor.execute("SELECT COUNT(*) FROM game")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO game (time_choice) VALUES (600)")

        self.connection.commit()
        print("Database ready: Liderboard and Settings initialized.")
    

# db = DB()
# # db.clear_app_data()
# db.add_score('johnny', 30, "3")
# print(db.get_liderboard())
# andazebi = db.get_random_andaza()
# db.close()
# print(andazebi)


