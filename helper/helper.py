import requests
import tkinter as tk
from tkinter import messagebox
import sys

from bot.config import TWITCH_CLIENT_ID

# A simple check to see if token is valid or not
def can_connect_with_token(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": TWITCH_CLIENT_ID,
    }
    try:
        response = requests.get("https://api.twitch.tv/helix/users", headers=headers, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print("Error testing token connectivity:", e)
        return False

# A function to create popups
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