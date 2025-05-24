
# # utils/exporter.py

# import os
# from datetime import datetime
# import matplotlib.pyplot as plt
# import pandas as pd
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors


# def save_to_excel(data, theta_history, task_analysis, student_name=None, test_duration=None):
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M")
#     filename = f"test_{student_name.replace(' ', '_')}_{timestamp}.xlsx"
#     path = os.path.join("reports/excel", filename)

#     df = pd.DataFrame(data)
#     if test_duration:
#         df["Время прохождения"] = test_duration

#     df.to_excel(path, index=False)

#     # Сохраняем историю theta
#     df_theta = pd.DataFrame({"Theta": theta_history})
#     with pd.ExcelWriter(path, mode="a", engine="openpyxl") as writer:
#         df_theta.to_excel(writer, sheet_name="Theta", index=False)

#     return path


# def save_to_pdf(theta, theta_history, recommendations, task_analysis, student_name=None, test_duration=None, questions=None):
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M")

#     if not student_name or student_name.strip() == "":
#         student_name = "Неизвестный_ученик"

#     filename = f"test_{student_name}_{timestamp}.pdf"
#     path = os.path.join("reports/pdf", filename)

#     doc = SimpleDocTemplate(path)
#     styles = getSampleStyleSheet()
#     flowables = []

#     # === Заголовок ===
#     flowables.append(Paragraph(f"<b>Результаты тестирования</b>", styles['Title']))
#     flowables.append(Spacer(1, 12))
#     flowables.append(Paragraph(f"<b>Ученик:</b> {student_name}", styles['Normal']))
#     flowables.append(Paragraph(f"<b>Дата и время теста:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}", styles['Normal']))
#     flowables.append(Paragraph(f"<b>Время прохождения:</b> {test_duration} мин.", styles['Normal']))
#     flowables.append(Spacer(1, 24))

#     # === Общая оценка ===
#     flowables.append(Paragraph("<b>Итоговая оценка уровня знаний</b>", styles['Heading2']))
#     flowables.append(Paragraph(f"<b>Тета (θ):</b> {theta:.2f}", styles['Normal']))
#     flowables.append(Paragraph(f"<b>Уровень знаний:</b> {recommendations.get('level', 'Не определён')}", styles['Normal']))
#     flowables.append(Paragraph(f"<b>Рекомендации:</b> {recommendations.get('text', 'Нет данных.')}", styles['Normal']))
#     flowables.append(Spacer(1, 24))

#     # === Статистика по типам задач ===
#     flowables.append(Paragraph("<b>Статистика по типам задач</b>", styles['Heading2']))
#     data = [["Тип задачи", "Правильных ответов (%)"]]
#     for t, score in task_analysis.items():
#         data.append([t, f"{score * 100:.0f}%"])

#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('FONTSIZE', (0, 0), (-1, 0), 12),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ]))
#     flowables.append(table)
#     flowables.append(Spacer(1, 24))

#     # === Список всех вопросов ===
#     flowables.append(Paragraph("<b>Список пройденных задач</b>", styles['Heading2']))

#     question_data = [["#", "Задача", "Ваш ответ", "Верный ответ", "Правильно?"]]
#     for idx, q in enumerate(questions):
#         correct = q.get("правильно", None)
#         correct_str = "Да" if correct is True else ("Нет" if correct is False else "[пропущено]")
#         question_data.append([
#             str(idx + 1),
#             q.get("текст", ""),
#             q.get("ответ пользователя", ""),
#             q.get("верный ответ", ""),
#             correct_str
#         ])

#     question_table = Table(question_data, colWidths=[30, 200, 80, 80, 60])
#     question_table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('FONTSIZE', (0, 0), (-1, 0), 12),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('TOPPADDING', (0, 1), (-1, -1), 6),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ]))
#     flowables.append(question_table)
#     flowables.append(Spacer(1, 24))

#     # === График изменения θ ===
#     plt.figure(figsize=(8, 5))
#     plt.plot(range(len(theta_history)), theta_history, marker='o', linestyle='-')
#     plt.title('Изменение уровня способности θ по ходу теста')
#     plt.xlabel('Номер вопроса')
#     plt.ylabel('θ')
#     plt.grid(True)
#     plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)
#     plt.savefig("temp_plot.png")
#     plt.close()

#     flowables.append(Paragraph("<b>График уровня знаний θ</b>", styles['Heading2']))
#     flowables.append(Paragraph("Динамика уровня способности ученика по мере прохождения теста:", styles['Normal']))
#     flowables.append(Image("temp_plot.png"))
#     flowables.append(Spacer(1, 24))

#     # === Графики по типам задач ===
#     from collections import defaultdict
#     type_theta = defaultdict(list)
#     cumulative_theta = 0.0
#     count = 0

#     for q in questions:
#         task_type = q.get("тип", "unknown")
#         response = q.get("правильно", None)
#         if response is not None:
#             count += 1
#             if count > 0:
#                 cumulative_theta += theta_history[count]
#                 type_theta[task_type].append(response)

#     # === График θ по типам задач (среднее) ===
#     if type_theta:
#         labels = []
#         scores = []
#         for t, responses in type_theta.items():
#             avg = sum(responses) / len(responses)
#             labels.append(t)
#             scores.append(avg)

#         plt.figure(figsize=(8, 5))
#         plt.bar(labels, [s * 100 for s in scores], color='skyblue')
#         plt.title('Уровень знаний по типам задач')
#         plt.ylabel('Процент правильных ответов')
#         plt.xticks(rotation=45)
#         plt.tight_layout()
#         plt.savefig("temp_plot_by_type.png")
#         plt.close()

