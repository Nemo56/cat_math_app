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


# def apply_theme(style, theme):
#     if theme == "light":
#         style.theme_use('clam')
#         style.configure("TFrame", background="#ffffff")
#         style.configure("TLabel", background="#ffffff", foreground="#000000")
#         style.configure("TButton", background="#f0f0f0", foreground="#000000")
#         style.map("TButton",
#                   background=[('active', '#d9d9d9')],
#                   relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

#         style.configure("TNotebook", background="#ffffff")
#         style.configure("TNotebook.Tab", background="#e0e0e0", foreground="#000000")
#         style.map("TNotebook.Tab",
#                   background=[('selected', '#ffffff')],
#                   foreground=[('selected', '#007acc')])
    
 



#     elif theme == "dark":
#         style.theme_use('clam')
#         style.configure("TFrame", background="#2e2e2e")
#         style.configure("TLabel", background="#2e2e2e", foreground="white")
#         style.configure("TButton", background="#444444", foreground="white")
#         style.map("TButton",
#                   background=[('active', '#555555')],
#                   relief=[('pressed', 'flat'), ('!pressed', 'groove')])

#         style.configure("TNotebook", background="#2e2e2e")
#         style.configure("TNotebook.Tab", background="#444444", foreground="white")
#         style.map("TNotebook.Tab",
#                   background=[('selected', '#555555')],
#                   foreground=[('selected', 'yellow')])

def apply_theme(style, theme):
    # Загрузка стилей из JSON
    style_file = os.path.join("styles", f"{theme}.json")
    if os.path.exists(style_file):
        try:
            with open(style_file, "r") as f:
                styles = json.load(f)
            
            # Применение стилей для всех виджетов
            for widget, config in styles.items():
                style.configure(widget, **config)
            
            # Особые настройки для вкладок (если не заданы в JSON)
            if "TNotebook" not in styles:
                style.configure("TNotebook", background="#ffffff")
                style.configure("TNotebook.Tab", background="#e0e0e0")
            return
        except Exception as e:
            print(f"Ошибка загрузки темы: {e}")

    # # Fallback-стили (если файл не найден)
    # if theme == "light":
    #     # ... (существующий light-стиль)
    # elif theme == "dark":
    #     # ... (существующий dark-стиль)
    # elif theme == "school":
    #     style.theme_use('clam')
    #     style.configure(".", font=("Arial", 12))
    # elif theme == "high_contrast":
    #     style.theme_use('alt')


    # Fallback-стили (если файл не найден)
    if theme == "light":
        style.theme_use('clam')
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", foreground="#000000", font=("Arial", 12))
        style.configure("TButton", background="#f0f0f0", foreground="#000000", font=("Arial", 12))
        style.configure("TNotebook", background="#ffffff")
        style.configure("TNotebook.Tab", background="#e0e0e0", foreground="#000000")
        style.map("TButton",
                background=[('active', '#d9d9d9')],
                relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        style.map("TNotebook.Tab",
                background=[('selected', '#ffffff')],
                foreground=[('selected', '#007acc')])

    elif theme == "dark":
        style.theme_use('clam')
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TLabel", background="#2e2e2e", foreground="white", font=("Arial", 12))
        style.configure("TButton", background="#444444", foreground="white", font=("Arial", 12))
        style.configure("TNotebook", background="#2e2e2e")
        style.configure("TNotebook.Tab", background="#444444", foreground="white")
        style.map("TButton",
                background=[('active', '#555555')],
                relief=[('pressed', 'flat'), ('!pressed', 'groove')])
        style.map("TNotebook.Tab",
                background=[('selected', '#555555')],
                foreground=[('selected', 'yellow')])

    elif theme == "school":
        style.theme_use('clam')
        style.configure(".", font=("Arial", 12))
        style.configure("TFrame", background="#f0f8ff")
        style.configure("TLabel", background="#f0f8ff", foreground="#2a52be", font=("Arial", 12, "bold"))
        style.configure("TButton", background="#ff9966", foreground="#003366", 
                      font=("Arial", 12, "bold"), padding=10)
        style.configure("TNotebook", background="#f0f8ff")
        style.configure("TNotebook.Tab", background="#ffcc99", foreground="#003366")
        style.map("TButton",
                background=[('active', '#ffcc00')],
                relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        style.map("TNotebook.Tab",
                background=[('selected', '#ff9966')],
                foreground=[('selected', '#ffffff')])

    elif theme == "high_contrast":
        style.theme_use('alt')
        style.configure(".", font=("Arial", 14, "bold"))
        style.configure("TFrame", background="#000000")
        style.configure("TLabel", background="#000000", foreground="#ffff00")
        style.configure("TButton", background="#ffffff", foreground="#000000", 
                      borderwidth=3, relief="raised")
        style.configure("TNotebook", background="#000000")
        style.configure("TNotebook.Tab", background="#222222", foreground="#ffff00")
        style.map("TButton",
                background=[('active', '#ffff00')],
                foreground=[('active', '#000000')])
        style.map("TNotebook.Tab",
                background=[('selected', '#ffff00')],
                foreground=[('selected', '#000000')])