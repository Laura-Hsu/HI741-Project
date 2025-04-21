
from patient import PatientManager
from note import NoteManager
import pandas as pd

class Admin:
    def __init__(self):
        self.patient_manager = PatientManager()
        self.note_manager = NoteManager()

class Nurse:
    def __init__(self):
        self.patient_manager = PatientManager()
        self.note_manager = NoteManager()

class Clinician:
    def __init__(self):
        self.patient_manager = PatientManager()
        self.note_manager = NoteManager()

class Management:
    def __init__(self):
        self.patient_manager = PatientManager()
        self.note_manager = NoteManager()

def authenticate_user(username, password):
    df = pd.read_csv("Credentials.csv")
    match = df[(df["username"] == username) & (df["password"] == password)]
    if not match.empty:
        return match.iloc[0]["role"]
    return None
