# core/data_loader.py

import os
import json
from config import TASK_TYPES, TASKS_DIR

def load_all_items():
    items = {}
    for filename in os.listdir(TASKS_DIR):
        if filename.endswith('.json'):
            path = os.path.join(TASKS_DIR, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    if not isinstance(data, list):
                        print(f"[Ошибка] Файл {filename} должен содержать список задач.")
                        continue

                    for task in data:
                        if not isinstance(task, dict):
                            continue
                        item_id = task.get("id")
                        irt = task.get("irt", {})
                        if not all(k in irt for k in ['a', 'b', 'c']):
                            print(f"[Задача {item_id}] Отсутствуют IRT-параметры. Пропущено.")
                            continue
                        try:
                            a = float(irt['a'])
                            b = float(irt['b'])
                            c = float(irt['c'])
                            if not (0 < c < 1 and a > 0):
                                print(f"[Задача {item_id}] Некорректные IRT-параметры: a={a}, b={b}, c={c}. Пропущено.")
                                continue
                        except (TypeError, ValueError):
                            print(f"[Задача {item_id}] IRT-параметры не являются числами. Пропущено.")
                            continue

                        items[item_id] = {
                            "a": a,
                            "b": b,
                            "c": c,
                            "text": task.get("text", "[нет текста]"),
                            "correct_answer": str(task.get("correct_answer", "")),
                            "type": task.get("type", "unknown")
                        }
            except json.JSONDecodeError:
                print(f"[Ошибка] Не удалось прочитать файл {filename} — неверный формат JSON.")
            except Exception as e:
                print(f"[Ошибка] При обработке файла {filename}: {e}")
    return items