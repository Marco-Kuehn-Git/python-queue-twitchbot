import requests
import tkinter as tk
from tkinter import messagebox
import sys

from bot.config import TWITCH_CLIENT_ID

def can_connect_with_token(token):
    """
    Checks if a connection to Twitch can be established using the provided token.

    Returns True if the token is valid (HTTP status 200), otherwise False.
    """
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

def show_popup(type, title, message):
    """
    Creates a popup message window using tkinter.
    
    Args
    - type (str): Type of popup ('info', 'warning', or 'error').
    - title (str): Title of the popup window.
    - message (str): Message content to display.
    
    Raises ValueError If an invalid popup type is provided.
    """
    root = tk.Tk()
    root.withdraw()

    popup_types = {
        "info": messagebox.showinfo,
        "warning": messagebox.showwarning,
        "error": messagebox.showerror
    }
    
    if type in popup_types:
        popup_types[type](title, message)
    else:
        raise ValueError("Invalid popup type. Use 'info', 'warning', or 'error'.")
    
    root.destroy()
    sys.exit(1)
