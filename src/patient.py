import os
import pandas as pd

DATA_DIR = "data"
PATIENT_FILE = os.path.join(DATA_DIR, "Patient_data.csv")
NOTE_FILE = os.path.join(DATA_DIR, "Notes.csv")

class PatientManager:
    def __init__(self):
        self.df = pd.read_csv(PATIENT_FILE)

    def add_patient_from_gui(self, pid, visit_time, dept, race, gender, ethnicity, age, zipcode, insurance, chief, note_id, note_type, note_text):
        import random
        visit_id = str(random.randint(100000, 999999))
        new_row = {
            "Patient_ID": pid,
            "Visit_ID": visit_id,
            "Visit_time": visit_time,
            "Visit_department": dept,
            "Race": race,
            "Gender": gender,
            "Ethnicity": ethnicity,
            "Age": age,
            "Zip_code": zipcode,
            "Insurance": insurance,
            "Chief_complaint": chief,
            "Note_ID": note_id,
            "Note_type": note_type
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.df.to_csv(PATIENT_FILE, index=False)

        try:
            notes_df = pd.read_csv(NOTE_FILE)
        except FileNotFoundError:
            notes_df = pd.DataFrame(columns=["Note_ID", "Note_text"])

        notes_df["Note_ID"] = notes_df["Note_ID"].astype(str)
        if note_id not in notes_df["Note_ID"].values:
            notes_df = pd.concat([notes_df, pd.DataFrame([{"Note_ID": note_id, "Note_text": note_text}])], ignore_index=True)
            notes_df.to_csv(NOTE_FILE, index=False)

    def count_visits(self, date):
        df = self.df.copy()
        df['Visit_time'] = pd.to_datetime(df['Visit_time'], errors='coerce')
        target_date = pd.to_datetime(date, errors='coerce')
        return df[df['Visit_time'] == target_date].shape[0]

    def remove_patient(self):
        import tkinter.simpledialog as simpledialog
        from tkinter import messagebox

        pid = simpledialog.askstring("Remove Patient", "Enter Patient_ID to remove:")
        if pid:
            pid = pid.strip()
            self.df["Patient_ID"] = self.df["Patient_ID"].astype(str).str.strip()

            if pid not in self.df["Patient_ID"].values:
                messagebox.showerror("Error", f"Patient_ID {pid} does not exist.")
                return

            self.df = self.df[self.df["Patient_ID"] != pid]
            self.df.to_csv(PATIENT_FILE, index=False)
            messagebox.showinfo("Success", f"All records for Patient_ID {pid} have been removed.")

    def retrieve_patient(self):
        import tkinter.simpledialog as simpledialog
        import tkinter as tk
        from tkinter import messagebox

        pid = simpledialog.askstring("Retrieve Patient", "Enter Patient_ID to retrieve:")
        if pid:
            pid = pid.strip()
            self.df["Patient_ID"] = self.df["Patient_ID"].astype(str).str.strip()
            result = self.df[self.df["Patient_ID"] == pid]
            if result.empty:
                messagebox.showerror("Not Found", f"Patient_ID {pid} does not exist.")
            else:
                info = result.to_string(index=False)

                result_window = tk.Toplevel()
                result_window.title(f"Records for Patient_ID {pid}")
                result_window.geometry("1100x400")

                text_widget = tk.Text(result_window, wrap=tk.WORD)
                text_widget.insert(tk.END, info)
                text_widget.config(state=tk.DISABLED)
                text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

