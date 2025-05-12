import pandas as pd
import tkinter as tk
from tkinter import messagebox
import os

# Define paths to data files in the 'data' directory
DATA_DIR = "data"
NOTE_FILE = os.path.join(DATA_DIR, "Notes.csv")
PATIENT_FILE = os.path.join(DATA_DIR, "Patient_data.csv")

class NoteManager:
    def __init__(self):
        self.notes = pd.read_csv(NOTE_FILE)
        self.notes.columns = self.notes.columns.str.strip()

        # Prevent column name conflicts during merging
        self.notes = self.notes.rename(columns={
            "Patient_ID": "Note_Patient_ID",
            "Visit_ID": "Note_Visit_ID"
        })

        self.patient_data = pd.read_csv(PATIENT_FILE)
        self.patient_data.columns = self.patient_data.columns.str.strip()

    def view_note(self, date):
        try:
            self.patient_data['Visit_time'] = pd.to_datetime(self.patient_data['Visit_time'], errors='coerce')
            target_date = pd.to_datetime(date)
            matches = self.patient_data[self.patient_data['Visit_time'] == target_date].copy()
            matches = matches.dropna(subset=["Note_ID"])
            matches['Note_ID'] = matches['Note_ID'].astype(str)
            self.notes['Note_ID'] = self.notes['Note_ID'].astype(str)

            merged = matches.merge(self.notes, on="Note_ID", how="left")
            merged = merged.fillna("N/A")

            if merged.empty:
                messagebox.showerror("No Notes", "No notes found for the selected date.")
                return

            # Create a new window to display notes
            note_window = tk.Toplevel()
            note_window.title(f"Notes for {date}")
            note_window.geometry("850x500")

            frame = tk.Frame(note_window)
            frame.pack(fill=tk.BOTH, expand=True)

            scrollbar_y = tk.Scrollbar(frame)
            scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

            text_widget = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar_y.set)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar_y.config(command=text_widget.yview)

            for _, row in merged.iterrows():
                content = (
                    f"--- Note ---\n"
                    f"Patient_ID: {row.get('Patient_ID', 'N/A')}\n"
                    f"Visit_ID: {row.get('Visit_ID', 'N/A')}\n"
                    f"Note_ID: {row.get('Note_ID', 'N/A')}\n"
                    f"Type: {row.get('Note_type', 'N/A')}\n"
                    f"Text: {row.get('Note_text', '')}\n\n"
                )
                text_widget.insert(tk.END, content)

            text_widget.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading notes: {str(e)}")

