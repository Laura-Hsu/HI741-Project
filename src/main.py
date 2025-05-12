import tkinter as tk
from gui import LoginWindow

if __name__ == "__main__":
    print("Launching login window...")  # 測試輸出
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
