

import os
import tkinter as tk
from tkinter import ttk, messagebox
from config import TEACHER_PASSWORD
from gui.student_mode import StudentMode
from gui.teacher_mode import TeacherMode
from utils.theme_manager import apply_theme


def apply_theme(style, theme_name):
    if theme_name == "light":
        style.theme_use("clam")
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", foreground="black")
        style.configure("TButton", background="#f0f0f0", foreground="black")
        style.map("TButton",
                  background=[('active', '#d9d9d9')],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

    elif theme_name == "dark":
        style.theme_use("clam")
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TLabel", background="#2e2e2e", foreground="white")
        style.configure("TButton", background="#444444", foreground="white")
        style.map("TButton",
                  background=[('active', '#555555')],
                  relief=[('pressed', 'flat'), ('!pressed', 'groove')])


class CATApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Адаптивное тестирование по математике")
        self.geometry("800x600")
        self.resizable(True, True)

        # === Инициализируем переменные ===
        self.style = ttk.Style()
        self.current_theme = "light"
        self.load_and_apply_theme()

        self.current_frame = None
        self.user_data = {}

        self.show_main_menu()

    def load_and_apply_theme(self):
        import json
        if os.path.exists("theme.json"):
            try:
                with open("theme.json", "r") as f:
                    data = json.load(f)
                    self.current_theme = data.get("theme", self.current_theme)
            except Exception:
                pass
        apply_theme(self.style, self.current_theme)

    def show_main_menu(self):
        self.clear_frame()  # ← Очищаем всё содержимое

        # === Заголовок ===
        tk.Label(self.current_frame, text="Добро пожаловать!", font=("Arial", 20, "bold")).pack(pady=30)

        # === Выбор темы ===
        theme_frame = ttk.Frame(self.current_frame)
        theme_frame.pack(pady=10)

        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_selector = ttk.Combobox(theme_frame, textvariable=self.theme_var, values=["light", "dark"], state="readonly", width=15)
        theme_selector.pack(side="left")

        apply_btn = ttk.Button(theme_frame, text="Применить тему", command=self.apply_selected_theme)
        apply_btn.pack(side="left", padx=5)

        # === Кнопки ===
        tk.Button(self.current_frame, text="Пройти тест", width=40, font=("Arial", 14),
                  command=self.start_student_mode).pack(pady=15)
        tk.Button(self.current_frame, text="Режим учителя", width=40, font=("Arial", 14),
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

        # Сохраняем тему в файл
        import json
        with open("theme.json", "w") as f:
            json.dump({"theme": selected}, f)

        # Применяем стиль
        apply_theme(self.style, selected)

        # Обновляем меню с новой темой
        self.show_main_menu()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(self)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # def open_teacher_login(self):
    #     password = tk.simpledialog.askstring("Вход", "Введите пароль учителя:", show='*')
    #     if password == TEACHER_PASSWORD:
    #         self.clear_frame()  # ← Убедитесь, что этот метод уничтожает старые виджеты
    #         TeacherMode(self).pack(fill="both", expand=True)
    #     else:
    #         messagebox.showerror("Ошибка", "Неверный пароль.")


