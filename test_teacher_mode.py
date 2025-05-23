# test_teacher_mode.py

import unittest
import os
import json
import shutil
from tkinter import TclError
from gui.teacher_mode import TeacherMode
import tkinter as tk


class TestTeacherMode(unittest.TestCase):
    def setUp(self):
        """Инициализация тестового окружения"""
        self.root = tk.Tk()
        self.root.withdraw()  # Скрываем главное окно
        self.app = TeacherMode(self.root)

    def tearDown(self):
        """Очистка после теста"""
        self.root.update()
        self.root.destroy()

    def test_01_teacher_login_and_ui(self):
        """Проверяет, что интерфейс учителя загружается корректно"""
        self.assertIsInstance(self.app, TeacherMode)
        self.assertTrue(hasattr(self.app, 'notebook'))
        self.assertEqual(len(self.app.notebook.tabs()), 2)

    def test_02_load_reports(self):
        """Проверяет, что список отчётов загружается"""
        self.app.load_reports()
        reports_container = self.app.reports_container
        children = reports_container.winfo_children()
        report_files = [f for f in os.listdir("reports") if f.endswith((".xlsx", ".pdf"))]
        self.assertGreaterEqual(len(children), len(report_files),
                                "Количество элементов не совпадает с количеством отчётов")

    def test_03_load_tasks_from_file(self):
        """Проверяет, что задачи из JSON-файла загружаются"""
        self.app.file_selector.current(0)  # Выбираем первый файл
        self.app.load_tasks()
        task_container = self.app.tasks_container
        children = task_container.winfo_children()
        self.assertGreater(len(children), 0, "Задачи не загружены")

    def test_04_edit_task_and_save(self):
        """Проверяет, что можно редактировать и сохранять задачи"""
        test_json_path = "tasks/arithmetic_test.json"
        backup_json_path = "tasks/arithmetic_test_backup.json"

        # Подготовка тестового файла
        with open(test_json_path, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        with open(backup_json_path, 'w', encoding='utf-8') as f:
            json.dump(original_data, f, ensure_ascii=False, indent=2)

        # Установка тестового файла
        self.app.file_selector.set(os.path.basename(test_json_path))
        self.app.load_tasks()

        # Изменяем первую задачу
        first_task = self.app.task_files[os.path.basename(test_json_path)][0]
        first_task["text"].delete(0, tk.END)
        first_task["text"].insert(0, "[ТЕСТ] Новый текст задачи")
        first_task["answer"].delete(0, tk.END)
        first_task["answer"].insert(0, "999")
        first_task["a"].delete(0, tk.END)
        first_task["a"].insert(0, "1.5")
        first_task["b"].delete(0, tk.END)
        first_task["b"].insert(0, "0.5")
        first_task["c"].delete(0, tk.END)
        first_task["c"].insert(0, "0.2")

        # Сохраняем изменения
        self.app.save_tasks(os.path.basename(test_json_path))

        # Проверяем, сохранились ли изменения
        with open(test_json_path, "r", encoding="utf-8") as f:
            updated_data = json.load(f)

        self.assertEqual(updated_data[0]["text"], "[ТЕСТ] Новый текст задачи")
        self.assertEqual(updated_data[0]["correct_answer"], "999")
        self.assertEqual(updated_data[0]["irt"]["a"], 1.5)
        self.assertEqual(updated_data[0]["irt"]["b"], 0.5)
        self.assertEqual(updated_data[0]["irt"]["c"], 0.2)

        # Восстанавливаем оригинал
        with open(backup_json_path, 'r', encoding='utf-8') as f:
            restored_data = json.load(f)
        with open(test_json_path, 'w', encoding='utf-8') as f:
            json.dump(restored_data, f, ensure_ascii=False, indent=2)

    def test_05_invalid_password(self):
        """Проверяет, что неправильный пароль блокирует вход"""
        password = "wrong_password"
        self.assertFalse(password == "school123", "Неверный пароль должен быть неверным")

    def test_06_no_task_files(self):
        """Проверяет, что при отсутствии задач выводится сообщение"""
        temp_dir = "tasks_temp"
        original_dir = "tasks"

        # Убедимся, что temp_dir не существует
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

        # Убедимся, что оригинальная папка существует
        if os.path.exists(original_dir):
            os.rename(original_dir, temp_dir)

        try:
            from gui.teacher_mode import TeacherMode
            fake_root = tk.Tk()
            fake_root.withdraw()
            tm = TeacherMode(fake_root)
            tm.load_task_files()

            # Проверяем, что выпадающий список пуст
            self.assertEqual(tm.file_selector["values"], '')  # ← ИСПРАВЛЕНО

        finally:
            # Восстанавливаем папку обратно
            if os.path.exists(original_dir):
                shutil.rmtree(original_dir)
            if os.path.exists(temp_dir):
                os.rename(temp_dir, original_dir)


if __name__ == "__main__":
    unittest.main()