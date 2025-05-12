import os
import pandas as pd
from patient import PatientManager
from note import NoteManager

DATA_DIR = "data"
CREDENTIAL_FILE = os.path.join(DATA_DIR, "Credentials.csv")

class Admin:
    def __init__(self):
        self.patient_manager = PatientManager()

class Management:
    def __init__(self):
        pass  # Management only uses key statistics (from utils)

class Nurse:
    def __init__(self):
        self.patient_manager = PatientManager()
        self.note_manager = NoteManager()

class Clinician:
    def __init__(self):
        self.patient_manager = PatientManager()
        self.note_manager = NoteManager()

def authenticate_user(username, password):
    df = pd.read_csv(CREDENTIAL_FILE)
    match = df[(df["username"] == username) & (df["password"] == password)]
    if not match.empty:
        return match.iloc[0]["role"]
    return None
