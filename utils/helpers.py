# # utils/helpers.py

# import os

# def list_reports():
#     report_dir = "reports"
#     if not os.path.exists(report_dir):
#         os.makedirs(report_dir)
#     return os.listdir(report_dir)

# def clear_frame(frame):
#     for widget in frame.winfo_children():
#         widget.destroy()

        # utils/helpers.py

# import os

# def list_reports():
#     report_dir = "reports"
#     if not os.path.exists(report_dir):
#         os.makedirs(report_dir)
#     return [f for f in os.listdir(report_dir) if f.endswith((".xlsx", ".pdf"))]


# def clear_frame(frame):
#     for widget in frame.winfo_children():
#         widget.destroy()


# utils/helpers.py

# import os

# def list_reports():
#     report_dir = "reports"
#     if not os.path.exists(report_dir):
#         os.makedirs(report_dir)
#     try:
#         files = [f for f in os.listdir(report_dir) if f.endswith(('.xlsx', '.pdf'))]
#         return sorted(files)
#     except Exception as e:
#         print(f"[Ошибка] Не удалось прочитать папку reports: {e}")
#         return []

# def clear_frame(frame):
#     for widget in frame.winfo_children():
#         widget.destroy()

# # utils/helpers.py

import os


def list_reports():
    """Возвращает список всех отчётов из папки reports"""
    report_dir = "reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # Ищем во всех подпапках (excel, pdf)
    files = []
    for root, _, filenames in os.walk(report_dir):
        for f in filenames:
            if f.endswith(('.xlsx', '.pdf')):
                rel_path = os.path.relpath(os.path.join(root, f), report_dir)
                files.append(rel_path)

    return sorted(files)  # Сортируем для удобства


def clear_frame(frame):
    """Очистка фрейма от виджетов"""
    for widget in frame.winfo_children():
        widget.destroy()