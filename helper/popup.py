import tkinter as tk
from tkinter import messagebox
import sys

# Info popup
def show_info_popup(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()
    sys.exit(1)

# Warning popup
def show_warning_popup(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning(title, message)
    root.destroy()
    sys.exit(1)

# Error popup
def show_error_popup(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()
    sys.exit(1)