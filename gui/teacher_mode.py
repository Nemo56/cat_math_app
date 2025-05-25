# # gui/teacher_mode.py

# import os
# import json
# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox


# class TeacherMode(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.master = master

#         # === Очистим предыдущий фрейм ===
#         self.master.clear_frame()

#         # === Создаём Notebook для вкладок ===
#         self.notebook = ttk.Notebook(self)
#         self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

#         # === Вкладка "Результаты" ===
#         self.results_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.results_frame, text="Результаты")

#         # Кнопка "Загрузить отчёты"
#         self.load_reports_button = ttk.Button(self.results_frame, text="Загрузить отчёты", command=self.load_reports)
#         self.load_reports_button.pack(pady=5)

#         # Canvas + Scrollbar для отчётов
#         self.reports_canvas = tk.Canvas(self.results_frame)
#         self.reports_scroll = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.reports_canvas.yview)
#         self.reports_container = ttk.Frame(self.reports_canvas)

#         self.reports_canvas.configure(yscrollcommand=self.reports_scroll.set)
#         self.reports_scroll.pack(side="right", fill="y")
#         self.reports_canvas.pack(side="left", fill="both", expand=True)
#         self.reports_canvas.create_window((0, 0), window=self.reports_container, anchor="nw")

#         # === Вкладка "Редактировать задачи" ===
#         self.edit_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.edit_frame, text="Редактировать задачи")

#         # === Селектор файлов ===
#         self.file_selector = ttk.Combobox(self.edit_frame)
#         self.file_selector.bind("<<ComboboxSelected>>", self.load_tasks)
#         self.file_selector.pack(pady=5)

#         # Canvas для прокрутки задач
#         self.tasks_canvas = tk.Canvas(self.edit_frame)
#         self.tasks_scroll = ttk.Scrollbar(self.edit_frame, orient="vertical", command=self.tasks_canvas.yview)
#         self.tasks_container = ttk.Frame(self.tasks_canvas)

#         self.tasks_canvas.configure(yscrollcommand=self.tasks_scroll.set)
#         self.tasks_scroll.pack(side="right", fill="y")
#         self.tasks_canvas.pack(side="left", fill="both", expand=True)
#         self.tasks_canvas.create_window((0, 0), window=self.tasks_container, anchor="nw", tags="tasks_window")

#         # Привязка изменения размера контейнера к canvas
#         self.tasks_container.bind("<Configure>",
#                                   lambda e: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all")))

#         # === Кнопка сохранения ===
#         self.save_button_frame = ttk.Frame(self.edit_frame)
#         self.save_button_frame.pack(side="bottom", fill="x", pady=5)

#         self.save_btn = ttk.Button(self.save_button_frame, text="Сохранить изменения",
#                                    command=lambda: self.save_tasks(self.file_selector.get()))
#         self.save_btn.pack()

#         self.task_files = {}
#         self.current_task_list = []
#         self.load_task_files()

#         # === Кнопка "Вернуться в меню" ===
#         back_frame = ttk.Frame(self)
#         back_frame.pack(side="bottom", fill="x", pady=10)

#         tk.Button(back_frame, text="Вернуться в меню", font=("Arial", 12),
#                   command=self.return_to_menu).pack()






#     def return_to_menu(self):
#         """Возвращение в главное меню"""
#         self.pack_forget()  # Отвязываем текущий фрейм от окна
#         self.destroy()      # Уничтожаем текущий интерфейс учителя

#         # Очищаем всё содержимое главного окна
#         for widget in self.master.winfo_children():
#             widget.destroy()

#         # Показываем главное меню
#         self.master.show_main_menu()

#     def load_reports(self):
#         from utils.helpers import list_reports
#         reports = list_reports()
#         for widget in self.reports_container.winfo_children():
#             widget.destroy()

#         if not reports:
#             tk.Label(self.reports_container, text="Нет сохранённых отчётов").pack()
#             return

#         for report in reports:
#             frame = ttk.Frame(self.reports_container, borderwidth=1, relief="solid")
#             frame.pack(fill="x", pady=2)

#             tk.Label(frame, text=report, wraplength=400).pack(side="left", padx=5)
#             tk.Button(frame, text="Открыть", width=8,
#                       command=lambda f=report: self.open_report(f)).pack(side="right", padx=5)

#     def open_report(self, filename):
#         import webbrowser
#         full_path = os.path.join("reports", filename)
#         if os.path.exists(full_path):
#             webbrowser.open(full_path)
#         else:
#             messagebox.showerror("Ошибка", "Файл не найден.")

