import sqlite3 
import bcrypt
from pathlib import Path

class UserModel:
    def __init__(self, db):
        db_path = Path(db)
        if not db_path.exists():
            raise FileNotFoundError(f'Database file {db} does not excist')
        self.dbpath = db_path

    def get_cursor(self):
        connection = sqlite3.connect(self.dbpath)
        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row
        return cursor
    

    def create_user(self, display_name, username, password, is_admin):
        # password hashen
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO teachers (display_name, username, teacher_password, date_created, is_admin) VALUES (?, ?, ?, datetime('now'), ?)",
                       display_name, username, hashed_password, is_admin)
        cursor.connection.commit()


    def check_login(self, username, password):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM teachers WHERE username=?", (username))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['teacher_password']):
            return True
        else:
            return False
    
    def get_all_teachers(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM teachers")
        return cursor.fetchall() 

        