# gui/student_mode.py

import tkinter as tk
from tkinter import ttk, messagebox
from core.cat_engine import select_next_item, estimate_theta
from utils.exporter import save_to_excel, save_to_pdf
from core.data_loader import load_all_items
from config import THETA_LEVELS


class StudentMode(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.student_name = tk.StringVar()

        # === Ввод имени ученика ===
        tk.Label(self, text="Введите ваше имя и фамилию:", font=("Arial", 14)).pack(pady=10)
        self.name_entry = tk.Entry(self, textvariable=self.student_name, width=40, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        self.start_button = tk.Button(self, text="Начать тест", command=self.start_test)
        self.start_button.pack(pady=10)

    def start_test(self):
        name = self.student_name.get().strip()
        if not name:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите имя и фамилию.")
            return

        self.destroy_widgets()

        # === Начало тестирования ===
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

    def create_widgets(self):
        self.question_label = tk.Label(self, text="", wraplength=500, justify="left", font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.answer_entry = tk.Entry(self, font=("Arial", 14), width=30)
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(self, text="Ответить", command=self.submit_answer)
        self.submit_button.pack(pady=10)

    def next_question(self):
        if self.current_step >= self.max_questions:
            self.finish_test()
            return

        item = select_next_item(self.responses, self.items, self.used_ids, self.theta)
        if not item:
            self.finish_test()
            return

        self.current_item = item
        self.question_label.config(text=item["text"])
        self.answer_entry.delete(0, tk.END)
        self.current_step += 1

    def submit_answer(self):
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

    def finish_test(self):
        # Удаляем все текущие виджеты
        for widget in self.winfo_children():
            widget.destroy()

        level = get_theta_level(self.theta)
        task_analysis = analyze_by_type(self.responses, self.items)

        # === Блок с результатами ===
        tk.Label(self, text="Тест завершён!", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self, text=f"Уровень знаний: {level}", font=("Arial", 14)).pack(pady=5)

        tk.Label(self, text="Анализ по темам:", font=("Arial", 12, "underline")).pack(pady=5)
        for t, score in task_analysis.items():
            tk.Label(self, text=f"{t}: {'%.0f%%' % (score * 100)} правильных ответов").pack()

        # === Кнопки ===
        tk.Button(self, text="Сохранить в Excel",
                command=lambda: save_to_excel(self.questions, self.theta_history, task_analysis, student_name=self.name)).pack(pady=5)
        tk.Button(self, text="Сохранить в PDF",
                command=lambda: save_to_pdf(self.theta, self.theta_history,
                                            {"level": level, "text": "Рекомендация: продолжайте практиковаться!"},
                                            task_analysis, student_name=self.name)).pack(pady=5)

        tk.Button(self, text="Вернуться в меню", command=self.return_to_menu).pack(pady=10)
        tk.Button(self, text="Пройти тест снова", command=self.restart_test).pack(pady=5)


    def return_to_menu(self):
        """Чисто возвращаемся в главное меню"""
        self.pack_forget()  # Отвязываем текущий фрейм
        self.destroy()      # Уничтожаем текущий StudentMode

        # Очищаем всё содержимое главного окна
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.show_main_menu()  # Показываем главное меню

    def restart_test(self):
        """Перезапуск теста"""
        self.pack_forget()  # Отвязываем от layout
        self.destroy()      # Уничтожаем текущий фрейм
        StudentMode(self.master).pack(fill="both", expand=True)  # Создаём новый и прикрепляем

    



def get_theta_level(theta):
    for level, (low, high) in THETA_LEVELS.items():
        if low <= theta < high:
            return level
    return "Неизвестный уровень"


def analyze_by_type(responses, items):
    from collections import defaultdict
    scores = defaultdict(list)
    for item_id, correct in responses.items():
        item = items.get(item_id)
        if not item:
            continue
        task_type = item["type"]
        scores[task_type].append(correct)
    result = {}
    for t, answers in scores.items():
        result[t] = sum(answers) / len(answers) if answers else 0
    return result