import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QComboBox, QLabel,
                             QSpinBox, QGroupBox, QTextEdit, QSplitter, QSlider,
                             QFrame, QTabWidget, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QWheelEvent, QLinearGradient
from algorithms import RasterAlgorithms

class StyledButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6a11cb, stop:1 #2575fc);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7d29d9, stop:1 #3a86ff);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a0db9, stop:1 #1c6df2);
            }
        """)
        self.setFixedHeight(35)

class ArrowButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #94a3b8, stop:1 #64748b);
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                min-width: 25px;
                max-width: 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a8b8d0, stop:1 #7a8ca6);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7a8ca6, stop:1 #4a5568);
            }
        """)
        self.setFixedSize(25, 25)

class ModernGroupBox(QGroupBox):
    def __init__(self, title):
        super().__init__(title)
        self.setStyleSheet("""
            QGroupBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.9), stop:1 rgba(240,245,255,0.9));
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                margin-top: 1ex;
                padding-top: 10px;
                font-weight: bold;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6a11cb, stop:1 #2575fc);
                color: white;
                border-radius: 6px;
            }
        """)

class ModernSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QSpinBox {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 5px;
                font-size: 12px;
                selection-background-color: #2575fc;
            }
            QSpinBox:focus {
                border: 2px solid #2575fc;
            }
        """)
        self.setFixedHeight(30)
        self.setButtonSymbols(QSpinBox.NoButtons)

class ModernComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QComboBox {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 5px;
                font-size: 12px;
                min-width: 120px;
            }
            QComboBox:focus {
                border: 2px solid #2575fc;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6a11cb;
                width: 0px;
                height: 0px;
            }
        """)
        self.setFixedHeight(30)

class ModernSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: white;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6a11cb, stop:1 #2575fc);
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6a11cb, stop:1 #2575fc);
                border: 1px solid #5c5c5c;
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
        """)

class CoordinateControl(QWidget):
    def __init__(self, label, default_value=0, allow_negative=True):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.label = QLabel(label)
        self.label.setFixedWidth(25)

        self.spin_box = ModernSpinBox()
        if allow_negative:
            self.spin_box.setRange(-100, 100)
        else:
            self.spin_box.setRange(0, 100)
        self.spin_box.setValue(default_value)

        self.up_btn = ArrowButton("▲")
        self.down_btn = ArrowButton("▼")

        self.up_btn.clicked.connect(self.increment)
        self.down_btn.clicked.connect(self.decrement)

        layout.addWidget(self.label)
        layout.addWidget(self.spin_box)
        layout.addWidget(self.up_btn)
        layout.addWidget(self.down_btn)

        self.setLayout(layout)

    def increment(self):
        self.spin_box.setValue(self.spin_box.value() + 1)

    def decrement(self):
        self.spin_box.setValue(self.spin_box.value() - 1)

    def value(self):
        return self.spin_box.value()

    def setValue(self, value):
        self.spin_box.setValue(value)

class RasterPlotter(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.smooth_points = []  # Для пунктаў з інтэнсіўнасцю
        self.algorithm_name = ""
        self.setMinimumSize(800, 600)

        self.offset_x = 0
        self.offset_y = 0
        self.scale = 20
        self.is_dragging = False
        self.last_mouse_pos = None

        self.colors = {
            'background': QColor(248, 250, 252),
            'grid': QColor(226, 232, 240),
            'axes': QColor(148, 163, 184),
            'points': QColor(34, 197, 94),
            'smooth_points': QColor(59, 130, 246),
            'accent': QColor(139, 92, 246),
            'text': QColor(30, 41, 59)
        }

    def draw_points(self, points, algorithm_name):
        # Раздзяляем звычайныя пункты і пункты з інтэнсіўнасцю
        regular_points = []
        smooth_points = []

        for point in points:
            if len(point) == 3:  # Пункты з інтэнсіўнасцю (x, y, intensity)
                x, y, intensity = point
                smooth_points.append((x + 0.5, y + 0.5, intensity))
            else:  # Звычайныя пункты (x, y)
                x, y = point
                regular_points.append((x + 0.5, y + 0.5))

        self.points = regular_points
        self.smooth_points = smooth_points
        self.algorithm_name = algorithm_name
        self.update()

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        if delta > 0:
            self.scale = min(self.scale * 1.2, 100)
        else:
            self.scale = max(self.scale / 1.2, 5)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.is_dragging and self.last_mouse_pos:
            delta = event.pos() - self.last_mouse_pos
            self.offset_x += delta.x()
            self.offset_y += delta.y()
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.last_mouse_pos = None

    def reset_view(self):
        self.offset_x = 0
        self.offset_y = 0
        self.scale = 20
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width, height = self.width(), self.height()
        center_x, center_y = width // 2 + self.offset_x, height // 2 + self.offset_y

        gradient = QLinearGradient(0, 0, width, height)
        gradient.setColorAt(0, QColor(248, 250, 252))
        gradient.setColorAt(1, QColor(241, 245, 249))
        painter.fillRect(0, 0, width, height, gradient)

        painter.setPen(QPen(self.colors['grid'], 1))
        grid_size = self.scale

        start_x = center_x % grid_size
        start_y = center_y % grid_size

        for x in range(int(start_x), width, grid_size):
            painter.drawLine(x, 0, x, height)
        for y in range(int(start_y), height, grid_size):
            painter.drawLine(0, y, width, y)

        painter.setPen(QPen(self.colors['axes'], 2))
        painter.drawLine(0, center_y, width, center_y)
        painter.drawLine(center_x, 0, center_x, height)

        painter.setFont(QFont("Segoe UI", 9))
        painter.setPen(QPen(self.colors['text']))

        for i in range(int((-center_x) / grid_size), int((width - center_x) / grid_size) + 1):
            x_pos = center_x + i * grid_size
            if 0 <= x_pos <= width:
                painter.drawText(x_pos - 8, center_y + 20, str(i))

        for i in range(int((-center_y) / grid_size), int((height - center_y) / grid_size) + 1):
            y_pos = center_y + i * grid_size
            if 0 <= y_pos <= height:
                painter.drawText(center_x + 10, y_pos + 5, str(-i))

        # Малюем згладжаныя пункты (з інтэнсіўнасцю)
        if self.smooth_points:
            pixel_margin = 1
            pixel_size = self.scale - pixel_margin * 2

            for x, y, intensity in self.smooth_points:
                screen_x = center_x + x * self.scale
                screen_y = center_y - y * self.scale

                pixel_x = screen_x - self.scale // 2 + pixel_margin
                pixel_y = screen_y - self.scale // 2 + pixel_margin

                # Выкарыстоўваем інтэнсіўнасць для альфа-канала
                alpha = int(255 * intensity)
                color = QColor(59, 130, 246, alpha)

                painter.setBrush(color)
                painter.setPen(QPen(QColor(30, 64, 175, alpha), 1))
                painter.drawRect(int(pixel_x), int(pixel_y), pixel_size, pixel_size)

        # Малюем звычайныя пункты
        if self.points:
            pixel_margin = 1
            pixel_size = self.scale - pixel_margin * 2

            painter.setBrush(QColor(34, 197, 94, 240))
            painter.setPen(QPen(QColor(21, 128, 61), 1))

            for idx, (x, y) in enumerate(self.points):
                screen_x = center_x + x * self.scale
                screen_y = center_y - y * self.scale

                pixel_x = screen_x - self.scale // 2 + pixel_margin
                pixel_y = screen_y - self.scale // 2 + pixel_margin

                painter.drawRect(int(pixel_x), int(pixel_y), pixel_size, pixel_size)

        # Інфармацыйная панэль
        painter.setBrush(QColor(255, 255, 255, 230))
        painter.setPen(QPen(QColor(226, 232, 240), 1))
        painter.drawRoundedRect(10, 10, 300, 150, 10, 10)

        painter.setPen(QPen(self.colors['text']))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(20, 30, "🎯 Растравыя Алгарытмы")

        painter.setFont(QFont("Segoe UI", 9))
        painter.drawText(20, 50, f"📐 Алгарытм: {self.algorithm_name}")
        painter.drawText(20, 70, f"🟢 Пікселі: {len(self.points)}")
        painter.drawText(20, 90, f"🔵 Згладжаныя: {len(self.smooth_points)}")
        painter.drawText(20, 110, f"🔍 Маштаб: {self.scale:.1f}x")
        painter.drawText(20, 130, f"🎮 Зрух: ({self.offset_x}, {self.offset_y})")

        painter.drawText(20, 150, "🖱️ Мышка - рух, Колца - маштаб")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 Лабараторная работа 4: Растравыя алгарытмы")
        self.setGeometry(100, 100, 1400, 800)

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8fafc, stop:1 #f1f5f9);
            }
            QTextEdit {
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px;
                font-size: 11px;
                font-family: 'Cascadia Code', 'Consolas', monospace;
            }
            QLabel {
                color: #334155;
                font-weight: bold;
                font-size: 11px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        control_panel = ModernGroupBox("🎮 Кіраванне")
        control_layout = QVBoxLayout()
        control_layout.setSpacing(12)

        control_layout.addWidget(QLabel("📊 Алгарытм:"))
        self.algorithm_combo = ModernComboBox()
        self.algorithm_combo.addItems([
            "📍 Пакрокавы алгарытм",
            "📈 Алгарытм ЦДА",
            "🎯 Алгарытм Брезенхема (адрэзак)",
            "⚡ Алгарытм Кастла-Пітвея",
            "⭕ Алгарытм Брезенхема (акружнасць)",
            "🌀 Алгарытм Ву (зглажванне)",
            "💫 Згладжаны пакрокавы",
            "🌫️ Гаусава зглажванне",
            "🔍 Супер-семплінг"
        ])
        control_layout.addWidget(self.algorithm_combo)

        coords_group = ModernGroupBox("📐 Каардынаты")
        coords_layout = QVBoxLayout()

        self.x1_control = CoordinateControl("X1:", 0)
        self.y1_control = CoordinateControl("Y1:", 0)
        self.x2_control = CoordinateControl("X2:", 8)
        self.y2_control = CoordinateControl("Y2:", 6)
        self.radius_control = CoordinateControl("R:", 5, allow_negative=False)

        coords_layout.addWidget(self.x1_control)
        coords_layout.addWidget(self.y1_control)
        coords_layout.addWidget(self.x2_control)
        coords_layout.addWidget(self.y2_control)
        coords_layout.addWidget(self.radius_control)

        coords_group.setLayout(coords_layout)
        control_layout.addWidget(coords_group)

        self.draw_btn = StyledButton("🎨 Намаляваць")
        self.draw_btn.clicked.connect(self.draw)
        control_layout.addWidget(self.draw_btn)

        self.reset_btn = StyledButton("🔄 Скінуць від")
        self.reset_btn.clicked.connect(self.reset_view)
        control_layout.addWidget(self.reset_btn)

        scale_group = ModernGroupBox("🔍 Маштаб")
        scale_layout = QVBoxLayout()
        self.scale_slider = ModernSlider()
        self.scale_slider.setRange(5, 100)
        self.scale_slider.setValue(20)
        self.scale_slider.valueChanged.connect(self.change_scale)
        scale_layout.addWidget(self.scale_slider)
        scale_group.setLayout(scale_layout)
        control_layout.addWidget(scale_group)

        stats_group = ModernGroupBox("📊 Статыстыка")
        stats_layout = QVBoxLayout()
        self.time_label = QLabel("⏱️ Час выканання: -- мс")
        self.time_label.setStyleSheet("color: #2563eb; font-weight: bold; font-size: 12px;")
        stats_layout.addWidget(self.time_label)
        stats_group.setLayout(stats_layout)
        control_layout.addWidget(stats_group)

        calc_group = ModernGroupBox("🧮 Разлікі")
        calc_layout = QVBoxLayout()
        self.calc_text = QTextEdit()
        self.calc_text.setMaximumHeight(250)
        calc_layout.addWidget(self.calc_text)
        calc_group.setLayout(calc_layout)
        control_layout.addWidget(calc_group)

        control_panel.setLayout(control_layout)
        control_panel.setMaximumWidth(400)

        self.plotter = RasterPlotter()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(control_panel)
        splitter.addWidget(self.plotter)
        splitter.setSizes([350, 1050])
        layout.addWidget(splitter)

    def draw(self):
        algorithm_index = self.algorithm_combo.currentIndex()
        x1, y1 = self.x1_control.value(), self.y1_control.value()
        x2, y2 = self.x2_control.value(), self.y2_control.value()
        radius = self.radius_control.value()

        algorithms = RasterAlgorithms()
        result = None
        execution_time = 0

        if algorithm_index == 0:
            result, execution_time = algorithms.measure_time(
                algorithms.step_by_step, x1, y1, x2, y2
            )
            self.show_step_calculations(x1, y1, x2, y2, result)

        elif algorithm_index == 1:
            result, execution_time = algorithms.measure_time(
                algorithms.dda, x1, y1, x2, y2
            )
            self.show_dda_calculations(x1, y1, x2, y2)

        elif algorithm_index == 2:
            result, execution_time = algorithms.measure_time(
                algorithms.bresenham_line, x1, y1, x2, y2
            )
            self.show_bresenham_line_calculations(x1, y1, x2, y2, result)

        elif algorithm_index == 3:  # Кастла-Пітвея
            result, execution_time = algorithms.measure_time(
                algorithms.castle_pitway, x1, y1, x2, y2
            )
            self.show_castle_pitway_calculations(x1, y1, x2, y2, result)

        elif algorithm_index == 4:  # Акружнасць Брезенхема
            result, execution_time = algorithms.measure_time(
                algorithms.bresenham_circle, x1, y1, radius
            )
            self.show_bresenham_circle_calculations(x1, y1, radius, result)

        elif algorithm_index == 5:  # Алгарытм Ву
            result, execution_time = algorithms.measure_time(
                algorithms.wu_line, x1, y1, x2, y2
            )
            self.show_wu_calculations(x1, y1, x2, y2, result)

        elif algorithm_index == 6:  # Згладжаны пакрокавы
            result, execution_time = algorithms.measure_time(
                algorithms.smooth_step_by_step, x1, y1, x2, y2
            )
            self.show_smooth_step_calculations(x1, y1, x2, y2, result)

        elif algorithm_index == 7:  # Гаусава зглажванне
            result, execution_time = algorithms.measure_time(
                algorithms.gaussian_smooth_line, x1, y1, x2, y2
            )
            self.show_gaussian_calculations(x1, y1, x2, y2, result)

        elif algorithm_index == 8:  # Супер-семплінг
            result, execution_time = algorithms.measure_time(
                algorithms.super_sampling_line, x1, y1, x2, y2
            )
            self.show_supersampling_calculations(x1, y1, x2, y2, result)

        if result:
            # Нармалізуем інтэнсіўнасць для згладжаных алгарытмаў
            if algorithm_index >= 5:  # Усе алгарытмы зглажвання
                result = algorithms.normalize_intensity(result)
                result = algorithms.apply_threshold(result, 0.05)

            self.plotter.draw_points(result, self.algorithm_combo.currentText().replace("📍 ", "").replace("📈 ", "").replace("🎯 ", "").replace("⚡ ", "").replace("⭕ ", "").replace("🌀 ", "").replace("💫 ", "").replace("🌫️ ", "").replace("🔍 ", ""))
            self.time_label.setText(f"⏱️ Час выканання: {execution_time:.3f} мс")

    def reset_view(self):
        self.plotter.reset_view()
        self.scale_slider.setValue(20)

    def change_scale(self):
        self.plotter.scale = self.scale_slider.value()
        self.plotter.update()

    def show_step_calculations(self, x1, y1, x2, y2, points):
        text = f"📍 Пакрокавы алгарытм для ({x1},{y1})-({x2},{y2}):\n"
        text += "="*50 + "\n"
        if x1 != x2:
            k = (y2 - y1) / (x2 - x1)
            b = y1 - k * x1
            text += f"📐 k = (y2-y1)/(x2-x1) = ({y2}-{y1})/({x2}-{x1}) = {k:.2f}\n"
            text += f"📏 b = y1 - k*x1 = {y1} - {k:.2f}*{x1} = {b:.2f}\n"
            text += f"🧮 y = {k:.2f}*x + {b:.2f}\n\n"
        text += f"🎯 Атрыманыя пікселі ({len(points)}):\n"
        text += str(points[:15])
        if len(points) > 15:
            text += "\n..."
        self.calc_text.setText(text)

    def show_dda_calculations(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_inc = dx / steps
        y_inc = dy / steps

        text = f"📈 Алгарытм ЦДА для ({x1},{y1})-({x2},{y2}):\n"
        text += "="*50 + "\n"
        text += f"📐 dx = x2-x1 = {x2}-{x1} = {dx}\n"
        text += f"📏 dy = y2-y1 = {y2}-{y1} = {dy}\n"
        text += f"🎯 steps = max(|dx|,|dy|) = max({abs(dx)},{abs(dy)}) = {steps}\n"
        text += f"📊 x_inc = dx/steps = {dx}/{steps} = {x_inc:.3f}\n"
        text += f"📈 y_inc = dy/steps = {dy}/{steps} = {y_inc:.3f}\n"
        self.calc_text.setText(text)

    def show_bresenham_line_calculations(self, x1, y1, x2, y2, points):
        text = f"🎯 Алгарытм Брезенхема для ({x1},{y1})-({x2},{y2}):\n"
        text += "="*50 + "\n"
        text += f"🟢 Атрыманыя пікселі ({len(points)}):\n"
        text += str(points[:15])
        if len(points) > 15:
            text += "\n..."
        self.calc_text.setText(text)

    def show_bresenham_circle_calculations(self, xc, yc, r, points):
        text = f"⭕ Алгарытм Брезенхема для акружнасці:\n"
        text += "="*50 + "\n"
        text += f"📍 Цэнтр: ({xc},{yc})\n"
        text += f"📏 Радыус: {r}\n"
        text += f"🎯 Атрыманыя пікселі ({len(points)}):\n"
        text += str(points[:20])
        if len(points) > 20:
            text += "\n..."
        self.calc_text.setText(text)

    def show_castle_pitway_calculations(self, x1, y1, x2, y2, points):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        text = f"⚡ Алгарытм Кастла-Пітвея для ({x1},{y1})-({x2},{y2}):\n"
        text += "="*50 + "\n"
        text += f"📐 dx = |x2-x1| = |{x2}-{x1}| = {dx}\n"
        text += f"📏 dy = |y2-y1| = |{y2}-{y1}| = {dy}\n"

        if dx > dy:
            text += f"📊 Асноўны выпадак (dx > dy):\n"
            text += f"   Пачатковая памылка = 2*dy - dx = {2*dy-dx}\n"
        else:
            text += f"📊 Асобны выпадак (dy >= dx):\n"
            text += f"   Пачатковая памылка = 2*dx - dy = {2*dx-dy}\n"

        text += f"🎯 Атрыманыя пікселі ({len(points)}):\n"
        text += str(points[:15])
        if len(points) > 15:
            text += "\n..."
        self.calc_text.setText(text)

    def show_wu_calculations(self, x1, y1, x2, y2, points):
        text = f"🌀 Алгарытм Ву для ({x1},{y1})-({x2},{y2}):\n"
        text += "="*50 + "\n"
        text += f"📊 Згладжаныя пікселі з інтэнсіўнасцю ({len(points)}):\n"

        # Паказваем першыя 10 пунктаў з інтэнсіўнасцю
        for i, (x, y, intensity) in enumerate(points[:10]):
            text += f"   ({x}, {y}) - {intensity:.2f}\n"

        if len(points) > 10:
            text += "   ...\n"

        text += f"📈 Дыяпазон інтэнсіўнасці: {min(p[2] for p in points):.2f} - {max(p[2] for p in points):.2f}"
        self.calc_text.setText(text)

    def show_smooth_step_calculations(self, x1, y1, x2, y2, points):
        text = f"💫 Згладжаны пакрокавы алгарытм для ({x1},{y1})-({x2},{y2}):\n"
        text += "="*50 + "\n"
        if x1 != x2:
            k = (y2 - y1) / (x2 - x1)
            b = y1 - k * x1
            text += f"📐 k = {k:.2f}, b = {b:.2f}\n"
        text += f"📊 Пікселі з інтэнсіўнасцю ({len(points)}):\n"

        for i, point in enumerate(points[:8]):
            if len(point) == 3:
                x, y, intensity = point
                text += f"   ({x}, {y}) - {intensity:.2f}\n"

        if len(points) > 8:
            text += "   ...\n"
        self.calc_text.setText(text)

    def show_gaussian_calculations(self, x1, y1, x2, y2, points):
        text = f"🌫️ Гаусава зглажванне для ({x1},{y1})-({x2},{y2}):\n"
        text += "="*50 + "\n"
        text += f"📊 Выкарыстана ядро 7x7 для зглажвання\n"
        text += f"🎯 Атрымана пікселяў: {len(points)}\n"
        text += f"📈 Сярэдняя інтэнсіўнасць: {sum(p[2] for p in points)/len(points):.3f}\n"
        self.calc_text.setText(text)

    def show_supersampling_calculations(self, x1, y1, x2, y2, points):
        text = f"🔍 Супер-семплінг для ({x1},{y1})-({x2},{y2}):\n"
        text += "="*50 + "\n"
        text += f"📊 Выкарыстана 4x4 дыскрэтызацыя\n"
        text += f"🎯 Атрымана пікселяў: {len(points)}\n"
        text += f"📈 Дыяпазон інтэнсіўнасці: {min(p[2] for p in points):.2f} - {max(p[2] for p in points):.2f}\n"
        self.calc_text.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
