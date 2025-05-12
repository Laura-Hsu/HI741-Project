import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
from user import authenticate_user
from utils import generate_key_statistics
import csv
from datetime import datetime
import pandas as pd
import os

DATA_DIR = "data"
PATIENT_FILE = os.path.join(DATA_DIR, "Patient_data.csv")
USAGE_LOG = os.path.join(DATA_DIR, "usage_log.csv")

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("300x200")

        tk.Label(master, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        tk.Label(master, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        tk.Button(master, text="Login", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user_role = authenticate_user(username, password)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        from user import Admin, Nurse, Clinician, Management
        if user_role == "admin":
            user = Admin()
        elif user_role == "nurse":
            user = Nurse()
        elif user_role == "clinician":
            user = Clinician()
        elif user_role == "management":
            user = Management()
        else:
            self.log_action(username, "unknown", "login_failed", timestamp)
            messagebox.showerror("Error", "Invalid role")
            return

        self.log_action(username, role=user_role, action="login_success", timestamp=timestamp)
        self.master.destroy()
        root = tk.Tk()
        MainMenu(root, user, username, user_role)

    def log_action(self, username, role, action, timestamp):
        file_exists = os.path.exists(USAGE_LOG)
        is_empty = not file_exists or os.stat(USAGE_LOG).st_size == 0
        with open(USAGE_LOG, 'a', newline='') as file:
            writer = csv.writer(file)
            if is_empty:
                writer.writerow(['Username', 'Role', 'Timestamp', 'Action'])
            writer.writerow([username, role.lower().capitalize(), timestamp, action])

class MainMenu:
    def __init__(self, master, user, username, role):
        self.master = master
        self.user = user
        self.username = username
        self.role = role

        self.master.title(f"{self.role} Menu")
        self.master.geometry("400x300")

        if self.role.lower() in ["clinician", "nurse"]:
            tk.Button(master, text="Add Patient", width=25, command=self.add_patient).pack(pady=5)
            tk.Button(master, text="Remove Patient", width=25, command=lambda: self.log_and_call("remove_patient", self.user.patient_manager.remove_patient)).pack(pady=5)
            tk.Button(master, text="Retrieve Patient", width=25, command=lambda: self.log_and_call("retrieve_patient", self.user.patient_manager.retrieve_patient)).pack(pady=5)
            tk.Button(master, text="Count Visits", width=25, command=self.count_visits).pack(pady=5)
            tk.Button(master, text="View Note", width=25, command=self.view_note).pack(pady=5)
        elif self.role.lower() == "admin":
            tk.Button(master, text="Count Visits", width=25, command=self.count_visits).pack(pady=5)
        elif self.role.lower() == "management":
            tk.Button(master, text="Generate Key Statistics", width=25, command=self.generate_key_statistics).pack(pady=5)

        tk.Button(master, text="Exit", width=25, command=self.exit_program).pack(pady=20)

    def add_patient(self):
        import random
        win = tk.Toplevel(self.master)
        win.title("Add Patient")
        win.geometry("400x600")

        def submit():
            pid = pid_entry.get().strip()
            visit_id = str(random.randint(100000, 999999))
            visit_time = time_entry.get().strip()

            new_row = {
                "Patient_ID": pid,
                "Visit_ID": visit_id,
                "Visit_time": visit_time,
                "Visit_department": dept_entry.get().strip(),
                "Race": race_entry.get().strip(),
                "Gender": gender_entry.get().strip(),
                "Ethnicity": ethnicity_entry.get().strip(),
                "Age": age_entry.get().strip(),
                "Zip_code": zip_entry.get().strip(),
                "Insurance": insurance_entry.get().strip(),
                "Chief_complaint": complaint_entry.get().strip(),
                "Note_ID": note_id_entry.get().strip(),
                "Note_type": note_type_entry.get().strip()
            }

            self.user.patient_manager.df = pd.concat([
                self.user.patient_manager.df,
                pd.DataFrame([new_row])
            ], ignore_index=True)
            self.user.patient_manager.df.to_csv(PATIENT_FILE, index=False)
            messagebox.showinfo("Success", "Patient record added.")
            win.destroy()

        # Entry fields
        fields = [
            ("Patient_ID", tk.Entry),
            ("Visit_time (YYYY-MM-DD)", tk.Entry),
            ("Visit_department", tk.Entry),
            ("Race", lambda parent: ttk.Combobox(parent, values=["White", "Black", "Asian", "Pacific islanders", "Native Americans", "Unknown"])),
            ("Gender", lambda parent: ttk.Combobox(parent, values=["Female", "Male", "Non-binary"])),
            ("Ethnicity", lambda parent: ttk.Combobox(parent, values=["Hispanic", "Non-Hispanic", "Other", "Unknown"])),
            ("Age", tk.Entry),
            ("Zip_code", tk.Entry),
            ("Insurance", lambda parent: ttk.Combobox(parent, values=["Medicare", "Medicaid", "None", "Unknown"])),
            ("Chief complaint", tk.Entry),
            ("Note_ID", tk.Entry),
            ("Note_type", tk.Entry)
        ]

        entries = {}
        for label_text, widget_class in fields:
            tk.Label(win, text=label_text).pack()
            widget = widget_class(win) if callable(widget_class) else widget_class(win)
            widget.pack()
            entries[label_text] = widget

        pid_entry = entries["Patient_ID"]
        time_entry = entries["Visit_time (YYYY-MM-DD)"]
        dept_entry = entries["Visit_department"]
        race_entry = entries["Race"]
        gender_entry = entries["Gender"]
        ethnicity_entry = entries["Ethnicity"]
        age_entry = entries["Age"]
        zip_entry = entries["Zip_code"]
        insurance_entry = entries["Insurance"]
        complaint_entry = entries["Chief complaint"]
        note_id_entry = entries["Note_ID"]
        note_type_entry = entries["Note_type"]

        tk.Button(win, text="Submit", command=submit).pack(pady=10)

    def log_action(self, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(USAGE_LOG, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.username, self.role.lower().capitalize(), timestamp, action])

    def log_and_call(self, action, func):
        self.log_action(action)
        func()

    def count_visits(self):
        date = askstring("Count Visits", "Enter date (YYYY-MM-DD):")
        if date:
            self.log_action("count_visits")
            count = self.user.patient_manager.count_visits(date)
            messagebox.showinfo("Visit Count", f"Total visits on {date}: {count}")

    def view_note(self):
        date = askstring("View Note", "Enter visit date (YYYY-MM-DD):")
        if date:
            self.log_action("view_note")
            self.user.note_manager.view_note(date)

    def generate_key_statistics(self):
        df = pd.read_csv(PATIENT_FILE)
        generate_key_statistics(df)
        self.log_action("generate_key_statistics")
        messagebox.showinfo("Done", "Key statistics generated and saved to 'data/' folder.")

    def exit_program(self):
        self.log_action("exit")
        self.master.quit()
