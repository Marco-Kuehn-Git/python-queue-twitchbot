import tkinter as tk
from tkinter import messagebox
import sys

def show_popup(type, title, message):
    root = tk.Tk()
    root.withdraw()
    
    types = {
        "info": messagebox.showinfo,
        "warning": messagebox.showwarning,
        "error": messagebox.showerror
    }
    
    if type in types:
        types[type](title, message)
    else:
        raise ValueError("Invalid popup type. Use 'info', 'warning', or 'error'.")
    
    root.destroy()
    sys.exit(1)
    