#     def load_task_files(self):
#         from utils.helpers import clear_frame
#         clear_frame(self.tasks_container)

#         task_dir = "tasks"
#         if not os.path.exists(task_dir):
#             os.makedirs(task_dir)

#         files = [f for f in os.listdir(task_dir) if f.endswith(".json")]
#         if not files:
#             messagebox.showinfo("Информация", "Нет задач для редактирования.")
#             return

#         self.file_selector["values"] = files
#         self.file_selector.current(0)
#         self.file_selector.bind("<<ComboboxSelected>>", self.load_tasks)

#     def load_tasks(self, event=None):
#         from utils.helpers import clear_frame
#         clear_frame(self.tasks_container)

#         filename = self.file_selector.get()
#         path = os.path.join("tasks", filename)

#         try:
#             with open(path, "r", encoding="utf-8") as f:
#                 self.current_task_list = json.load(f)
#         except Exception as e:
#             messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")
#             return

#         self.task_files[filename] = []

#         for idx, task in enumerate(self.current_task_list):
#             frame = ttk.Frame(self.tasks_container, borderwidth=1, relief="solid")
#             frame.pack(fill="x", pady=5, padx=5)

#             tk.Label(frame, text=f"Задача {idx + 1}").pack(anchor="w")

#             tk.Label(frame, text="Текст:").pack(anchor="w")
#             entry_text = tk.Entry(frame, width=60)
#             entry_text.insert(0, task.get("text", ""))
#             entry_text.pack()

#             tk.Label(frame, text="Правильный ответ:").pack(anchor="w")
#             entry_answer = tk.Entry(frame, width=60)
#             entry_answer.insert(0, str(task.get("correct_answer", "")))
#             entry_answer.pack()

#             tk.Label(frame, text="IRT параметры: a, b, c").pack(anchor="w")
#             irt_frame = ttk.Frame(frame)
#             irt_frame.pack(fill="x")

#             entry_a = tk.Entry(irt_frame, width=10)
#             entry_b = tk.Entry(irt_frame, width=10)
#             entry_c = tk.Entry(irt_frame, width=10)

#             irt = task.get("irt", {})
#             entry_a.insert(0, str(irt.get("a", "")))
#             entry_b.insert(0, str(irt.get("b", "")))
#             entry_c.insert(0, str(irt.get("c", "")))

#             entry_a.pack(side="left", padx=2)
#             entry_b.pack(side="left", padx=2)
#             entry_c.pack(side="left", padx=2)

#             self.task_files[filename].append({
#                 "frame": frame,
#                 "text": entry_text,
#                 "answer": entry_answer,
#                 "a": entry_a,
#                 "b": entry_b,
#                 "c": entry_c,
#             })

#     def save_tasks(self, filename):
#         path = os.path.join("tasks", filename)

#         updated_tasks = []
#         for idx, task_data in enumerate(self.task_files[filename]):
#             original = self.current_task_list[idx]
#             updated = {
#                 "id": original.get("id", f"task_{idx+1}"),
#                 "type": original.get("type", "unknown"),
#                 "text": task_data["text"].get(),
#                 "correct_answer": task_data["answer"].get(),
#                 "irt": {
#                     "model": "3pl",
#                     "a": float(task_data["a"].get()) if task_data["a"].get() else 1.0,
#                     "b": float(task_data["b"].get()) if task_data["b"].get() else 0.0,
#                     "c": float(task_data["c"].get()) if task_data["c"].get() else 0.2,
#                 }
#             }
#             updated_tasks.append(updated)

#         try:
#             with open(path, "w", encoding="utf-8") as f:
#                 json.dump(updated_tasks, f, ensure_ascii=False, indent=2)
#             messagebox.showinfo("Успех", "Задачи успешно сохранены.")
#         except Exception as e:
#             messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")






# # gui/teacher_mode.py

# import os
# import json
# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# from utils.helpers import clear_frame


# class TeacherMode(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.master = master

#         # === Вкладки ===
#         self.notebook = ttk.Notebook(self)
#         self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

#         # === Вкладка "Результаты" ===
#         self.results_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.results_frame, text="Результаты")

#         # === Вкладка "Редактировать задачи" ===
#         self.edit_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.edit_frame, text="Редактировать задачи")

#         # === Кнопка "Вернуться в меню" ===
#         back_frame = ttk.Frame(self)
#         back_frame.pack(side="bottom", fill="x", pady=10)

#         tk.Button(back_frame, text="Вернуться в меню", font=("Arial", 12),
#                   command=self.return_to_menu).pack()

