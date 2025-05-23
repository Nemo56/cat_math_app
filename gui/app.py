# gui/app.py

import tkinter as tk
from tkinter import messagebox
from config import TEACHER_PASSWORD
# from student_mode import StudentMode
# from teacher_mode import TeacherMode


from gui.student_mode import StudentMode
from gui.teacher_mode import TeacherMode

class CATApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Адаптивное тестирование по математике")
        self.geometry("800x600")  # ← Увеличили размер окна
        self.resizable(True, True)  # ← Можно менять размер вручную

        self.current_frame = None
        self.user_data = {}

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_frame()

        tk.Label(self, text="Добро пожаловать!", font=("Arial", 20, "bold")).pack(pady=30)

        tk.Button(self, text="Пройти тест", width=40, font=("Arial", 14),
                  command=self.start_student_mode).pack(pady=15)
        tk.Button(self, text="Режим учителя", width=40, font=("Arial", 14),
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

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

