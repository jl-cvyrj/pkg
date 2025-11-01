from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QComboBox,
                            QGroupBox, QFileDialog,
                            QMessageBox, QProgressBar,
                            QTabWidget, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QImage, QFont
import numpy as np
from PIL import Image
from image_processor import ImageProcessor
import os

class ProcessingThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, image, operation, params):
        super().__init__()
        self.image = image
        self.operation = operation
        self.params = params

    def run(self):
        try:
            result = ImageProcessor.process_image(self.image, self.operation, self.params)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(None)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_image = None
        self.processed_image = None
        self.original_image = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Processor - Апрацоўка выяў')
        self.setGeometry(100, 100, 1600, 1000)
        self.setMinimumSize(1400, 900)

        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        top_panel = self.create_top_panel()
        main_layout.addWidget(top_panel)

        image_panel = self.create_image_panel()
        main_layout.addWidget(image_panel, 1)

        bottom_panel = self.create_control_panel()
        main_layout.addWidget(bottom_panel)

        self.apply_styles()

    def create_top_panel(self):
        panel = QWidget()
        layout = QHBoxLayout(panel)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel('🖼️ Image Processor - Апрацоўка выяў')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("QLabel{font-size:28px;font-weight:bold;color:#2d5016;padding:15px 30px;background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 #4CAF50,stop:0.5 #66BB6A,stop:1 #81C784);border-radius:15px;color:white;margin:5px;}")
        layout.addWidget(title)
        return panel

    def create_control_panel(self):
        panel = QWidget()
        panel.setMaximumHeight(150)
        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignCenter)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.setSpacing(20)

        self.load_btn = QPushButton("📁 Загрузіць выяву")
        self.load_btn.clicked.connect(self.load_image)
        self.load_btn.setStyleSheet(self.get_button_style())
        self.load_btn.setFixedSize(180, 50)
        buttons_layout.addWidget(self.load_btn)

        self.save_btn = QPushButton("💾 Захаваць вынік")
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setStyleSheet(self.get_button_style())
        self.save_btn.setFixedSize(180, 50)
        self.save_btn.setEnabled(False)
        buttons_layout.addWidget(self.save_btn)

        self.operation_combo = QComboBox()
        self.operation_combo.setFixedWidth(300)
        operations = [
            "Выберыце метад...",
            "Лінейнае кантраставаньне",
            "Павялічыць яркасць",
            "Павялічыць кантраснасць",
            "Мануальная парогавая апрацоўка",
            "Адаптыўная парогавая апрацоўка (Otsu)",
            "Лякальная парогавая апрацоўка (Gaussian)",
            "Лякальная парогавая апрацоўка (Mean)",
            "Глабальная парогавая апрацоўка (Mean)",
            "Інвертаваць колеры",
        ]
        self.operation_combo.addItems(operations)
        self.operation_combo.setStyleSheet("QComboBox{padding:10px;border:2px solid #4CAF50;border-radius:10px;background:white;font-size:14px;min-width:300px;}QComboBox::drop-down{border:none;width:30px;}QComboBox::down-arrow{border-left:5px solid transparent;border-right:5px solid transparent;border-top:5px solid #4CAF50;width:0px;height:0px;}")
        buttons_layout.addWidget(self.operation_combo)

        self.process_btn = QPushButton("⚡ Апрацаваць")
        self.process_btn.clicked.connect(self.process_image)
        self.process_btn.setStyleSheet(self.get_process_button_style())
        self.process_btn.setFixedSize(170, 50)
        self.process_btn.setEnabled(False)
        buttons_layout.addWidget(self.process_btn)

        layout.addLayout(buttons_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignCenter)
        bottom_layout.setSpacing(25)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(350)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar{border:2px solid #4CAF50;border-radius:10px;text-align:center;background:white;height:22px;font-size:12px;}QProgressBar::chunk{background-color:#4CAF50;border-radius:8px;}")
        bottom_layout.addWidget(self.progress_bar)

        self.info_label = QLabel("Загрузіце выяву для пачатку апрацоўкі")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        self.info_label.setFixedWidth(350)
        self.info_label.setStyleSheet("QLabel{font-size:13px;color:#555;background:#F1F8E9;padding:8px;border-radius:8px;border:1px solid #C8E6C9;}")
        bottom_layout.addWidget(self.info_label)

        layout.addLayout(bottom_layout)
        return panel

    def create_image_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10)

        tabs = QTabWidget()
        tabs.setStyleSheet("QTabWidget::pane{border:2px solid #4CAF50;border-radius:12px;background:white;}QTabBar::tab{background:#E8F5E8;border:1px solid #4CAF50;padding:8px 15px;margin:2px;border-top-left-radius:8px;border-top-right-radius:8px;color:#2d5016;font-weight:bold;font-size:13px;}QTabBar::tab:selected{background:#4CAF50;color:white;}QTabBar::tab:hover{background:#C8E6C9;}")

        compare_tab = QWidget()
        compare_layout = QHBoxLayout(compare_tab)
        compare_layout.setAlignment(Qt.AlignCenter)
        compare_layout.setSpacing(25)
        compare_layout.setContentsMargins(15, 15, 15, 15)

        original_frame = QGroupBox("Арыгінальная выява")
        original_layout = QVBoxLayout(original_frame)
        original_layout.setAlignment(Qt.AlignCenter)

        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setMinimumSize(600, 500)
        self.original_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.original_label.setStyleSheet("QLabel{background:#f8f9fa;border:3px dashed #dee2e6;border-radius:15px;color:#6c757d;font-size:16px;}")
        self.original_label.setText("Тут будзе арыгінальная выява")
        original_layout.addWidget(self.original_label)

        processed_frame = QGroupBox("Апрацаваная выява")
        processed_layout = QVBoxLayout(processed_frame)
        processed_layout.setAlignment(Qt.AlignCenter)

        self.processed_label = QLabel()
        self.processed_label.setAlignment(Qt.AlignCenter)
        self.processed_label.setMinimumSize(600, 500)
        self.processed_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.processed_label.setStyleSheet("QLabel{background:#f8f9fa;border:3px dashed #dee2e6;border-radius:15px;color:#6c757d;font-size:16px;}")
        self.processed_label.setText("Тут будзе апрацаваная выява")
        processed_layout.addWidget(self.processed_label)

        compare_layout.addWidget(original_frame)
        compare_layout.addWidget(processed_frame)

        tabs.addTab(compare_tab, "👁️ Параўнанне")
        layout.addWidget(tabs)
        return panel

    def apply_styles(self):
        self.setStyleSheet("QMainWindow{background:#E8F5E8;}QGroupBox{font-weight:bold;font-size:15px;color:#2d5016;border:2px solid #A5D6A7;border-radius:10px;margin-top:8px;padding-top:12px;background:#F1F8E9;}QGroupBox::title{subcontrol-origin:margin;subcontrol-position:top center;padding:2px 10px;background-color:#F1F8E9;border-radius:6px;}")

    def get_button_style(self):
        return "QPushButton{background:#4CAF50;color:white;font-weight:bold;padding:12px;border-radius:10px;font-size:13px;border:none;}QPushButton:hover{background:#45a049;}QPushButton:pressed{background:#388E3C;}QPushButton:disabled{background:#C8E6C9;color:#81C784;}"

    def get_process_button_style(self):
        return "QPushButton{background:#2E7D32;color:white;font-weight:bold;padding:12px;border-radius:10px;font-size:13px;border:none;}QPushButton:hover{background:#1B5E20;}QPushButton:pressed{background:#0D4010;}QPushButton:disabled{background:#E8F5E8;color:#A5D6A7;border:2px solid #C8E6C9;}"

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузіць выяву", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff);;All Files (*)")

        if file_path:
            try:
                pil_image = Image.open(file_path)
                self.original_image = np.array(pil_image.convert('RGB'))
                self.current_image = self.original_image.copy()
                self.processed_image = None

                self.display_image(self.original_image, self.original_label)

                self.processed_label.clear()
                self.processed_label.setText("Тут будзе апрацаваная выява")

                self.process_btn.setEnabled(True)
                self.save_btn.setEnabled(False)

                height, width = self.original_image.shape[:2]
                self.info_label.setText(f"📊 Памер: {width}×{height}\n🎯 Фармат: RGB\n💾 Загружана: {os.path.basename(file_path)}")

            except Exception as e:
                QMessageBox.critical(self, "Памылка", f"Не атрымалася загрузіць выяву: {str(e)}")

    def display_image(self, image, label):
        if image is None:
            return

        try:
            if len(image.shape) == 3:
                h, w, ch = image.shape
                bytes_per_line = ch * w
                q_img = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            else:
                h, w = image.shape
                q_img = QImage(image.data, w, h, w, QImage.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_img)
            label_size = label.size()
            scaled_pixmap = pixmap.scaled(label_size.width() - 20, label_size.height() - 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled_pixmap)

        except Exception as e:
            print(f"Памылка адлюстравання выявы: {e}")

    def process_image(self):
        if self.current_image is None:
            QMessageBox.warning(self, "Увага", "Спачатку загрузіце выяву!")
            return

        operation = self.operation_combo.currentText()
        if operation == "Выберыце метад...":
            QMessageBox.warning(self, "Увага", "Выберыце метад апрацоўкі!")
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.process_btn.setEnabled(False)

        self.processing_thread = ProcessingThread(self.current_image, operation, {})
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.start()

    def on_processing_finished(self, result):
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)
        self.process_btn.setEnabled(True)

        if result is not None:
            self.processed_image = result
            self.display_image(self.processed_image, self.processed_label)
            self.save_btn.setEnabled(True)
            operation = self.operation_combo.currentText()
            self.info_label.setText(f"✅ Апрацавана: {operation}\n💾 Вынік гатовы да захавання")
        else:
            QMessageBox.critical(self, "Памылка", "Не атрымалася апрацаваць выяву!")

    def save_image(self):
        if self.processed_image is None:
            QMessageBox.warning(self, "Увага", "Няма апрацаванай выявы для захавання!")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Захаваць выяву", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")

        if file_path:
            try:
                from PIL import Image as PILImage
                pil_image = PILImage.fromarray(self.processed_image)
                pil_image.save(file_path)
                QMessageBox.information(self, "Паспяхова", f"Выява захавана ў: {file_path}")
                self.info_label.setText(f"💾 Выява паспяхова захавана!")
            except Exception as e:
                QMessageBox.critical(self, "Памылка", f"Памылка пры захаванні: {str(e)}")