#         # === Селектор файлов ===
#         self.file_selector = ttk.Combobox(self.edit_frame)
#         self.file_selector.bind("<<ComboboxSelected>>", self.load_tasks)
#         self.file_selector.pack(pady=5)

#         # === Canvas + Scrollbar для прокрутки задач ===
#         self.tasks_canvas = tk.Canvas(self.edit_frame)
#         self.tasks_scroll = ttk.Scrollbar(self.edit_frame, orient="vertical", command=self.tasks_canvas.yview)
#         self.tasks_container = ttk.Frame(self.tasks_canvas)

#         self.tasks_canvas.configure(yscrollcommand=self.tasks_scroll.set)
#         self.tasks_canvas.pack(side="left", fill="both", expand=True)
#         self.tasks_scroll.pack(side="right", fill="y")
#         self.tasks_canvas.create_window((0, 0), window=self.tasks_container, anchor="nw")

#         # Привязываем изменение размера контейнера к scrollregion
#         self.tasks_container.bind("<Configure>", lambda e: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all")))

#         # Привязываем колесо мыши к Canvas
#         self.tasks_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

#         self.task_files = {}
#         self.current_task_list = []

#         self.load_task_files()

#     def on_mousewheel(self, event):
#         """Прокрутка через колесо мыши"""
#         self.tasks_canvas.yview_scroll(int(-1 * (event.delta / 60)), "units")
#         return "break"

#     def return_to_menu(self):
#         """Чистый выход в главное меню"""
#         self.pack_forget()
#         self.destroy()

#         for widget in self.master.winfo_children():
#             widget.destroy()

#         self.master.show_main_menu()

#     def load_task_files(self):
#         from utils.helpers import clear_frame
#         clear_frame(self.tasks_container)

#         task_dir = "tasks"
#         if not os.path.exists(task_dir):
#             os.makedirs(task_dir)

#         files = [f for f in os.listdir(task_dir) if f.endswith(".json")]
#         if not files:
#             messagebox.showinfo("Информация", "Нет задач для редактирования.")
#             return

#         self.file_selector["values"] = files
#         self.file_selector.current(0)

#     def load_tasks(self, event=None):
#         from utils.helpers import clear_frame
#         clear_frame(self.tasks_container)

#         filename = self.file_selector.get()
#         path = os.path.join("tasks", filename)

#         try:
#             with open(path, "r", encoding="utf-8") as f:
#                 self.current_task_list = json.load(f)
#         except Exception as e:
#             messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")
#             return

#         self.task_files[filename] = []

#         for idx, task in enumerate(self.current_task_list):
#             frame = ttk.Frame(self.tasks_container, borderwidth=1, relief="solid")
#             frame.pack(fill="x", pady=5, padx=5)

#             tk.Label(frame, text=f"Задача {idx + 1}", font=("Arial", 10, "bold")).pack(anchor="w")

#             tk.Label(frame, text="Текст:").pack(anchor="w")
#             entry_text = tk.Entry(frame, width=60)
#             entry_text.insert(0, task.get("text", ""))
#             entry_text.pack()

#             tk.Label(frame, text="Правильный ответ:").pack(anchor="w")
#             entry_answer = tk.Entry(frame, width=60)
#             entry_answer.insert(0, str(task.get("correct_answer", "")))
#             entry_answer.pack()

#             tk.Label(frame, text="IRT параметры: a, b, c").pack(anchor="w")
#             irt_frame = ttk.Frame(frame)
#             irt_frame.pack(fill="x")

#             entry_a = tk.Entry(irt_frame, width=10)
#             entry_b = tk.Entry(irt_frame, width=10)
#             entry_c = tk.Entry(irt_frame, width=10)

#             irt = task.get("irt", {})
#             entry_a.insert(0, str(irt.get("a", "")))
#             entry_b.insert(0, str(irt.get("b", "")))
#             entry_c.insert(0, str(irt.get("c", "")))

#             entry_a.pack(side="left", padx=2)
#             entry_b.pack(side="left", padx=2)
#             entry_c.pack(side="left", padx=2)

#             self.task_files[filename].append({
#                 "frame": frame,
#                 "text": entry_text,
#                 "answer": entry_answer,
#                 "a": entry_a,
#                 "b": entry_b,
#                 "c": entry_c,
#             })

#         # После загрузки задач — обновляем регион прокрутки
#         self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))

#     def save_tasks(self, filename):
#         path = os.path.join("tasks", filename)

