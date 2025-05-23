# test_logic.py

import os
import json
from core.data_loader import load_all_items
from core.cat_engine import select_next_item, estimate_theta
from utils.exporter import save_to_excel, save_to_pdf
from config import THETA_LEVELS

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

def run_test(max_questions=5):
    items = load_all_items()
    if not items:
        print("❌ Нет доступных заданий.")
        return

    used_ids = set()
    responses = {}
    theta = 0.0
    theta_history = [theta]
    questions = []

    print("=== Тестирование началось ===\n")

    for step in range(1, max_questions + 1):
        item = select_next_item(responses, items, used_ids, theta)
        if not item:
            print("⚠️ Нет доступных заданий.")
            break

        print(f"\nВопрос {step}: {item['text']}")
        user_answer = input("Ваш ответ: ").strip()

        correct = user_answer == item["correct_answer"].strip()
        item_id = list(used_ids)[-1]
        responses[item_id] = correct
        questions.append({
            "номер": step,
            "текст": item['text'],
            "ответ пользователя": user_answer,
            "верный ответ": item["correct_answer"],
            "тип": item.get("type", "unknown"),
            "правильно": correct
        })

        theta = estimate_theta(responses, items)
        theta_history.append(theta)
        print(f"📈 Текущая оценка θ: {theta:.2f}")

    print("\n✅ Тест завершён")
    level = get_theta_level(theta)
    print(f"📊 Уровень знаний: {level}")

    # Анализ по типам заданий
    task_analysis = analyze_by_type(responses, items)
    print("\n🔍 Анализ по темам:")
    for task_type, score in task_analysis.items():
        print(f"- {task_type}: {'%.0f%%' % (score * 100)} правильных ответов")

    # Экспорт данных
    os.makedirs("reports/excel", exist_ok=True)
    os.makedirs("reports/pdf", exist_ok=True)

    excel_path = save_to_excel(questions, theta_history, task_analysis)
    pdf_path = save_to_pdf(theta, theta_history, {"level": level, "text": "Рекомендация: продолжайте практиковаться!"}, task_analysis)

    print(f"\n📁 Отчёты сохранены:")
    print(f"- Excel: {excel_path}")
    print(f"- PDF: {pdf_path}")


if __name__ == "__main__":
    run_test()