# main.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui_main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    font = QFont("Segoe UI", 12)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