#         updated_tasks = []
#         for idx, task_data in enumerate(self.task_files[filename]):
#             original = self.current_task_list[idx]
#             updated = {
#                 "id": original.get("id", f"task_{idx+1}"),
#                 "type": original.get("type", "unknown"),
#                 "text": task_data["text"].get(),
#                 "correct_answer": task_data["answer"].get(),
#                 "irt": {
#                     "model": "3pl",
#                     "a": float(task_data["a"].get()) if task_data["a"].get() else 1.0,
#                     "b": float(task_data["b"].get()) if task_data["b"].get() else 0.0,
#                     "c": float(task_data["c"].get()) if task_data["c"].get() else 0.2,
#                 }
#             }
#             updated_tasks.append(updated)

#         try:
#             with open(path, "w", encoding="utf-8") as f:
#                 json.dump(updated_tasks, f, ensure_ascii=False, indent=2)
#             messagebox.showinfo("Успех", "Задачи успешно сохранены.")
#         except Exception as e:
#             messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")


# gui/teacher_mode.py

import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from utils.helpers import list_reports, clear_frame


class TeacherMode(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # === Вкладки ===
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # === Вкладка "Результаты" ===
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Результаты")
        self.load_results_ui(self.results_frame)

        # === Вкладка "Редактировать задачи" ===
        self.edit_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.edit_frame, text="Редактировать задачи")

        # === Селектор файлов ===
        self.file_selector = ttk.Combobox(self.edit_frame)
        self.file_selector.bind("<<ComboboxSelected>>", self.load_tasks)
        self.file_selector.pack(pady=5)

        # Canvas + Scrollbar для прокрутки задач
        self.tasks_canvas = tk.Canvas(self.edit_frame)
        self.tasks_scroll = ttk.Scrollbar(self.edit_frame, orient="vertical", command=self.tasks_canvas.yview)
        self.tasks_container = ttk.Frame(self.tasks_canvas)

        self.tasks_canvas.configure(yscrollcommand=self.tasks_scroll.set)
        self.tasks_canvas.pack(side="left", fill="both", expand=True)
        self.tasks_scroll.pack(side="right", fill="y")
        self.tasks_canvas.create_window((0, 0), window=self.tasks_container, anchor="nw")

        # Привязка изменения размера контейнера к canvas
        self.tasks_container.bind("<Configure>",
                                  lambda e: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all")))

        # Привязка колеса мыши к прокрутке задач
        self.tasks_canvas.bind_all("<MouseWheel>", self.on_mousewheel_edit)

        # === Кнопка сохранения ===
        self.save_button_frame = ttk.Frame(self.edit_frame)
        self.save_button_frame.pack(side="bottom", fill="x", pady=5)

        self.save_btn = ttk.Button(self.save_button_frame, text="Сохранить изменения",
                                   command=lambda: self.save_tasks(self.file_selector.get()))
        self.save_btn.pack()

        # === Кнопка "Вернуться в меню" ===
        back_frame = ttk.Frame(self)
        back_frame.pack(side="bottom", fill="x", pady=10)

        tk.Button(back_frame, text="Вернуться в меню", font=("Arial", 12),
                  command=self.return_to_menu).pack()

        # === Первая загрузка задач ===
        self.task_files = {}
        self.current_task_list = []
        self.load_task_files()

    def on_mousewheel_edit(self, event):
        """Прокрутка через колесо мыши на вкладке 'Редактировать задачи'"""
        self.tasks_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def load_results_ui(self, parent):
        """Инициализация интерфейса вкладки 'Результаты'"""
        self.reports_container = ttk.Frame(parent)
        self.reports_container.pack(fill="both", expand=True)

        self.load_reports_button = ttk.Button(parent, text="Загрузить отчёты", command=self.load_reports)
        self.load_reports_button.pack(pady=5)

        # Canvas + Scrollbar для прокрутки списка отчётов
        self.reports_canvas = tk.Canvas(self.reports_container)
        self.reports_scroll = ttk.Scrollbar(self.reports_container, orient="vertical", command=self.reports_canvas.yview)
        self.reports_inner_frame = ttk.Frame(self.reports_canvas)

        self.reports_canvas.configure(yscrollcommand=self.reports_scroll.set)
        self.reports_scroll.pack(side="right", fill="y")
        self.reports_canvas.pack(side="left", fill="both", expand=True)
        self.reports_canvas.create_window((0, 0), window=self.reports_inner_frame, anchor="nw")

        # Обновляем регион прокрутки при изменении содержимого
        self.reports_inner_frame.bind("<Configure>",
                                      lambda e: self.reports_canvas.configure(scrollregion=self.reports_canvas.bbox("all")))

        # Привязка колеса мыши к прокрутке отчётов
        self.reports_canvas.bind_all("<MouseWheel>", self.on_mousewheel_report)

    def on_mousewheel_report(self, event):
        """Прокрутка вкладки 'Результаты' через колесо мыши"""
        self.reports_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def load_reports(self):
        reports = list_reports()
        for widget in self.reports_inner_frame.winfo_children():
            widget.destroy()

        if not reports:
            tk.Label(self.reports_inner_frame, text="Нет сохранённых отчётов", fg="gray").pack(pady=10)
            return

        for report in reports:
            frame = ttk.Frame(self.reports_inner_frame, borderwidth=1, relief="solid")
            frame.pack(fill="x", pady=2)

            tk.Label(frame, text=report, wraplength=400).pack(side="left", padx=5)
            tk.Button(frame, text="Открыть", width=8,
                      command=lambda f=report: self.open_report(f)).pack(side="right", padx=5)

    def open_report(self, filename):
        import webbrowser
        full_path = os.path.join("reports", filename)
        if os.path.exists(full_path):
            webbrowser.open(full_path)
        else:
            messagebox.showerror("Ошибка", "Файл не найден.")

    def load_task_files(self):
        task_dir = "tasks"
        if not os.path.exists(task_dir):
            os.makedirs(task_dir)

        files = [f for f in os.listdir(task_dir) if f.endswith(".json")]
        if not files:
            messagebox.showinfo("Информация", "Нет задач для редактирования.")
            return

        self.file_selector["values"] = files
        self.file_selector.current(0)
        self.file_selector.bind("<<ComboboxSelected>>", self.load_tasks)

    def load_tasks(self, event=None):
        from utils.helpers import clear_frame
        clear_frame(self.tasks_container)

        filename = self.file_selector.get()
        path = os.path.join("tasks", filename)

        try:
            with open(path, "r", encoding="utf-8") as f:
                self.current_task_list = json.load(f)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")
            return

        self.task_files[filename] = []

        for idx, task in enumerate(self.current_task_list):
            frame = ttk.Frame(self.tasks_container, borderwidth=1, relief="solid")
            frame.pack(fill="x", pady=5, padx=5)

            tk.Label(frame, text=f"Задача {idx + 1}", font=("Arial", 10, "bold")).pack(anchor="w")

            tk.Label(frame, text="Текст:").pack(anchor="w")
            entry_text = tk.Entry(frame, width=60)
            entry_text.insert(0, task.get("text", ""))
            entry_text.pack()

            tk.Label(frame, text="Правильный ответ:").pack(anchor="w")
            entry_answer = tk.Entry(frame, width=60)
            entry_answer.insert(0, str(task.get("correct_answer", "")))
            entry_answer.pack()

            tk.Label(frame, text="IRT параметры: a, b, c").pack(anchor="w")
            irt_frame = ttk.Frame(frame)
            irt_frame.pack(fill="x")

            entry_a = tk.Entry(irt_frame, width=10)
            entry_b = tk.Entry(irt_frame, width=10)
            entry_c = tk.Entry(irt_frame, width=10)

            irt = task.get("irt", {})
            entry_a.insert(0, str(irt.get("a", "")))
            entry_b.insert(0, str(irt.get("b", "")))
            entry_c.insert(0, str(irt.get("c", "")))

            entry_a.pack(side="left", padx=2)
            entry_b.pack(side="left", padx=2)
            entry_c.pack(side="left", padx=2)

            self.task_files[filename].append({
                "frame": frame,
                "text": entry_text,
                "answer": entry_answer,
                "a": entry_a,
                "b": entry_b,
                "c": entry_c,
            })

        # Обновляем регион прокрутки
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))

    def save_tasks(self, filename):
        path = os.path.join("tasks", filename)

        updated_tasks = []
        for idx, task_data in enumerate(self.task_files[filename]):
            original = self.current_task_list[idx]
            updated = {
                "id": original.get("id", f"task_{idx+1}"),
                "type": original.get("type", "unknown"),
                "text": task_data["text"].get(),
                "correct_answer": task_data["answer"].get(),
                "irt": {
                    "model": "3pl",
                    "a": float(task_data["a"].get()) if task_data["a"].get() else 1.0,
                    "b": float(task_data["b"].get()) if task_data["b"].get() else 0.0,
                    "c": float(task_data["c"].get()) if task_data["c"].get() else 0.2,
                }
            }
            updated_tasks.append(updated)

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(updated_tasks, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", "Задачи успешно сохранены.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

    def return_to_menu(self):
        """Чистый выход в главное меню"""
        self.pack_forget()
        self.destroy()

        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.show_main_menu()