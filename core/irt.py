# core/irt.py

import math

def three_pl_model(theta, a, b, c):
    return c + (1 - c) / (1 + math.exp(-a * (theta - b)))

def log_likelihood(theta, responses, items):
    log_like = 0.0
    for item_id, correct in responses.items():
        if item_id not in items:
            continue
        item = items[item_id]
        a, b, c = item['a'], item['b'], item['c']
        p = three_pl_model(theta, a, b, c)
        if correct:
            log_like += math.log(p + 1e-12)
        else:
            log_like += math.log(1 - p + 1e-12)
    return log_like