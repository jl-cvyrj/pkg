import sys
import math
import traceback
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QHBoxLayout, QWidget, QPushButton, QFileDialog,
                             QMessageBox, QLabel, QComboBox, QTextEdit,
                             QGroupBox, QSplitter, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor

def handle_exception(exc_type, exc_value, exc_traceback):
    """Глабальны апрацоўшчык памылак"""
    print("Нечаканая памылка:")
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    input("Націсніце Enter для выхаду...")
    sys.exit(1)

sys.excepthook = handle_exception

try:
    from coordinate_system import CoordinateSystem
    from clipping_algorithms import LiangBarskyClipper, PolygonLineClipper
except ImportError as e:
    print(f"Памылка імпарту: {e}")
    input("Націсніце Enter для выхаду...")
    sys.exit(1)

class StyledMainWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle("Лабараторная работа 5 - Алгарытмы адсячэння")
            self.setGeometry(100, 100, 1400, 900)
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 #2c3e50, stop:1 #34495e);
                    color: white;
                }
                QGroupBox {
                    font-weight: bold;
                    font-size: 12px;
                    color: #ecf0f1;
                    border: 2px solid #3498db;
                    border-radius: 8px;
                    margin-top: 1ex;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #3498db;
                }
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #3498db, stop:1 #2980b9);
                    border: 1px solid #2574a9;
                    border-radius: 6px;
                    color: white;
                    font-weight: bold;
                    padding: 8px 16px;
                    min-height: 20px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #3cb0fd, stop:1 #3498db);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #2574a9, stop:1 #2980b9);
                }
                QPushButton:disabled {
                    background: #95a5a6;
                    border: 1px solid #7f8c8d;
                    color: #bdc3c7;
                }
                QComboBox {
                    background: white;
                    border: 2px solid #bdc3c7;
                    border-radius: 6px;
                    padding: 5px;
                    color: #2c3e50;
                    min-width: 120px;
                }
                QComboBox:focus {
                    border-color: #3498db;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 5px solid transparent;
                    border-right: 5px solid transparent;
                    border-top: 5px solid #34495e;
                    width: 0px;
                    height: 0px;
                }
                QTextEdit {
                    background: #ecf0f1;
                    border: 2px solid #bdc3c7;
                    border-radius: 6px;
                    color: #2c3e50;
                    font-family: 'Courier New';
                    font-size: 10px;
                }
                QLabel {
                    color: #ecf0f1;
                }
                QSplitter::handle {
                    background: #3498db;
                    width: 3px;
                }
            """)

            self.segments = []
            self.window = None
            self.polygon = None

            self.init_ui()

        except Exception as e:
            print(f"Памылка ініцыялізацыі: {e}")
            traceback.print_exc()
            input("Націсніце Enter для выхаду...")
            sys.exit(1)

    def init_ui(self):
        try:
            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            main_layout = QHBoxLayout()
            central_widget.setLayout(main_layout)

            # Левая панэль кіравання
            control_panel = self.create_control_panel()

            # Раздзяляльнік
            splitter = QSplitter(Qt.Orientation.Horizontal)
            splitter.addWidget(control_panel)

            # Правая панэль з графікай
            graphics_panel = self.create_graphics_panel()
            splitter.addWidget(graphics_panel)

            splitter.setSizes([300, 1100])
            main_layout.addWidget(splitter)

        except Exception as e:
            self.log(f"Памылка стварэння інтэрфейсу: {e}")
            raise

    def create_control_panel(self):
        panel = QWidget()
        panel.setMaximumWidth(350)
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # Загаловак
        title = QLabel("Алгарытмы адсячэння")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #3498db; margin: 10px;")
        layout.addWidget(title)

        # Група файлаў
        file_group = QGroupBox("Кіраванне файламі")
        file_layout = QVBoxLayout()
        file_group.setLayout(file_layout)

        # Кнопкі загрузкі файлаў
        liang_btn = QPushButton("Загрузіць для Ліяна-Барскі")
        liang_btn.clicked.connect(lambda: self.load_file("liang"))

        polygon_btn = QPushButton("Загрузіць для мнагавугольніка")
        polygon_btn.clicked.connect(lambda: self.load_file("polygon"))

        file_layout.addWidget(liang_btn)
        file_layout.addWidget(polygon_btn)

        # Група алгарытмаў
        algo_group = QGroupBox("Алгарытмы адсячэння")
        algo_layout = QVBoxLayout()
        algo_group.setLayout(algo_layout)

        self.clipping_combo = QComboBox()
        self.clipping_combo.addItems([
            "Ліяна-Барскі (прамавугольнае вакно)",
            "Мнагавугольнік (адсячэнне адрэзкаў)"
        ])

        btn_clip = QPushButton("Выканаць адсячэнне")
        btn_clip.clicked.connect(self.perform_clipping)

        btn_show_original = QPushButton("Паказаць толькі зыходныя")
        btn_show_original.clicked.connect(self.show_original)

        btn_reset_view = QPushButton("Скід маштабу і пазіцыі")
        btn_reset_view.clicked.connect(self.reset_view)

        btn_clear = QPushButton("Ачысціць усё")
        btn_clear.clicked.connect(self.clear_data)

        algo_layout.addWidget(QLabel("Выберыце алгарытм:"))
        algo_layout.addWidget(self.clipping_combo)
        algo_layout.addWidget(btn_clip)
        algo_layout.addWidget(btn_show_original)
        algo_layout.addWidget(btn_reset_view)
        algo_layout.addWidget(btn_clear)

        # Група інфармацыі
        info_group = QGroupBox("Інфармацыя")
        info_layout = QVBoxLayout()
        info_group.setLayout(info_layout)

        info_label = QLabel(
            "Фармат файлаў:\n\n"
            "Для Ліяна-Барскі:\n"
            "• Адрэзкі\n• Прамавугольнае вакно\n\n"
            "Для мнагавугольніка:\n"
            "• Адрэзкі\n• Мнагавугольнік\n\n"
            "Кіраванне:\n"
            "• Колеса мышы - маштаб\n"
            "• ЛКМ + рух - перацягванне\n"
            "• Скід - вяртанне да пачатку"
        )
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)

        # Група лагоў
        log_group = QGroupBox("Лагі і статыстыка")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)

        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        log_layout.addWidget(self.log_text)

        # Дадаем усе групы
        layout.addWidget(file_group)
        layout.addWidget(algo_group)
        layout.addWidget(info_group)
        layout.addWidget(log_group)
        layout.addStretch()

        return panel

    def create_graphics_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # Загаловак графікі
        graphics_title = QLabel("Візуалізацыя адсячэння")
        graphics_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        graphics_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        graphics_title.setStyleSheet("color: #3498db; margin: 10px;")
        layout.addWidget(graphics_title)

        # Сістэма каардынат
        self.coord_system = CoordinateSystem()
        layout.addWidget(self.coord_system)

        # Статусны бар
        self.status_label = QLabel("Гатова да работы")
        self.status_label.setStyleSheet("""
            QLabel {
                background: #34495e;
                color: #ecf0f1;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.status_label)

        return panel

    def parse_liang_barsky_file(self, filename):
        """Для файлаў Ліяна-Барскі"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]

            n_segments = int(lines[0])
            self.segments = []

            for i in range(1, 1 + n_segments):
                coords = list(map(float, lines[i].split()))
                if len(coords) == 4:
                    self.segments.append(coords)

            self.window = list(map(float, lines[1 + n_segments].split()))
            self.polygon = None

            self.log(f"Загружаны файл Ліяна-Барскі: {n_segments} адрэзкаў")
            self.log(f"Вакно адсячэння: {self.window}")

        except Exception as e:
            self.log(f"Памылка чытання файла Ліяна-Барскі: {str(e)}")
            raise

    def parse_polygon_file(self, filename):
        """Для файлаў з мнагавугольнікам"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]

            n_segments = int(lines[0])
            self.segments = []

            for i in range(1, 1 + n_segments):
                coords = list(map(float, lines[i].split()))
                if len(coords) == 4:
                    self.segments.append(coords)

            n_polygon = int(lines[1 + n_segments])
            self.polygon = []

            for i in range(2 + n_segments, 2 + n_segments + n_polygon):
                coords = list(map(float, lines[i].split()))
                if len(coords) == 2:
                    self.polygon.append(coords)

            self.window = None

            self.log(f"Загружаны файл мнагавугольніка: {n_segments} адрэзкаў, {n_polygon} вяршынь")
            for i, point in enumerate(self.polygon):
                self.log(f"  Вяршыня {i}: {point}")

        except Exception as e:
            self.log(f"Памылка чытання файла мнагавугольніка: {str(e)}")
            raise

    def load_file(self, algo_type):
        try:
            filename = None
            if algo_type == "liang":
                filename, _ = QFileDialog.getOpenFileName(
                    self, "Выберыце файл для Ліяна-Барскі", "", "Text Files (*.txt)")
                if filename:
                    self.parse_liang_barsky_file(filename)
            else:
                filename, _ = QFileDialog.getOpenFileName(
                    self, "Выберыце файл для адсячэння мнагавугольнікам", "", "Text Files (*.txt)")
                if filename:
                    self.parse_polygon_file(filename)

            if filename:
                self.coord_system.set_data(self.segments, self.window, self.polygon)
                self.log(f"Файл '{filename.split('/')[-1]}' паспяхова загружаны")
                self.status_label.setText(f"Загружаны дадзеныя з {filename.split('/')[-1]}")
                self.show_original()

        except Exception as e:
            error_msg = f"Памылка чытання файла: {str(e)}"
            self.log(error_msg)
            QMessageBox.critical(self, "Памылка", error_msg)

    def log(self, message):
        """Дадае паведамленне ў лаг"""
        self.log_text.append(f"{message}")

    def show_original(self):
        """Паказвае толькі зыходныя дадзеныя без адсячэння"""
        self.coord_system.set_data(self.segments, self.window, self.polygon)
        self.coord_system.set_clipped_segments([])
        self.log("Паказаны зыходныя дадзеныя")
        self.status_label.setText("Зыходныя дадзеныя")

    def reset_view(self):
        """Скід маштабу і пазіцыі"""
        self.coord_system.reset_view()
        self.log("Маштаб і пазіцыя скінутыя")
        self.status_label.setText("Маштаб і пазіцыя скінутыя")

    def perform_clipping(self):
        algorithm = self.clipping_combo.currentText()
        self.log(f"Выкананне адсячэння: {algorithm}")

        if algorithm == "Ліяна-Барскі (прамавугольнае вакно)":
            self.perform_liang_barsky()
        elif algorithm == "Мнагавугольнік (адсячэнне адрэзкаў)":
            self.perform_polygon_clipping()

    def perform_liang_barsky(self):
        if not self.segments or not self.window:
            self.log("Памылка: Няма дадзеных для адсячэння!")
            QMessageBox.warning(self, "Памылка", "Няма дадзеных для адсячэння!")
            return

        clipped_segments = []
        visible_count = 0

        for i, segment in enumerate(self.segments):
            clipped = LiangBarskyClipper.clip_segment(segment, self.window)
            if clipped:
                clipped_segments.append(clipped)
                visible_count += 1
                self.log(f"Адрэзак {i+1} адсечаны: {clipped}")
            else:
                self.log(f"Адрэзак {i+1} цалкам звонку")

        self.coord_system.set_clipped_segments(clipped_segments)
        self.log(f"Вынік: {visible_count}/{len(self.segments)} адрэзкаў бачныя")
        self.status_label.setText(f"Адсечана: {visible_count}/{len(self.segments)} адрэзкаў")

    # main.py (толькі змененыя часткі)
    def perform_polygon_clipping(self):
        """Выкананне адсячэння выпуклага мнагавугольніка"""
        if not self.polygon:
            self.log("Памылка: Няма мнагавугольніка для адсячэння!")
            QMessageBox.warning(self, "Памылка", "Няма мнагавугольніка для адсячэння!")
            return

        # Для адсячэння выпуклага мнагавугольніка трэба мець суб'ект-мнагавугольнік
        # У нашым выпадку суб'ект-мнагавугольнік - гэта першыя 3 ці болей кропак з адрэзкаў
        subject_polygon = []

        # Ствараем суб'ект-мнагавугольнік з кропак адрэзкаў
        for segment in self.segments:
            subject_polygon.append((segment[0], segment[1]))
            subject_polygon.append((segment[2], segment[3]))

        # Бяром унікальныя кропкі
        subject_polygon = list(set(subject_polygon))

        if len(subject_polygon) < 3:
            self.log("Памылка: Замала кропак для фарміравання мнагавугольніка!")
            QMessageBox.warning(self, "Памылка", "Замала кропак для фарміравання мнагавугольніка!")
            return

        # Сартуем кропкі па вугле для фарміравання выпуклага мнагавугольніка
        subject_polygon = self._make_convex_polygon(subject_polygon)

        self.log(f"Суб'ект-мнагавугольнік: {len(subject_polygon)} вяршынь")
        self.log(f"Clip-мнагавугольнік: {len(self.polygon)} вяршынь")

        try:
            # Адсякаем мнагавугольнік
            clipped_polygon = PolygonClipper.clip_polygon(subject_polygon, self.polygon)

            if clipped_polygon:
                # Пераўтвараем выніковы мнагавугольнік у адрэзкі для адлюстравання
                clipped_segments = []
                for i in range(len(clipped_polygon)):
                    start_point = clipped_polygon[i]
                    end_point = clipped_polygon[(i + 1) % len(clipped_polygon)]
                    clipped_segments.append([
                        start_point[0], start_point[1],
                        end_point[0], end_point[1]
                    ])

                self.coord_system.set_clipped_segments(clipped_segments)
                self.log(f"Вынік: адсечаны мнагавугольнік з {len(clipped_polygon)} вяршынямі")
                self.status_label.setText(f"Адсечаны мнагавугольнік ({len(clipped_polygon)} вяршынь)")

                # Захоўваем адсечаны мнагавугольнік для адлюстравання
                self.coord_system.clipped_polygon = clipped_polygon
            else:
                self.coord_system.set_clipped_segments([])
                self.coord_system.clipped_polygon = None
                self.log("Вынік: мнагавугольнік цалкам звонку")
                self.status_label.setText("Мнагавугольнік цалкам звонку")

        except Exception as e:
            self.log(f"Памылка пры адсячэнні мнагавугольніка: {e}")
            QMessageBox.critical(self, "Памылка", f"Памылка пры адсячэнні мнагавугольніка: {e}")

    def _make_convex_polygon(self, points):
        """Стварае выпуклы мнагавугольнік з кропак (алгарытм Грэхема)"""
        if len(points) <= 3:
            return points

        # Знаходзім самую ніжнюю кропку
        min_y_point = min(points, key=lambda p: (p[1], p[0]))

        # Сартуем кропкі па вуглу адносна min_y_point
        def polar_angle(p):
            return math.atan2(p[1] - min_y_point[1], p[0] - min_y_point[0])

        sorted_points = sorted(points, key=polar_angle)

        # Будуем выпуклую абалонку
        hull = [sorted_points[0], sorted_points[1]]

        for i in range(2, len(sorted_points)):
            while len(hull) > 1 and self._cross(hull[-2], hull[-1], sorted_points[i]) <= 0:
                hull.pop()
            hull.append(sorted_points[i])

        return hull

    def _cross(self, o, a, b):
        """Вектарны здабытак вектараў OA і OB"""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


    def clear_data(self):
        self.segments = []
        self.window = None
        self.polygon = None
        self.coord_system.set_data([], None, None)
        self.coord_system.set_clipped_segments([])
        self.log_text.clear()
        self.log("Усе дадзеныя ачышчаны")
        self.status_label.setText("Гатова да работы")

def main():
    try:
        print("Запуск праграмы...")
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        window = StyledMainWindow()
        window.show()
        result = app.exec()
        print("Праграма завершана")
        return result
    except Exception as e:
        print(f"Крытычная памылка: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    main()
