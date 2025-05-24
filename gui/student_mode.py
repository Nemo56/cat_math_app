# gui/student_mode.py

import tkinter as tk
from tkinter import ttk, messagebox
from core.cat_engine import select_next_item, estimate_theta
from utils.exporter import save_to_excel, save_to_pdf
from core.data_loader import load_all_items
from config import THETA_LEVELS

# class StudentMode(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.master = master

#         # === Сброс состояния ===
#         self.reset_state()

#         # === Начальный интерфейс ввода имени ===
#         tk.Label(self, text="Введите ваше имя и фамилию:", font=("Arial", 14)).pack(pady=10)

#         self.name_entry = tk.Entry(self, textvariable=self.student_name, width=40, font=("Arial", 12))
#         self.name_entry.pack(pady=5)

#         self.start_button = tk.Button(self, text="Начать тест", command=self.start_test)
#         self.start_button.pack(pady=10)

#     def reset_state(self):
#         """Сброс всех переменных перед началом теста"""
#         self.student_name = tk.StringVar()
#         self.items = {}
#         self.used_ids = set()
#         self.responses = {}
#         self.theta = 0.0
#         self.theta_history = [self.theta]
#         self.questions = []
#         self.current_step = 0
#         self.max_questions = 10

# gui/student_mode.py

