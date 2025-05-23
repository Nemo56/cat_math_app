# utils/helpers.py

import os

def list_reports():
    report_dir = "reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    return os.listdir(report_dir)

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()