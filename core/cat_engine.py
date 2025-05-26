# # core/cat_engine.py

# from .irt import log_likelihood, three_pl_model
# import math

# def estimate_theta(responses, items):
#     low, high = -4, 4
#     for _ in range(10):
#         mid = (low + high) / 2
#         ll_mid = log_likelihood(mid, responses, items)
#         ll_low = log_likelihood(low, responses, items)
#         if ll_mid > ll_low:
#             low = mid
#         else:
#             high = mid
#     return (low + high) / 2


# def select_next_item(responses, items, used_ids, theta):
#     max_info = -1
#     next_item = None
#     next_item_id = None
#     for item_id, item in items.items():
#         if item_id in used_ids:
#             continue
#         try:
#             a = float(item['a'])
#             b = float(item['b'])
#             c = float(item['c'])
#             p = three_pl_model(theta, a, b, c)
#             info = a ** 2 * ((p - c) ** 2) / (p * (1 - p) + 1e-12)
#             if info > max_info:
#                 max_info = info
#                 next_item = item
#                 next_item_id = item_id
#         except:
#             continue
#     if next_item:
#         used_ids.add(next_item_id)
#         return next_item
#     else:
#         return None
    
# core/cat_engine.py

from .irt import log_likelihood, three_pl_model
import math


def estimate_theta(responses, items):
    """
    Оценивает theta методом максимального правдоподобия с использованием Ньютона-Рафсона
    """
    theta = 0.0
    for _ in range(10):  # до 10 итераций
        ll = log_likelihood(theta, responses, items)
        ll_p = log_likelihood(theta + 0.01, responses, items)
        ll_n = log_likelihood(theta - 0.01, responses, items)

        # Градиент и информация Фишера
        gradient = (ll_p - ll_n) / (0.02)
        curvature = (ll_p + ll_n - 2 * ll) / (0.01 ** 2)

        if curvature == 0:
            break

        # Обновление theta
        delta = -gradient / curvature
        theta += delta

        if abs(delta) < 0.01:
            break

    return theta


def item_info(theta, a, b, c):
    """Вычисляет информативность задачи при данном theta"""
    p = three_pl_model(theta, a, b, c)
    dp_dtheta = a * (1 - c) * (math.exp(-a * (theta - b))) / (1 + math.exp(-a * (theta - b)))**2
    info = (dp_dtheta ** 2) / (p * (1 - p))
    return info


def select_next_item(responses, items, used_ids, theta):
    """
    Выбирает следующую наиболее информативную задачу.
    responses: dict {item_id: True/False}
    items: dict {item_id: {a, b, c, text, ...}}
    used_ids: множество уже показанных задач
    theta: текущая оценка уровня знаний
    """
    best_item = None
    best_id = None
    max_info = -1

    for item_id, item in items.items():
        if item_id in used_ids:
            continue

        try:
            a = float(item.get("a", 1.0))
            b = float(item.get("b", 0.0))
            c = float(item.get("c", 0.2))

            # Получаем информативность задачи при текущем theta
            info = item_info(theta, a, b, c)

            if info > max_info:
                max_info = info
                best_item = item
                best_id = item_id

        except Exception as e:
            print(f"[Ошибка] Не удалось рассчитать информативность задачи: {e}")
            continue

    if best_id and best_item:
        used_ids.add(best_id)
        return best_item
    else:
        return None