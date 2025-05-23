# core/cat_engine.py

from .irt import log_likelihood, three_pl_model
import math

def estimate_theta(responses, items):
    low, high = -4, 4
    for _ in range(10):
        mid = (low + high) / 2
        ll_mid = log_likelihood(mid, responses, items)
        ll_low = log_likelihood(low, responses, items)
        if ll_mid > ll_low:
            low = mid
        else:
            high = mid
    return (low + high) / 2

def select_next_item(responses, items, used_ids, theta):
    max_info = -1
    next_item = None
    next_item_id = None
    for item_id, item in items.items():
        if item_id in used_ids:
            continue
        try:
            a = float(item['a'])
            b = float(item['b'])
            c = float(item['c'])
            p = three_pl_model(theta, a, b, c)
            info = a ** 2 * ((p - c) ** 2) / (p * (1 - p) + 1e-12)
            if info > max_info:
                max_info = info
                next_item = item
                next_item_id = item_id
        except:
            continue
    if next_item:
        used_ids.add(next_item_id)
        return next_item
    else:
        return None