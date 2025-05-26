# # utils/style_loader.py

# import os
# import json


# def load_styles(style_manager, theme_name="default"):
#     """Загружает стиль из JSON и применяет его"""
#     styles_path = os.path.join("styles", f"{theme_name}.json")

#     if not os.path.exists(styles_path):
#         print(f"[Ошибка] Файл стиля {styles_path} не найден.")
#         return

#     with open(styles_path, "r", encoding="utf-8") as f:
#         styles = json.load(f)

#     for widget_type, settings in styles.items():
#         style_manager.configure(widget_type, **settings)

# utils/style_loader.py

import os
import json
from tkinter import ttk


def load_styles(style_manager, theme_name="default"):
    styles_path = os.path.join("styles", f"{theme_name}.json")

    if not os.path.exists(styles_path):
        print(f"[Ошибка] Стиль '{theme_name}' не найден.")
        return

    try:
        with open(styles_path, "r", encoding="utf-8") as f:
            styles = json.load(f)

        for widget_type, settings in styles.items():
            if hasattr(style_manager, "configure"):
                style_manager.configure(widget_type, **settings)

    except Exception as e:
        print(f"[Ошибка] Не удалось загрузить стиль: {e}")