#         flowables.append(Paragraph("<b>График по типам задач</b>", styles['Heading2']))
#         flowables.append(Paragraph("Распределение правильных ответов по темам:", styles['Normal']))
#         flowables.append(Image("temp_plot_by_type.png"))
#         flowables.append(Spacer(1, 24))

#     # === Подпись ===
#     flowables.append(Paragraph("Конец отчёта", styles['Normal']))

#     # === Генерация PDF ===
#     doc.build(flowables)
#     return path

# utils/exporter.py

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from collections import defaultdict


# === Регистрация шрифта для кириллицы (PDF) ===
try:
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSerif.ttf'))
except Exception as e:
    print(f"[Предупреждение] Не удалось загрузить шрифт DejaVu: {e}")
    # Используем стандартный шрифт, если нет файла
    pass


# === Сохранение в Excel ===
def save_to_excel(data, theta_history, task_analysis, student_name=None, test_duration=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"test_{student_name}_{timestamp}.xlsx"
    path = os.path.join("reports/excel", filename)

    df = pd.DataFrame(data)
    if test_duration:
        df["Время прохождения"] = test_duration

    df.to_excel(path, index=False)

    # Добавляем Theta
    df_theta = pd.DataFrame({"Theta": theta_history})
    with pd.ExcelWriter(path, mode="a", engine="openpyxl") as writer:
        df_theta.to_excel(writer, sheet_name="Theta", index=False)

    return path


# === Сохранение в PDF ===
def save_to_pdf(theta, theta_history, recommendations, task_analysis, student_name=None, test_duration=None, questions=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    if not student_name or student_name.strip() == "":
        student_name = "Неизвестный_ученик"

    filename = f"test_{student_name}_{timestamp}.pdf"
    path = os.path.join("reports/pdf", filename)

    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    # Применяем шрифт с поддержкой кириллицы
    for style in styles.byName.values():
        try:
            style.fontName = 'DejaVu'
        except:
            pass

    flowables = []

    # Заголовок
    flowables.append(Paragraph("<b>Результаты тестирования</b>", styles['Title']))
    flowables.append(Spacer(1, 12))
    flowables.append(Paragraph(f"<b>Ученик:</b> {student_name}", styles['Normal']))
    flowables.append(Paragraph(f"<b>Дата и время теста:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}", styles['Normal']))
    flowables.append(Paragraph(f"<b>Время прохождения:</b> {test_duration} мин.", styles['Normal']))
    flowables.append(Spacer(1, 24))

    # Общая оценка
    flowables.append(Paragraph("<b>Итоговая оценка уровня знаний</b>", styles['Heading2']))
    flowables.append(Paragraph(f"<b>Тета (θ):</b> {theta:.2f}", styles['Normal']))
    flowables.append(Paragraph(f"<b>Уровень знаний:</b> {recommendations.get('level', 'Не определён')}", styles['Normal']))
    flowables.append(Paragraph(f"<b>Рекомендации:</b> {recommendations.get('text', 'Нет данных.')}", styles['Normal']))
    flowables.append(Spacer(1, 24))

    # Статистика по типам задач
    flowables.append(Paragraph("<b>Статистика по типам задач</b>", styles['Heading2']))
    data = [["Тип задачи", "Правильных ответов (%)"]]
    for t, score in task_analysis.items():
        data.append([t, f"{score * 100:.0f}%"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu')
    ]))
    flowables.append(table)
    flowables.append(Spacer(1, 24))

    # Список вопросов
    flowables.append(Paragraph("<b>Список пройденных задач</b>", styles['Heading2']))
    question_data = [["#", "Задача", "Ваш ответ", "Верный ответ", "Правильно?"]]
    for idx, q in enumerate(questions):
        correct = q.get("правильно", None)
        correct_str = "Да" if correct is True else ("Нет" if correct is False else "[пропущено]")
        question_data.append([
            str(idx + 1),
            q.get("текст", ""),
            q.get("ответ пользователя", ""),
            q.get("верный ответ", ""),
            correct_str
        ])

    question_table = Table(question_data, colWidths=[30, 150, 80, 80, 60])
    question_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVu')
    ]))
    flowables.append(question_table)
    flowables.append(Spacer(1, 24))

    # График θ
    plt.figure(figsize=(8, 5))
    plt.plot(range(len(theta_history)), theta_history, marker='o', linestyle='-')
    plt.title('Изменение уровня способности θ по ходу теста')
    plt.xlabel('Номер вопроса')
    plt.ylabel('θ')
    plt.grid(True)
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)
    plt.savefig("temp_plot.png")
    plt.close()

    flowables.append(Paragraph("<b>График уровня знаний θ</b>", styles['Heading2']))
    flowables.append(Paragraph("Динамика уровня способности ученика:", styles['Normal']))
    flowables.append(Image("temp_plot.png"))
    flowables.append(Spacer(1, 24))

    # График по типам задач
    type_scores = defaultdict(list)
    for q in questions:
        task_type = q.get("тип", "unknown")
        response = q.get("правильно", None)
        if response is not None:
            type_scores[task_type].append(response)

    if type_scores:
        labels = []
        scores = []
        for t, responses in type_scores.items():
            avg = sum(responses) / len(responses)
            labels.append(t)
            scores.append(avg * 100)

        plt.figure(figsize=(9, 5))
        plt.bar(labels, scores, color='skyblue')
        plt.title('Процент правильных ответов по темам')
        plt.ylabel('Правильных ответов (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("temp_plot_by_type.png")
        plt.close()

        flowables.append(Paragraph("<b>График по типам задач</b>", styles['Normal']))
        flowables.append(Image("temp_plot_by_type.png"))

    # Конец отчёта
    flowables.append(Spacer(1, 24))
    flowables.append(Paragraph("Конец отчёта", styles['Normal']))

    # Генерация PDF
    doc.build(flowables)
    return path