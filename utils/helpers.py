

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
