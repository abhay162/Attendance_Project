import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Database connection
conn = sqlite3.connect('attendance.db')
c = conn.cursor()

# Create student table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE)''')

# Create attendance table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY,
                student_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id))''')

# Function to add new student
def add_student():
    name = entry_name.get()
    if name:
        try:
            c.execute("INSERT INTO students (name) VALUES (?)", (name,))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            entry_name.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student already exists!")
    else:
        messagebox.showerror("Error", "Please enter student name.")

# Function to mark attendance
def mark_attendance():
    name = entry_name.get()
    if name:
        try:
            student_id = c.execute("SELECT id FROM students WHERE name=?", (name,)).fetchone()
            if student_id:
                today_date = datetime.today().strftime('%Y-%m-%d')
                c.execute("INSERT INTO attendance (student_id, date) VALUES (?, ?)", (student_id[0], today_date))
                conn.commit()
                messagebox.showinfo("Success", "Attendance marked successfully!")
                entry_name.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Student not found!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please enter student name.")

# Function to generate attendance report
def generate_report():
    try:
        c.execute('''SELECT students.name, attendance.date
                     FROM students LEFT JOIN attendance
                     ON students.id = attendance.student_id
                     ORDER BY students.name, attendance.date''')
        data = c.fetchall()
        report = ''
        if data:
            for row in data:
                report += f"{row[0]} - {row[1]}\n"
            messagebox.showinfo("Attendance Report", report)
        else:
            messagebox.showinfo("Attendance Report", "No attendance records found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Attendance Management System")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

label_name = tk.Label(frame, text="Student Name:")
label_name.grid(row=0, column=0, padx=5, pady=5)

entry_name = tk.Entry(frame, width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

button_add = tk.Button(frame, text="Add Student", command=add_student)
button_add.grid(row=1, column=0, columnspan=2, pady=5)

button_mark = tk.Button(frame, text="Mark Attendance", command=mark_attendance)
button_mark.grid(row=2, column=0, columnspan=2, pady=5)

button_report = tk.Button(frame, text="Generate Report", command=generate_report)
button_report.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()

# Close database connection
conn.close()