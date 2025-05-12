import tkinter as tk
from gui import LoginWindow

print("Launching GUI...") 

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
