import sqlite3
from tkinter import messagebox


class ManipulateDB:
    def add_to_database(self, student_id, first_name, last_name, course, year_level, grades, status):
        try:
            conn = sqlite3.connect("testBubDatabase.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Student (StudentID, StudentFirstName, StudentLastName, \
                           Course, YearLevel, Grades, Status) \
                           VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (student_id, first_name, last_name, course, year_level, grades, status))
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error while adding to database:", e)

    def is_student_id_exists(self, student_id):
        # Check if the StudentID already exists in the database
        self.conn = sqlite3.connect('testBubDatabase.db')
        self.strSQL = "SELECT * FROM Student WHERE StudentID = ?"
        self.cursor = self.conn.execute(self.strSQL, (student_id,))
        row = self.cursor.fetchone()
        self.conn.close()
        return row is not None

    def update_database(self, student_id, updated_student_number, updated_first_name, updated_last_name,
                        updated_course, updated_year, updated_grades, updated_status):
        self.conn = sqlite3.connect('testBubDatabase.db')
        self.strSQL = "UPDATE Student SET StudentID=?, StudentFirstName=?, StudentLastName=?, " \
                      "Course=?, YearLevel=?, Grades=?, Status=? WHERE StudentID=?"
        self.cursor = self.conn.execute(self.strSQL, (updated_student_number, updated_first_name,
                                                      updated_last_name, updated_course, updated_year,
                                                      updated_grades, updated_status, student_id))
        self.conn.commit()
        self.cursor.close()

    def remove_from_database(self, student_id):
        self.conn = sqlite3.connect('testBubDatabase.db')
        self.strSQL = "DELETE FROM Student WHERE StudentID = ?"
        self.cursor = self.conn.execute(self.strSQL, (student_id,))
        self.conn.commit()
        self.cursor.close()
        messagebox.Message("Successfully removed from the database.")

    def create_table(self):
        try:
            conn = sqlite3.connect("testBubDatabase.db")
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Student (
                    StudentID INTEGER PRIMARY KEY,
                    StudentFirstName TEXT NOT NULL,
                    StudentLastName TEXT NOT NULL,
                    Course TEXT NOT NULL,
                    YearLevel TEXT NOT NULL,
                    Grades REAL NOT NULL,
                    Status TEXT NOT NULL  -- Add the "Status" column here
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error creating table:", e)
