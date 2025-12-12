from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
from PyQt6.QtCore import QPointF, Qt
import math

class CoordinateSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)

        # Дадзеныя
        self.segments = []
        self.clipped_segments = []
        self.window = None
        self.polygon = None

        # Колеры
        self.window_color = QColor(255, 0, 0)      # Чырвоны - вакно
        self.original_color = QColor(0, 0, 255)    # Сіні - зыходныя адрэзкі
        self.clipped_color = QColor(0, 255, 0)     # Зялёны - адсечаныя адрэзкі
        self.polygon_color = QColor(255, 165, 0)   # Аранжавы - мнагавугольнік

        # Маштабаванне і перацягванне
        self.scale = 40
        self.auto_scale = True
        self.offset_x = 0
        self.offset_y = 0
        self.drag_start = None
        self.is_dragging = False

        self.setMouseTracking(True)

    def set_data(self, segments, window, polygon=None):
        self.segments = segments
        self.window = window
        self.polygon = polygon
        self.clipped_segments = []  # ДАДАЦЬ ГЭТЫ РАДОК - ачышчаем старыя адсечаныя адрэзкі
        self._calculate_auto_scale()
        self.update()

    def set_clipped_segments(self, clipped_segments):
        self.clipped_segments = clipped_segments
        self.update()

    def _calculate_auto_scale(self):
        if not self.segments and not self.window and not self.polygon:
            self.scale = 40
            return

        all_points = []

        for segment in self.segments:
            all_points.extend([segment[0], segment[1], segment[2], segment[3]])

        if self.window:
            all_points.extend([self.window[0], self.window[1], self.window[2], self.window[3]])

        if self.polygon:
            for point in self.polygon:
                all_points.extend(point)

        if not all_points:
            self.scale = 40
            return

        max_abs_value = max(abs(x) for x in all_points)

        if max_abs_value == 0:
            self.scale = 40
        else:
            available_size = min(self.width(), self.height()) * 0.8
            self.scale = available_size / (max_abs_value * 2) if max_abs_value > 0 else 40
            self.scale = max(20, min(100, self.scale))

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            painter.fillRect(0, 0, self.width(), self.height(), QColor(240, 240, 240))

            center_x = self.width() / 2 + self.offset_x
            center_y = self.height() / 2 + self.offset_y

            self._draw_coordinate_axes(painter, center_x, center_y, self.scale)

            # Малюем мнагавугольнік (калі ёсць)
            if self.polygon:
                self._draw_polygon(painter, self.polygon, self.polygon_color, center_x, center_y, self.scale)

            # Малюем вакно (калі ёсць і няма мнагавугольніка)
            elif self.window:
                self._draw_window(painter, center_x, center_y, self.scale)

            # Малюем зыходныя адрэзкі
            for segment in self.segments:
                self._draw_segment(painter, segment, self.original_color, center_x, center_y, self.scale)

            # Малюем адсечаныя адрэзкі
            for segment in self.clipped_segments:
                self._draw_segment(painter, segment, self.clipped_color, center_x, center_y, self.scale)

            self._draw_legend(painter)
            self._draw_scale_info(painter)

        except Exception as e:
            print(f"Памылка ў paintEvent: {e}")
            import traceback
            traceback.print_exc()

    def _draw_coordinate_axes(self, painter, offset_x, offset_y, scale):
        pen = QPen(QColor(150, 150, 150), 1)
        painter.setPen(pen)

        offset_x_int = int(offset_x)
        offset_y_int = int(offset_y)
        width_int = int(self.width())
        height_int = int(self.height())

        painter.drawLine(0, offset_y_int, width_int, offset_y_int)
        painter.drawLine(offset_x_int, 0, offset_x_int, height_int)

        grid_pen = QPen(QColor(220, 220, 220), 1)
        painter.setPen(grid_pen)

        for i in range(-20, 21):
            x = int(offset_x + i * scale)
            painter.drawLine(x, 0, x, height_int)

        for i in range(-20, 21):
            y = int(offset_y - i * scale)
            painter.drawLine(0, y, width_int, y)

        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)
        painter.setPen(QPen(QColor(100, 100, 100)))

        for i in range(-10, 11):
            x = int(offset_x + i * scale)
            painter.drawLine(x, offset_y_int - 5, x, offset_y_int + 5)
            if i != 0:
                painter.drawText(x - 10, offset_y_int + 20, str(i))

        for i in range(-10, 11):
            y = int(offset_y - i * scale)
            painter.drawLine(offset_x_int - 5, y, offset_x_int + 5, y)
            if i != 0:
                painter.drawText(offset_x_int + 10, y + 5, str(i))

        painter.drawText(offset_x_int + 5, offset_y_int + 15, "0")

    def _draw_window(self, painter, offset_x, offset_y, scale):
        if not self.window:
            return

        xmin, ymin, xmax, ymax = self.window

        screen_xmin = int(offset_x + xmin * scale)
        screen_ymin = int(offset_y - ymin * scale)
        screen_xmax = int(offset_x + xmax * scale)
        screen_ymax = int(offset_y - ymax * scale)

        width = screen_xmax - screen_xmin
        height = screen_ymax - screen_ymin

        pen = QPen(self.window_color, 3)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 0, 0, 30))

        painter.drawRect(screen_xmin, screen_ymin, width, height)

    def _draw_segment(self, painter, segment, color, offset_x, offset_y, scale):
        if len(segment) != 4:
            return

        x1, y1, x2, y2 = segment

        screen_x1 = int(offset_x + x1 * scale)
        screen_y1 = int(offset_y - y1 * scale)
        screen_x2 = int(offset_x + x2 * scale)
        screen_y2 = int(offset_y - y2 * scale)

        pen = QPen(color, 2)
        painter.setPen(pen)
        painter.drawLine(screen_x1, screen_y1, screen_x2, screen_y2)

    def _draw_polygon(self, painter, polygon, color, offset_x, offset_y, scale):
        if len(polygon) < 3:
            return

        points = []
        for x, y in polygon:
            screen_x = int(offset_x + x * scale)
            screen_y = int(offset_y - y * scale)
            points.append(QPointF(screen_x, screen_y))

        pen = QPen(color, 3)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 165, 0, 80))

        for i in range(len(points)):
            start_point = points[i]
            end_point = points[(i + 1) % len(points)]
            painter.drawLine(start_point, end_point)

        painter.drawPolygon(points)

    def _draw_legend(self, painter):
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)

        y_offset = 30
        x_offset = 10

        painter.fillRect(5, 5, 220, 160, QColor(255, 255, 255, 230))
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.drawRect(5, 5, 220, 160)

        painter.drawText(x_offset, y_offset, "Легенда:")
        y_offset += 20

        painter.setPen(QPen(self.window_color, 3))
        painter.drawLine(x_offset, y_offset, x_offset + 40, y_offset)
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.drawText(x_offset + 50, y_offset + 4, "Вакно адсячэння")
        y_offset += 20

        painter.setPen(QPen(self.original_color, 2))
        painter.drawLine(x_offset, y_offset, x_offset + 40, y_offset)
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.drawText(x_offset + 50, y_offset + 4, "Зыходныя адрэзкі")
        y_offset += 20

        painter.setPen(QPen(self.clipped_color, 2))
        painter.drawLine(x_offset, y_offset, x_offset + 40, y_offset)
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.drawText(x_offset + 50, y_offset + 4, "Адсечаныя адрэзкі")
        y_offset += 20

        if self.polygon:
            painter.setPen(QPen(self.polygon_color, 3))
            painter.drawLine(x_offset, y_offset, x_offset + 40, y_offset)
            painter.setPen(QPen(QColor(0, 0, 0)))
            painter.drawText(x_offset + 50, y_offset + 4, "Мнагавугольнік")
            y_offset += 20

    def _draw_scale_info(self, painter):
        font = QFont()
        font.setPointSize(9)
        painter.setFont(font)
        painter.setPen(QPen(QColor(0, 0, 0)))

        info_text = f"Маштаб: {self.scale:.1f} | Колеса мышы - маштаб | ЛКМ + рух - перацягванне"
        painter.drawText(10, self.height() - 40, info_text)

        center_x = self.width() / 2 + self.offset_x
        center_y = self.height() / 2 + self.offset_y
        center_info = f"Цэнтр: ({self.offset_x/self.scale:.1f}, {-self.offset_y/self.scale:.1f})"
        painter.drawText(10, self.height() - 20, center_info)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        old_scale = self.scale

        if delta > 0:
            self.scale *= 1.1
        else:
            self.scale *= 0.9

        self.scale = max(10, min(200, self.scale))
        self.auto_scale = False

        pos = event.position()
        scale_factor = self.scale / old_scale
        self.offset_x = (self.offset_x + pos.x() - self.width()/2) * scale_factor - (pos.x() - self.width()/2)
        self.offset_y = (self.offset_y + pos.y() - self.height()/2) * scale_factor - (pos.y() - self.height()/2)

        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start = event.pos()
            self.is_dragging = True
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.is_dragging and self.drag_start:
            delta = event.pos() - self.drag_start
            self.offset_x += delta.x()
            self.offset_y += delta.y()
            self.drag_start = event.pos()
            self.update()

        if not self.is_dragging:
            self.setCursor(Qt.CursorShape.OpenHandCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            self.drag_start = None
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def reset_view(self):
        self.offset_x = 0
        self.offset_y = 0
        self.scale = 40
        self.auto_scale = True
        self._calculate_auto_scale()
        self.update()
