# utils/exporter.py

import pandas as pd
import matplotlib.pyplot as plt
import os
from config import EXCEL_DIR, PDF_DIR
from datetime import datetime


def save_to_excel(data, theta_history, task_analysis, student_name=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"test_{student_name.replace(' ', '_')}_{timestamp}.xlsx"
    path = os.path.join(EXCEL_DIR, filename)

    df = pd.DataFrame(data)
    df.to_excel(path, index=False)

    # Добавляем историю theta
    df_theta = pd.DataFrame({"Theta": theta_history})
    with pd.ExcelWriter(path, mode="a", engine="openpyxl") as writer:
        df_theta.to_excel(writer, sheet_name="Theta", index=False)

    return path


def save_to_pdf(theta, theta_history, recommendations, task_analysis, student_name=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"test_{student_name.replace(' ', '_')}_{timestamp}.pdf"
    path = os.path.join(PDF_DIR, filename)

    plt.figure(figsize=(8, 5))
    plt.plot(range(len(theta_history)), theta_history, marker='o', linestyle='-')
    plt.title('Изменение уровня способности θ')
    plt.xlabel('Номер вопроса')
    plt.ylabel('θ')
    plt.grid(True)
    plt.savefig("temp_plot.png")
    plt.close()

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    flowables = []

    flowables.append(Paragraph(f"Результаты тестирования — {student_name}", styles['Title']))
    flowables.append(Spacer(1, 12))

    flowables.append(Paragraph(f"<b>Итоговый уровень:</b> {recommendations['level']}", styles['Normal']))
    flowables.append(Paragraph(f"<b>Рекомендации:</b> {recommendations['text']}", styles['Normal']))
    flowables.append(Spacer(1, 12))

    flowables.append(Paragraph("<b>Анализ по темам:</b>", styles['Normal']))
    for t, score in task_analysis.items():
        flowables.append(Paragraph(f"- {t}: {'%.0f%%' % (score * 100)} правильных ответов", styles['Normal']))

    flowables.append(Spacer(1, 24))
    flowables.append(Paragraph("График изменения уровня знаний:", styles['Normal']))
    flowables.append(Image("temp_plot.png"))

    doc.build(flowables)
    return path