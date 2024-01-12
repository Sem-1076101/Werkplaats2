import sqlite3 
import bcrypt
import csv
from io import StringIO
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
                       (display_name, username, hashed_password, is_admin))
        cursor.connection.commit()


    def get_user_by_username(self, username):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM teachers WHERE username=?", (username,))
        return cursor.fetchone()


    def check_login(self, username, password):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM teachers WHERE username=?", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['teacher_password']):
            return True
        else:
            return False
    
    def get_all_teachers(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM teachers")
        return cursor.fetchall() 

    def get_teacher_by_id(self, teacher_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM teachers WHERE teacher_id=?", (teacher_id,))
        return cursor.fetchall()
    
    # def get_teacher_by_note(self, note_id):
    #     cursor = self.get_cursor()
    #     cursor.execute("SELECT * FROM teachers WHERE note_id=?", (teacher_id,))
    #     return cursor.fetchone()
    
    def get_all_categories(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM categories")
        return cursor.fetchall() 
    
    def get_categories_by_id(self, category_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM categories WHERE category_id =?", (category_id,))
        return cursor.fetchone()
    
    def create_note(self, title, note_source, is_public, teacher_id, category_id, note):
        cursor = self.get_cursor()
        cursor.execute(
            "INSERT INTO notes (title, note_source, is_public, teacher_id, category_id, note, date_created) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))",
            (title, note_source, is_public, teacher_id, category_id, note)
        )
        cursor.connection.commit()
    
    def create_question(self, teacher_id, note_id, generated_question, final_changed_question):
        cursor = self.get_cursor()
        cursor.execute(
            "INSERT INTO questions (note_id, exam_question, date_created, teacher_id, generated_question) VALUES (?, ?, datetime('now'), ?, ?)",
            (note_id, final_changed_question, teacher_id, generated_question)
        )
        cursor.connection.commit()

    def get_all_notes_and_questions_by_name(self, note_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT notes.note_id, notes.title, notes.note_source, notes.is_public, notes.teacher_id, notes.note, notes.date_created, teachers.display_name, questions.exam_question, questions.generated_question, questions.date_created AS question_date_created FROM notes LEFT JOIN teachers ON notes.teacher_id = teachers.teacher_id LEFT JOIN questions ON notes.note_id = questions.note_id WHERE notes.note_id = ?", (note_id,))
        return cursor.fetchall()
    
    def get_all_notes(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM notes")
        return cursor.fetchall()
    
    def get_note_by_id(self, note_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM notes WHERE note_id = ?", (note_id,))
        return cursor.fetchone()
    
    
    def get_all_notes_by_name(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT notes.note_id, notes.title, notes.note_source, notes.is_public, notes.teacher_id, notes.note, notes.date_created, teachers.display_name FROM notes JOIN teachers ON notes.teacher_id = teachers.teacher_id")
        return cursor.fetchall()
    
    def get_all_questions(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM questions")
        return cursor.fetchall()
    
    def get_note_id_by_note(self, question_note):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM notes WHERE note = ?", (question_note,))
        return cursor.fetchall()
    
    def get_all_questions_by_note_id(self, note_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM questions WHERE note_id = ?", (note_id,))
        return cursor.fetchall()
    
    def get_questions_by_id(self, questions_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM questions WHERE questions_id = ?", (questions_id,))
        return cursor.fetchone()

    def get_all_questions_by_id_user(self, teacher_id, note_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM questions WHERE teacher_id = ? AND note_id = ?", (teacher_id, note_id,))
        return cursor.fetchall()

    def create_category(self, description):
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO categories (omschrijving, date_created) VALUES (?, datetime('now'))",(description,))
        cursor.connection.commit()

    def delete_category(self, category_id):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM categories WHERE category_id = ?", (category_id,))
        cursor.connection.commit()

    def update_category(self, category_id, omschrijving):
        cursor = self.get_cursor()
        cursor.execute("UPDATE categories SET omschrijving=? WHERE category_id =?", (omschrijving, category_id))
        cursor.connection.commit()

    def update_question(self, questions_id, exam_question):
        cursor = self.get_cursor()
        cursor.execute("UPDATE questions SET exam_question=? WHERE questions_id =?", (exam_question, questions_id))
        cursor.connection.commit()

    def update_note(self, note_id, title, note_source, is_public, category_id, note):
        cursor = self.get_cursor()
        cursor.execute("UPDATE notes SET title =?, note_source =?, is_public=?, category_id=?, note =? WHERE note_id=?", (title, note_source, is_public, category_id, note, note_id))
        cursor.connection.commit()

    def update_user(self, teacher_id, display_name, username, is_admin):
        cursor = self.get_cursor()
        cursor.execute("UPDATE teachers SET display_name=?, username=?, is_admin=? WHERE teacher_id=?", (display_name, username, is_admin, teacher_id))
        cursor.connection.commit()

    def delete_user(self, teacher_id):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM teachers WHERE teacher_id = ?", (teacher_id,))
        cursor.connection.commit()

    def delete_question(self, questions_id):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM questions WHERE questions_id = ?", (questions_id,))
        cursor.connection.commit()

    def delete_note(self, note_id):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM notes WHERE note_id = ?", (note_id,))
        cursor.connection.commit()
    
    def export_notes_to_csv(self, filename='exported_notes.csv'):
        cursor = self.get_cursor()
        cursor.execute("SELECT note_id, title, note_source, is_public, teacher_id, note, date_created FROM notes")
        notes = cursor.fetchall()

        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(['Note ID', 'Title', 'Source', 'Public', 'Teacher ID', 'Note', 'Date Created'])
        
        for note in notes:
            csv_writer.writerow([note['note_id'], note['title'], note['note_source'], note['is_public'], note['teacher_id'], note['note'], note['date_created']])
        
        with open(filename, 'w', newline='') as csv_file:
            csv_file.write(csv_data.getvalue())

        print(f"Notities zijn succesvol geëxporteerd naar {filename}.")

    