class StudentMode(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.reset_state()

        # === Начальный интерфейс ввода имени ===
        tk.Label(self, text="Введите ваше имя и фамилию:", font=("Arial", 14)).pack(pady=10)

        self.name_entry = tk.Entry(self, textvariable=self.student_name, width=40, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        self.start_button = tk.Button(self, text="Начать тест", command=self.start_test)
        self.start_button.pack(pady=10)

    def reset_state(self):
        """Сброс всех переменных перед началом теста"""
        self.student_name = tk.StringVar()
        self.items = {}
        self.used_ids = set()
        self.responses = {}
        self.theta = 0.0
        self.theta_history = [self.theta]
        self.questions = []
        self.current_step = 0
        self.max_questions = 10
        self.remaining_time = 1200  # 20 минут = 1200 секунд
        self.timer_id = None

    def start_test(self):
        name = self.student_name.get().strip()
        if not name:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите имя и фамилию.")
            return

        self.destroy_widgets()

        self.items = load_all_items()
        if not self.items:
            tk.Label(self, text="Ошибка: не найдены задачи.", fg="red").pack()
            tk.Button(self, text="Назад", command=self.master.show_main_menu).pack()
            return

        self.name = name
        self.used_ids = set()
        self.responses = {}
        self.theta = 0.0
        self.theta_history = [self.theta]
        self.questions = []
        self.current_step = 0
        self.max_questions = 10

        self.create_widgets()
        self.next_question()

    def destroy_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    # def create_widgets(self):
    #     # === Прогресс-бар ===
    #     self.progress_frame = ttk.Frame(self)
    #     self.progress_frame.pack(fill="x", padx=20, pady=10)

    #     self.progress_label = tk.Label(self.progress_frame,
    #                                    text=f"Задача {self.current_step + 1} из {self.max_questions}",
    #                                    font=("Arial", 12))
    #     self.progress_label.pack(side="left")

    #     self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=300, mode="determinate")
    #     self.progress.pack(side="left", padx=10, expand=True, fill="x")
    #     self.progress["maximum"] = self.max_questions
    #     self.progress["value"] = self.current_step

    #     # === Вопрос ===
    #     self.question_label = tk.Label(self, text="", wraplength=500, justify="left", font=("Arial", 14))
    #     self.question_label.pack(pady=20)

    #     # === Поле ввода ответа ===
    #     self.answer_entry = tk.Entry(self, font=("Arial", 14), width=30)
    #     self.answer_entry.pack(pady=10)

    #     # === Кнопка "Ответить" ===
    #     self.submit_button = tk.Button(self, text="Ответить", command=self.submit_answer)
    #     self.submit_button.pack(pady=10)

    #     # === Кнопка "Пропустить" ===
    #     self.skip_button = tk.Button(self, text="Пропустить задание", command=self.skip_question)
    #     self.skip_button.pack(pady=5)

    def create_widgets(self):
        # === Прогресс-бар ===
        self.progress_frame = ttk.Frame(self)
        self.progress_frame.pack(fill="x", padx=20, pady=10)

        self.progress_label = tk.Label(self.progress_frame,
                                    text=f"Задача {self.current_step + 1} из {self.max_questions}",
                                    font=("Arial", 12))
        self.progress_label.pack(side="left")

        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(side="left", padx=10, expand=True, fill="x")
        self.progress["maximum"] = self.max_questions
        self.progress["value"] = self.current_step

        # === Таймер ===
        self.timer_label = tk.Label(self, text="", font=("Arial", 12), fg="red")
        self.timer_label.pack(pady=5)

        # === Вопрос ===
        self.question_label = tk.Label(self, text="", wraplength=500, justify="left", font=("Arial", 14))
        self.question_label.pack(pady=20)

        # === Поле ввода ответа ===
        self.answer_entry = tk.Entry(self, font=("Arial", 14), width=30)
        self.answer_entry.pack(pady=10)

        # === Кнопки ===
        self.submit_button = tk.Button(self, text="Ответить", command=self.submit_answer)
        self.submit_button.pack(pady=10)

        self.skip_button = tk.Button(self, text="Пропустить задание", command=self.skip_question)
        self.skip_button.pack(pady=5)

        # === Запуск таймера ===
        self.update_timer()

    # def next_question(self):
    #     if self.current_step >= self.max_questions:
    #         self.finish_test()
    #         return

    #     item = select_next_item(self.responses, self.items, self.used_ids, self.theta)
    #     if not item:
    #         self.finish_test()
    #         return

    #     self.current_item = item
    #     self.question_label.config(text=item["text"])
    #     self.answer_entry.delete(0, tk.END)
    #     self.current_step += 1

    #     # Обновляем прогресс-бар
    #     self.progress["value"] = self.current_step
    #     self.progress_label.config(text=f"Задача {self.current_step + 1} из {self.max_questions}")

    def next_question(self):
        if self.current_step >= self.max_questions:
            self.finish_test()
            return

        item = select_next_item(self.responses, self.items, self.used_ids, self.theta)
        if not item:
            self.finish_test()
            return

        self.current_item = item  # ← Убедитесь, что это назначение происходит
        self.question_label.config(text=item["text"])
        self.answer_entry.delete(0, tk.END)
        self.current_step += 1

        self.progress["value"] = self.current_step
        self.progress_label.config(text=f"Задача {self.current_step + 1} из {self.max_questions}")

    # def submit_answer(self):
    #     user_answer = self.answer_entry.get().strip()
    #     correct = user_answer == self.current_item["correct_answer"].strip()
    #     item_id = list(self.used_ids)[-1]
    #     self.responses[item_id] = correct

    #     self.questions.append({
    #         "ученик": self.name,
    #         "номер": self.current_step,
    #         "текст": self.current_item['text'],
    #         "ответ пользователя": user_answer,
    #         "верный ответ": self.current_item["correct_answer"],
    #         "тип": self.current_item.get("type", "unknown"),
    #         "правильно": correct
    #     })

    #     self.theta = estimate_theta(self.responses, self.items)
    #     self.theta_history.append(self.theta)
    #     self.next_question()

    # def skip_question(self):
    #     """Ученик пропускает текущее задание"""
    #     self.questions.append({
    #         "ученик": self.name,
    #         "номер": self.current_step,
    #         "текст": self.current_item['text'],
    #         "ответ пользователя": "[пропущено]",
    #         "верный ответ": self.current_item["correct_answer"],
    #         "тип": self.current_item.get("type", "unknown"),
    #         "правильно": None  # Не оценивается
    #     })

    #     self.theta_history.append(self.theta)  # Текущая оценка остается без изменений
    #     self.next_question()


    def submit_answer(self):
        if not hasattr(self, 'current_item') or self.current_item is None:
            messagebox.showwarning("Ошибка", "Нет активного задания для ответа.")
            return

        user_answer = self.answer_entry.get().strip()
        correct = user_answer == self.current_item["correct_answer"].strip()
        item_id = list(self.used_ids)[-1]
        self.responses[item_id] = correct

        self.questions.append({
            "ученик": self.name,
            "номер": self.current_step,
            "текст": self.current_item['text'],
            "ответ пользователя": user_answer,
            "верный ответ": self.current_item["correct_answer"],
            "тип": self.current_item.get("type", "unknown"),
            "правильно": correct
        })

        self.theta = estimate_theta(self.responses, self.items)
        self.theta_history.append(self.theta)
        self.next_question()
 

    def skip_question(self):
        """Пропуск задания"""
        if not hasattr(self, 'current_item') or self.current_item is None:
            messagebox.showwarning("Предупреждение", "Нет текущего задания для пропуска.")
            return

        self.questions.append({
            "ученик": self.name,
            "номер": self.current_step,
            "текст": self.current_item['text'],
            "ответ пользователя": "[пропущено]",
            "верный ответ": self.current_item["correct_answer"],
            "тип": self.current_item.get("type", "unknown"),
            "правильно": None
        })

        self.theta_history.append(self.theta)  # Не меняем уровень знаний
        self.next_question()

    # def finish_test(self):
    #     self.destroy_widgets()

    #     level = get_theta_level(self.theta)
    #     task_analysis = analyze_by_type(self.responses, self.items)

    #     # === Блок с результатами ===
    #     tk.Label(self, text="Тест завершён!", font=("Arial", 16, "bold")).pack(pady=10)
    #     tk.Label(self, text=f"Уровень знаний: {level}", font=("Arial", 14)).pack(pady=5)

    #     tk.Label(self, text="Анализ по темам:", font=("Arial", 12, "underline")).pack(pady=5)
    #     for t, score in task_analysis.items():
    #         tk.Label(self, text=f"{t}: {'%.0f%%' % (score * 100)} правильных ответов").pack()

    #     # === Кнопки ===
    #     tk.Button(self, text="Сохранить в Excel",
    #               command=lambda: save_to_excel(self.questions, self.theta_history, task_analysis, student_name=self.name)).pack(pady=5)
    #     tk.Button(self, text="Сохранить в PDF",
    #               command=lambda: save_to_pdf(self.theta, self.theta_history,
    #                                          {"level": level, "text": "Рекомендация: продолжайте практиковаться!"},
    #                                          task_analysis, student_name=self.name)).pack(pady=5)

    #     tk.Button(self, text="Вернуться в меню", command=self.return_to_menu).pack(pady=10)
    #     tk.Button(self, text="Пройти тест снова", command=self.restart_test).pack(pady=5)

    def finish_test(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        self.destroy_widgets()

        level = get_theta_level(self.theta)
        task_analysis = analyze_by_type(self.responses, self.items)

        tk.Label(self, text="Тест завершён!", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self, text=f"Уровень знаний: {level}", font=("Arial", 14)).pack(pady=5)

        tk.Label(self, text="Анализ по темам:", font=("Arial", 12, "underline")).pack(pady=5)
        for t, score in task_analysis.items():
            tk.Label(self, text=f"{t}: {'%.0f%%' % (score * 100)} правильных ответов").pack()

        tk.Button(self, text="Сохранить в Excel",
                command=lambda: save_to_excel(self.questions, self.theta_history, task_analysis, student_name=self.name)).pack(pady=5)
        tk.Button(self, text="Сохранить в PDF",
                command=lambda: save_to_pdf(self.theta, self.theta_history,
                                            {"level": level, "text": "Рекомендация: продолжайте практиковаться!"},
                                            task_analysis, student_name=self.name)).pack(pady=5)

        tk.Button(self, text="Вернуться в меню", command=self.return_to_menu).pack(pady=10)
        tk.Button(self, text="Пройти тест снова", command=self.restart_test).pack(pady=5)

    def return_to_menu(self):
        self.pack_forget()
        self.destroy()
        for widget in self.master.winfo_children():
            widget.destroy()
        self.master.show_main_menu()

    def restart_test(self):
        self.pack_forget()
        self.destroy()
        StudentMode(self.master).pack(fill="both", expand=True)

    def destroy_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def update_timer(self):
        """Обновление таймера каждую секунду"""
        if self.remaining_time <= 0:
            self.finish_test()
            messagebox.showinfo("Время истекло", "Время на выполнение теста истекло.")
            return

        mins, secs = divmod(self.remaining_time, 60)
        time_format = f"{mins:02d}:{secs:02d}"
        self.timer_label.config(text=f"Оставшееся время: {time_format}")
        self.remaining_time -= 1
        self.timer_id = self.after(1000, self.update_timer)

def get_theta_level(theta):
    for level, (low, high) in THETA_LEVELS.items():
        if low <= theta < high:
            return level
    return "Неизвестный уровень"


def analyze_by_type(responses, items):
    from collections import defaultdict
    scores = defaultdict(list)
    for item_id, correct in responses.items():
        if correct is None:
            continue  # Пропущенные задания не влияют на анализ
        item = items.get(item_id)
        if not item:
            continue
        task_type = item["type"]
        scores[task_type].append(correct)
    result = {}
    for t, answers in scores.items():
        result[t] = sum(answers) / len(answers) if answers else 0
    return result

