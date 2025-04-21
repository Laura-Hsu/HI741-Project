import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
from user import authenticate_user
from utils import generate_statistics
import csv
from datetime import datetime
import pandas as pd
import os

USAGE_LOG = "usage_log.csv"

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
            tk.Button(master, text="Generate Statistics", width=25, command=self.generate_stats).pack(pady=5)

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
                "Race": race_entry.get().strip() if isinstance(race_entry, tk.StringVar) else race_entry.get().strip(),
                "Gender": gender_entry.get().strip() if isinstance(gender_entry, tk.StringVar) else gender_entry.get().strip(),
                "Ethnicity": ethnicity_entry.get().strip() if isinstance(ethnicity_entry, tk.StringVar) else ethnicity_entry.get().strip(),
                "Age": age_entry.get().strip(),
                "Zip_code": zip_entry.get().strip(),
                "Insurance": insurance_entry.get().strip() if isinstance(insurance_entry, tk.StringVar) else insurance_entry.get().strip(),
                "Chief_complaint": complaint_entry.get().strip(),
                "Note_ID": note_id_entry.get().strip(),
                "Note_type": note_type_entry.get().strip()
            }

            self.user.patient_manager.df = pd.concat([
                self.user.patient_manager.df,
                pd.DataFrame([new_row])
            ], ignore_index=True)
            self.user.patient_manager.df.to_csv("Patient_data.csv", index=False)
            messagebox.showinfo("Success", "Patient record added.")
            win.destroy()

        tk.Label(win, text="Patient_ID").pack()
        pid_entry = tk.Entry(win)
        pid_entry.pack()

        tk.Label(win, text="Visit_time (YYYY-MM-DD)").pack()
        time_entry = tk.Entry(win)
        time_entry.pack()

        tk.Label(win, text="Visit_department").pack()
        dept_entry = tk.Entry(win)
        dept_entry.pack()

        tk.Label(win, text="Race").pack()
        race_entry = ttk.Combobox(win, values=["White", "Black", "Asian", "Pacific islanders", "Native Americans", "Unknown"])
        race_entry.pack()

        tk.Label(win, text="Gender").pack()
        gender_entry = ttk.Combobox(win, values=["Female", "Male", "Non-binary"])
        gender_entry.pack()

        tk.Label(win, text="Ethnicity").pack()
        ethnicity_entry = ttk.Combobox(win, values=["Hispanic", "Non-Hispanic", "Other", "Unknown"])
        ethnicity_entry.pack()

        tk.Label(win, text="Age").pack()
        age_entry = tk.Entry(win)
        age_entry.pack()

        tk.Label(win, text="Zip_code").pack()
        zip_entry = tk.Entry(win)
        zip_entry.pack()

        tk.Label(win, text="Insurance").pack()
        insurance_entry = ttk.Combobox(win, values=["Medicare", "Medicaid", "None", "Unknown"])
        insurance_entry.pack()

        tk.Label(win, text="Chief complaint").pack()
        complaint_entry = tk.Entry(win)
        complaint_entry.pack()

        tk.Label(win, text="Note_ID").pack()
        note_id_entry = tk.Entry(win)
        note_id_entry.pack()

        tk.Label(win, text="Note_type").pack()
        note_type_entry = tk.Entry(win)
        note_type_entry.pack()

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

    def generate_stats(self):
        generate_statistics(self.user.patient_manager.df)
        self.log_action("generate_statistics")
        messagebox.showinfo("Done", "Statistics generated and saved as images.")

    def exit_program(self):
        self.log_action("exit")
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
