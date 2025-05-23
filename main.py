# main.py

import os
from gui.app import CATApp

if __name__ == "__main__":
    os.makedirs("reports/excel", exist_ok=True)
    os.makedirs("reports/pdf", exist_ok=True)
    app = CATApp()
    app.mainloop()