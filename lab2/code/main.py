import sys
import os
import traceback
from PyQt6.QtWidgets import QApplication
from gui import MainWindow

def main():
    """Галоўная функцыя запуску праграмы"""
    try:
        # Стварэнне дадатку
        app = QApplication(sys.argv)
        app.setApplicationName("Image Metadata Analyzer")
        app.setApplicationVersion("1.0")

        # Стварэнне і адлюстраванне галоўнага акна
        window = MainWindow()
        window.show()

        # Запуск галоўнага цыкла
        return app.exec()

    except Exception as e:
        print(f"Крытычная памылка: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
