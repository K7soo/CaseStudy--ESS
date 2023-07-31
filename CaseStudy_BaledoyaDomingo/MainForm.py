import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from DBManipulation import ManipulateDB


class MainForm:
    def __init__(self, window, manipulate_db):
        self.window = window
        self.window.title("Enrollment Scheduling System")
        self.db = manipulate_db

        self.headingLabel = tk.Label(self.window, text="Q U E R Y   F O R M",
                                     font=("", 12), bg="#3f3f3f", pady=7)
        self.headingLabel.pack(fill=X)
        self.headingLabel.config(fg="white")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_pos = (screen_width - 700) // 2
        y_pos = (screen_height - 350) // 2
        self.window.geometry(f"700x350+{x_pos}+{y_pos}")
  
        self.frame = tk.Frame(self.window)
        self.frame.pack()

        self.query = tk.StringVar()
        self.conn = sqlite3.connect('testBubDatabase.db')
        self.strSQL = None
        self.cursor = None

        self.create_widgets()

    def create_widgets(self):
        # Frame 1
        self.title_frame = tk.LabelFrame(self.frame, text="Main Menu")
        self.title_frame.grid(row=0, column=0, pady=20)

        tk.Label(self.title_frame, text="Queries:").grid(row=0, column=0)

        self.query_combobox = ttk.Combobox(self.title_frame, width=53, values=[
            "Tell me the available time slots to enroll in a specific subject",
            "Tell me when enrollment has started for my year(1st-4th)",
            "Give me the available subjects for my course",
            "Tell me the due date of enrollment for my year(1st-4th)",
            "Tell me the available schedules for each subject"],
                                           textvariable=self.query)
        self.query_combobox.grid(row=0, column=1)

        # self.filler_lbl = tk.Label(self.title_frame, text="hi")
        # self.filler_lbl.grid(row=0, column=0)

        for widget in self.title_frame.winfo_children():
            widget.grid_configure(sticky="news", padx=5, pady=5)

        # Frame 2
        self.second_frame = tk.LabelFrame(self.frame, text="")
        self.second_frame.grid(row=1, column=0, pady=20)

        tk.Label(self.second_frame, text="Options: ").grid(row=0, column=0)

        self.add_btn = tk.Button(self.second_frame, text="Test Button", command=self.btn_command)
        self.add_btn.grid(row=1, column=0)

    def btn_command(self):
        self.conn = sqlite3.connect('testBubDatabase.db')
        # SELECT statement
        self.strSQL = "INSERT INTO Student( [StudentID], [StudentName], [YearLevel], [Status], [GPA]) " \
                 "VALUES (6, 'Baobs', '2', 'Regular', '2.00')"

        # execute() methods run sql query
        self.cursor = self.conn.execute(self.strSQL)
        self.conn.commit()
        self.cursor.close()
        messagebox.showinfo("", "Data Uploaded Successfully.")

    def close_and_open_login(self):
        self.window.destroy()  # Close the MainForm window
        self.show_login()  # Open the Login window

    def show_login(self):
        if self.app:
            self.app.destroy()
        self.window.deiconify()

# Run code for testing #
if __name__ == "__main__":
    window = tk.Tk()
    db = ManipulateDB()
    app = MainForm(window, db)
    window.mainloop()
