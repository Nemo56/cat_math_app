# utils/theme_manager.py

import json
import os
from tkinter import ttk

THEME_FILE = "theme.json"


def load_theme():
    if os.path.exists(THEME_FILE):
        with open(THEME_FILE, "r") as f:
            data = json.load(f)
            return data.get("theme", "light")
    return "light"


def save_theme(theme):
    with open(THEME_FILE, "w") as f:
        json.dump({"theme": theme}, f)


def apply_theme(style, theme):
    if theme == "light":
        style.theme_use('clam')
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", foreground="#000000")
        style.configure("TButton", background="#f0f0f0", foreground="#000000")
        style.map("TButton",
                  background=[('active', '#d9d9d9')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        style.configure("TNotebook", background="#ffffff")
        style.configure("TNotebook.Tab", background="#e0e0e0", foreground="#000000")
        style.map("TNotebook.Tab",
                  background=[('selected', '#ffffff')],
                  foreground=[('selected', '#007acc')])
    
 



    elif theme == "dark":
        style.theme_use('clam')
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TLabel", background="#2e2e2e", foreground="white")
        style.configure("TButton", background="#444444", foreground="white")
        style.map("TButton",
                  background=[('active', '#555555')],
                  relief=[('pressed', 'flat'), ('!pressed', 'groove')])

        style.configure("TNotebook", background="#2e2e2e")
        style.configure("TNotebook.Tab", background="#444444", foreground="white")
        style.map("TNotebook.Tab",
                  background=[('selected', '#555555')],
                  foreground=[('selected', 'yellow')])