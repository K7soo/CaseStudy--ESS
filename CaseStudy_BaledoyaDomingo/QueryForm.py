import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from DBManipulation import ManipulateDB


class QueryForm:
    def __init__(self, window, manipulate_db):
        # Constructor
        self.window = window
        self.window.title("Enrollment Scheduling System")
        self.window.configure(bg="#bebebe")
        self.db = manipulate_db

        self.headingLabel = tk.Label(self.window, text="Q U E R Y   F O R M",
                                     font=("", 12), bg="#3f3f3f", pady=7)
        self.headingLabel.pack(fill=X)
        self.headingLabel.config(fg="white")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_pos = (screen_width - 800) // 2
        y_pos = (screen_height - 500) // 2
        self.window.geometry(f"800x500+{x_pos}+{y_pos}")

        # Canvases
        self.student_frame = tk.Frame(self.window, bg="#bebebe")
        self.student_frame.pack(fill=tk.BOTH, expand=True)

        self.query = tk.StringVar()
        self.conn = sqlite3.connect('testBubDatabase.db')
        self.strSQL = None
        self.cursor = None
        self.create_student_form()

    # -- Creates a Student Form to Verify Status as a student -- #
    def create_student_form(self):
        self.verification_frame = tk.LabelFrame(self.student_frame, text="Status Verification", 
                                                font=("Calibri"), bg="#bebebe")
        self.verification_frame.pack(padx=20, pady=20, fill=tk.BOTH)

        tk.Label(self.verification_frame, text="Enter Your Student ID: ", font=("Calibri", 14), 
                 bg="#bebebe").grid(row=0, column=0)
        self.id_entry = tk.Entry(self.verification_frame, font=("Calibri", 14))
        self.id_entry.grid(row=0, column=1, pady=20)

        self.verify_btn = tk.Button(self.verification_frame, text="Verify Status", width=15, 
                                    font=("Calibri", 14), bg="lightgray", 
                                    command=self.verify_student_status)
        self.verify_btn.grid(row=0, column=2)

        self.clear_btn = tk.Button(self.verification_frame, text="Clear", width=15, 
                                   font=("Calibri", 14), bg="lightgray", 
                                   command=self.clear_btn)
        self.clear_btn.grid(row=0, column=3)

        for widget in self.verification_frame.winfo_children():
            widget.grid_configure(padx=5, pady=10)

    # -- Checks from database if student ID exists or not
    def verify_student_status(self):
        student_id = self.id_entry.get()
        exists = self.db.is_student_id_exists(student_id)

        if not exists:
            messagebox.showinfo("Invalid Student ID", "The student ID does not exist in the database.")
        if exists:
            status = self.db.get_student_status(student_id)  # Get the student status separately
            if status == "Regular":
                self.create_widgets_regular()
                messagebox.showinfo("", "The entered student number is a regular.")
            if status == "Irregular":
                self.create_widgets_regular()
                messagebox.showinfo("", "The entered student number is an irregular.")

    # -- Creates Widgets based on Status -- Regular
    def create_widgets_regular(self):
        self.frame = tk.Frame(self.window, bg="#bebebe")
        self.frame.pack()
        self.container_frame = tk.Frame(self.window, bg="#bebebe")
        self.container_frame.pack(pady=20)

        # Widget Frame
        self.title_frame = tk.LabelFrame(self.frame, text="Queries", bg="#bebebe")
        self.title_frame.pack(fill=tk.BOTH, expand=True, padx=20, anchor=tk.CENTER)

        self.query_combobox = ttk.Combobox(self.title_frame, width=53, values=[
            "Tell me the available subjects in my course for 1st semester",
            "Tell me the available subjects in my course for 2nd semester",
            "Tell me the available schedules for each subject in my Course", 
            "Give me the available subjects for my course",
            "Give me a list of all professors for my course",
            "Give me a list of Major Subjects",
            "Give me a list of Minor Subjects"], textvariable=self.query)
        self.query_combobox.grid(row=0, column=0)
        
        self.add_btn = tk.Button(self.title_frame, width=20, text="Test Button", command=self.btn_command)
        self.add_btn.grid(row=0, column=1)

        for widget in self.title_frame.winfo_children():
            widget.grid_configure(sticky="news", padx=5, pady=5)

        # Treeview Frame
        self.table_frame = tk.LabelFrame(self.container_frame, text="", bg="#bebebe")
        self.table_frame.pack(padx=20, pady=10, fill=tk.BOTH)

        # Treeview
        self.tree = ttk.Treeview(self.table_frame,
                                 columns=("SubjectID", "SubjectName", "Year", "Semester", 
                                          "CourseID", "FacultyID", "Schedule"))
        self.tree.heading("#0", text="Index")
        self.tree.heading("SubjectID", text="Subject ID")
        self.tree.heading("SubjectName", text="Subject Name")
        self.tree.heading("CourseID", text="Course ID")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Semester", text="Semester")
        self.tree.heading("FacultyID", text="Faculty ID")
        self.tree.heading("Schedule", text="Schedule")

        self.tree_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)
        self.tree_scrollbar.pack(side="right", fill="y")

        self.tree.pack(fill=tk.BOTH, expand=True)  

    # Clears the Screen
    def clear_btn(self):
        self.frame.pack_forget()
        self.container_frame.pack_forget()
        # self.id_entry.delete(0, tk.END)

    # Is a command based on the query entered by User
    def btn_command(self):
        selected_query = self.query.get()
        if selected_query == "Tell me the available subjects in my course for 1st semester":
            self.tell_enrollment_start()
        elif selected_query == "Tell me the available subjects in my course for 2nd semester":
            self.tell_enrollment_start()
        elif selected_query == "Tell me the available schedules for each subject in my Course":
            self.available_schedules()
        elif selected_query == "Give me the available subjects for my course":
            self.available_subjects()
        elif selected_query == "Give me a list of all professors for my course":
            self.list_professors()
        elif selected_query == "Give me a list of Major Subjects":
            self.list_major_subjects()
        elif selected_query == "Give me a list of Minor Subjects":
            self.list_minor_subjects()
        else:
            messagebox.showwarning("Invalid Query", "Please select a valid query.")
        
    def tell_enrollment_start(self, student_id):
        conn = sqlite3.connect('testBubDatabase.db')
        cursor = conn.execute("SELECT YearLevel FROM Student WHERE StudentID = ?", (student_id,))
        data = cursor.fetchone()
        conn.close()

        if data is not None:
            selected_year = data[0]
            conn = sqlite3.connect('testBubDatabase.db')
            cursor = conn.execute("SELECT TimeStart FROM Subject WHERE Year = ?", (selected_year,))
            enrollment_data = cursor.fetchone()
            conn.close()

            if enrollment_data is not None:
                enrollment_date = enrollment_data[0]
                print("Enrollment for year", selected_year, "starts on:", enrollment_date)
            else:
                print("No enrollment schedule found for year", selected_year)
        else:
            print("Student not found.")

    def available_schedules(self):
        selected_course = "BSIT"  # You can get this from the user if needed
        conn = sqlite3.connect('testBubDatabase.db')
        cursor = conn.execute("SELECT SubjectName, Year, Semester, TimeStart, TimeEnd FROM Subject WHERE CourseID = ?", (selected_course,))
        data = cursor.fetchall()
        conn.close()

        if data:
            print("Available schedules for", selected_course, "course:")
            for subject in data:
                subject_name, year, semester, time_start, time_end = subject
                print(f"Subject: {subject_name}, Year: {year}, Semester: {semester}, Time: {time_start} - {time_end}")
        else:
            print("No subjects found for", selected_course, "course.")

    def available_subjects(self):
        selected_course = "BSIT"  # You can get this from the user if needed
        conn = sqlite3.connect('testBubDatabase.db')
        cursor = conn.execute("SELECT SubjectName FROM Subject WHERE CourseID = ?", (selected_course,))
        data = cursor.fetchall()
        conn.close()

        if data:
            print("Available subjects for", selected_course, "course:")
            for subject in data:
                subject_name = subject[0]
                print(subject_name)
        else:
            print("No subjects found for", selected_course, "course.")

    def list_professors(self):
        selected_course = "BSIT"  # You can get this from the user if needed
        conn = sqlite3.connect('testBubDatabase.db')
        cursor = conn.execute("SELECT Faculty.FacultyFirstName, Faculty.FacultyLastName, Subject.SubjectName "
                            "FROM Faculty INNER JOIN Subject ON Faculty.FacultyID = Subject.FacultyID "
                            "WHERE Subject.CourseID = ?", (selected_course,))
        data = cursor.fetchall()
        conn.close()

        if data:
            print("Professors for", selected_course, "course:")
            for professor in data:
                faculty_first_name, faculty_last_name, subject_name = professor
                print(f"{faculty_first_name} {faculty_last_name}: {subject_name}")
        else:
            print("No professors found for", selected_course, "course.")

    def list_major_subjects(self):
        student_id = self.id_entry.get()
        if not student_id:
            messagebox.showwarning("Invalid Input", "Please enter a student ID.")
            return

        conn = sqlite3.connect('testBubDatabase.db')
        cursor = conn.execute("SELECT CourseID FROM Student WHERE StudentID = ?", (student_id,))
        data = cursor.fetchone()
        conn.close()

        if data:
            selected_course_id = data[0]

            conn = sqlite3.connect('testBubDatabase.db')
            cursor = conn.execute("SELECT SubjectName FROM Subject WHERE CourseID = ? AND SubjectType = 'Major'", (selected_course_id,))
            data = cursor.fetchall()
            conn.close()

            if data:
                print("Major Subjects for the selected course:")
                for subject in data:
                    subject_name = subject[0]
                    print(subject_name)
            else:
                print("No major subjects found for the selected course.")
        else:
            print("Student not found.")

    def list_minor_subjects(self):
        student_id = self.id_entry.get()
        if not student_id:
            messagebox.showwarning("Invalid Input", "Please enter a student ID.")
            return

        conn = sqlite3.connect('testBubDatabase.db')
        cursor = conn.execute("SELECT CourseID FROM Student WHERE StudentID = ?", (student_id,))
        data = cursor.fetchone()
        conn.close()

        if data:
            selected_course_id = data[0]

            conn = sqlite3.connect('testBubDatabase.db')
            cursor = conn.execute("SELECT SubjectName FROM Subject WHERE CourseID = ? AND SubjectType = 'Minor'", (selected_course_id,))
            data = cursor.fetchall()
            conn.close()

            if data:
                print("Minor Subjects for the selected course:")
                for subject in data:
                    subject_name = subject[0]
                    print(subject_name)
            else:
                print("No minor subjects found for the selected course.")
        else:
            print("Student not found.")

    def close_and_open_login(self):
        self.window.destroy()
        self.show_login()

    def show_login(self):
        if self.app:
            self.app.destroy()
        self.window.deiconify()

# Run code for testing #
if __name__ == "__main__":
    window = tk.Tk()
    db = ManipulateDB()
    app = QueryForm(window, db)
    window.mainloop()
