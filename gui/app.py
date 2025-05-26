
# gui/app.py

import os
import tkinter as tk
from tkinter import ttk, messagebox
from config import TEACHER_PASSWORD
from gui.student_mode import StudentMode
from gui.teacher_mode import TeacherMode
from utils.style_loader import load_styles


class CATApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Адаптивное тестирование по математике")
        self.geometry("800x600")
        self.resizable(True, True)

        # === Путь к папке со стилями ===
        self.styles_dir = "styles"
        self.current_theme = "default"  # или "dark"

        # === Загружаем стиль из файла ===
        self.style = ttk.Style()
        self.load_and_apply_style()

        # === Текущий фрейм ===
        self.current_frame = None
        self.user_data = {}

        self.show_main_menu()

    def load_and_apply_style(self):
        """Загружает и применяет стиль из JSON"""
        if not os.path.exists(self.styles_dir):
            os.makedirs(self.styles_dir)

        style_path = os.path.join(self.styles_dir, f"{self.current_theme}.json")
        if not os.path.exists(style_path):
            print(f"[Ошибка] Файл стиля {style_path} не найден. Используется базовый стиль.")
            self.fallback_default_style()
        else:
            load_styles(self.style, self.current_theme)

    def fallback_default_style(self):
        """Резервный стиль, если нет JSON"""
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="white")
        self.style.configure("TLabel", background="white", foreground="black")
        self.style.configure("TButton", background="#f0f0f0", foreground="black")
        self.style.map("TButton",
                       background=[('active', '#d9d9d9')],
                       relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

    def show_main_menu(self):
        from utils.helpers import clear_frame
        clear_frame(self)

        # === Новый фрейм ===
        self.current_frame = ttk.Frame(self)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # === Заголовок ===
        tk.Label(self.current_frame, text="Добро пожаловать!", font=("Arial", 20, "bold")).pack(pady=30)

        # === Выбор темы ===
        theme_frame = ttk.Frame(self.current_frame)
        theme_frame.pack(pady=10)

        self.theme_var = tk.StringVar(value=self.current_theme)
        #theme_selector = ttk.Combobox(theme_frame, textvariable=self.theme_var, values=["default", "dark"], state="readonly", width=15)
        theme_selector = ttk.Combobox(theme_frame,textvariable=self.theme_var, 
                             values=["light", "dark", "school", "high_contrast"])
        theme_selector.pack(side="left")

        apply_btn = ttk.Button(theme_frame, text="Применить тему", command=self.apply_selected_theme)
        apply_btn.pack(side="left", padx=5)

        # === Кнопки главного меню ===
        ttk.Button(self.current_frame, text="Пройти тест", style="RoundedButton.TButton",
                   command=self.start_student_mode).pack(pady=15)

        ttk.Button(self.current_frame, text="Режим учителя", style="RoundedButton.TButton",
                   command=self.open_teacher_login).pack(pady=15)

    def start_student_mode(self):
        self.clear_frame()
        StudentMode(self).pack(fill="both", expand=True)

    def open_teacher_login(self):
        password = tk.simpledialog.askstring("Вход", "Введите пароль учителя:", show='*')
        if password == TEACHER_PASSWORD:
            self.clear_frame()
            TeacherMode(self).pack(fill="both", expand=True)
        else:
            messagebox.showerror("Ошибка", "Неверный пароль.")

    def apply_selected_theme(self):
        selected = self.theme_var.get()
        self.current_theme = selected

        # Сохраняем текущую тему
        import json
        with open("theme.json", "w") as f:
            json.dump({"theme": selected}, f)

        # Перезагружаем стиль
        self.load_and_apply_style()

        # Обновляем главное меню
        self.clear_frame()
        self.show_main_menu()

    def clear_frame(self):
        """Очистка текущего содержимого окна"""
        for widget in self.winfo_children():
            widget.destroy()
        self.current_frame = ttk.Frame(self)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)
 