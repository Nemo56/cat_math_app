# config.py

import os

MAX_QUESTIONS = 10
THETA_LEVELS = {
    "Очень низкий": (-float('inf'), -2.0),
    "Низкий": (-2.0, -1.0),
    "Ниже среднего": (-1.0, -0.5),
    "Средний": (-0.5, 0.5),
    "Выше среднего": (0.5, 1.0),
    "Высокий": (1.0, 2.0),
    "Очень высокий": (2.0, float('inf'))
}

TEACHER_PASSWORD = "school123"
TASK_TYPES = ['arithmetic', 'geometry', 'fractions', 'word_problem', 'equation', 'comparison', 'table']

REPORTS_DIR = "reports"
EXCEL_DIR = os.path.join(REPORTS_DIR, "excel")
PDF_DIR = os.path.join(REPORTS_DIR, "pdf")
TASKS_DIR = "tasks"



THEME_FILE = "theme.json"
DEFAULT_THEME = "light"  # или "dark", "accent"