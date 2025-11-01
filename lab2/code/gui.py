import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                             QTextEdit, QProgressBar, QFileDialog, QMessageBox,
                             QWidget, QHeaderView, QTabWidget,
                             QLineEdit, QGroupBox, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor
from image_analyzer import ImageAnalyzer

class AnalysisThread(QThread):
    """Асобны паток для апрацоўкі малюнкаў"""
    progress = pyqtSignal(int, int, str)  # бягучы, усяго, імя файла
    finished = pyqtSignal(dict)  # вынікі

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.analyzer = ImageAnalyzer(max_workers=6)

    def run(self):
        try:
            results = self.analyzer.analyze_folder(
                self.folder_path,
                lambda current, total, filename: self.progress.emit(current, total, filename)
            )
            self.finished.emit(results)
        except Exception as e:
            self.finished.emit({'error': str(e)})

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.analysis_thread = None
        self.current_results = None
        self.current_folder = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Анализатар метаданых малюнкаў v2.0")
        self.setGeometry(100, 100, 1400, 900)

        # Прыгожыя стылі для ўсяго інтэрфейсу
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
                font-family: Segoe UI, Arial;
                font-size: 12px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #d0d0d0;
                border-radius: 6px;
                margin-top: 5px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #2c3e50;
            }
            QLabel {
                color: #333333;
            }
        """)

        # Цэнтральны віджэт
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Галоўны layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)  # Меншыя адстаўкі паміж секцыямі
        main_layout.setContentsMargins(12, 12, 12, 12)
        central_widget.setLayout(main_layout)

        # Стварэнне інтэрфейсу
        self.create_header(main_layout)
        self.create_controls(main_layout)
        self.create_progress_section(main_layout)
        self.create_results_section(main_layout)  # Гэтая секцыя займае больш месца
        self.create_status_bar()

        # Таймер для абнаўлення інтэрфейсу
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui)
        self.update_timer.start(100)

    def create_header(self, layout):
        """Стварыць загаловак праграмы - меншы па памеры"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #3498db, stop: 1 #2c3e50);
                border-radius: 6px;
                padding: 10px;
            }
        """)

        header_layout = QVBoxLayout()
        header_frame.setLayout(header_layout)

        title = QLabel("🖼️ Аналізатар метаданых малюнкаў")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }
        """)

        subtitle = QLabel("Чытанне інфармацыі з графічных файлаў")
        subtitle.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 10px;
                text-align: center;
                font-style: italic;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        # Меншы прапорцыя для загалоўка
        layout.addWidget(header_frame, stretch=0)  # stretch=0 - фіксаваны памер

    def create_controls(self, layout):
        """Стварыць элементы кіравання - кампактней"""
        controls_group = QGroupBox("Кіраванне аналізам")
        controls_layout = QVBoxLayout()

        # Першы радок - шлях да папкі
        path_layout = QHBoxLayout()

        path_label = QLabel("📁 Папка:")
        path_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 11px;")

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Выберыце папку з малюнкамі...")
        self.path_edit.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
                font-size: 11px;
                color: #333333;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """)
        self.path_edit.textChanged.connect(self.on_folder_changed)

        self.browse_btn = QPushButton("📂 Абраць")
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.browse_btn.clicked.connect(self.browse_folder)

        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_edit, 1)
        path_layout.addWidget(self.browse_btn)

        # Другі радок - кнопкі дзеянняў
        buttons_layout = QHBoxLayout()

        self.analyze_btn = QPushButton("🚀 Аналізаваць")
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #7f8c8d;
            }
        """)
        self.analyze_btn.clicked.connect(self.start_analysis)

        self.export_btn = QPushButton("💾 Экспарт")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.export_btn.clicked.connect(self.export_results)
        self.export_btn.setEnabled(False)

        buttons_layout.addWidget(self.analyze_btn)
        buttons_layout.addWidget(self.export_btn)
        buttons_layout.addStretch()

        # Інфармацыя пра абраную папку - кампактная
        self.folder_info = QLabel("Папка не абраная")
        self.folder_info.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 9px;
                font-style: italic;
                padding: 3px;
                background-color: #ecf0f1;
                border-radius: 3px;
                border: 1px dashed #bdc3c7;
            }
        """)

        controls_layout.addLayout(path_layout)
        controls_layout.addLayout(buttons_layout)
        controls_layout.addWidget(self.folder_info)
        controls_group.setLayout(controls_layout)

        # Меншы прапорцыя для кіравання
        layout.addWidget(controls_group, stretch=0)  # stretch=0 - фіксаваны памер

    def create_progress_section(self, layout):
        """Стварыць секцыю прагрэсу - кампактную"""
        progress_group = QGroupBox("Прагрэс")
        progress_layout = QVBoxLayout()

        # Прагрэс-бар з прыгожым стылем
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 4px;
                text-align: center;
                background-color: #ecf0f1;
                height: 16px;
                color: #333333;
                font-size: 10px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #3498db, stop: 1 #2ecc71);
                border-radius: 3px;
            }
        """)

        # Статус аналізу - кампактны
        self.status_label = QLabel("✅ Гатовы да работы")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                font-weight: bold;
                padding: 4px;
                background-color: #d5f4e6;
                border-radius: 3px;
                border: 1px solid #2ecc71;
                color: #27ae60;
            }
        """)

        # Дэталі прагрэсу - кампактныя
        self.progress_details = QLabel("Абярыце папку для пачатку аналізу")
        self.progress_details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_details.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 9px;
                font-style: italic;
                padding: 2px;
            }
        """)

        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)
        progress_layout.addWidget(self.progress_details)
        progress_group.setLayout(progress_layout)

        # Меншы прапорцыя для прагрэсу
        layout.addWidget(progress_group, stretch=0)  # stretch=0 - фіксаваны памер

    def create_results_section(self, layout):
        """Стварыць секцыю вынікаў - ВЯЛІКАЯ, займае ўсё астатняе месца"""
        # Стварэнне ўкладак з прыгожымі стылямі
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cccccc;
                border-radius: 6px;
                background-color: white;
            }
            QTabBar::tab {
                background: #ecf0f1;
                border: 1px solid #cccccc;
                padding: 6px 12px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                color: #2c3e50;
                font-weight: bold;
                font-size: 11px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background: #d6dbdf;
            }
        """)

        # Укладка табліцы
        self.table_tab = QWidget()
        self.create_table_tab()
        self.tabs.addTab(self.table_tab, "📋 Табліца")

        # Укладка дэталяў
        self.details_tab = QWidget()
        self.create_details_tab()
        self.tabs.addTab(self.details_tab, "🔍 Дэталі")

        # Укладка статыстыкі
        self.stats_tab = QWidget()
        self.create_stats_tab()
        self.tabs.addTab(self.stats_tab, "📊 Статыстыка")

        # ВЯЛІКІ stretch - займае ўсё астатняе месца
        layout.addWidget(self.tabs, stretch=10)

    def create_table_tab(self):
        """Стварыць укладку табліцы - максімальны памер"""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Загаловак табліцы - кампактны
        table_title = QLabel("📊 Вынікі аналізу малюнкаў")
        table_title.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 12px; margin-bottom: 5px;")

        # Табліца вынікаў - ВЯЛІКАЯ, займае ўсё месца
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(10)  # Зменена з 9 на 10
        self.results_table.setHorizontalHeaderLabels([
            "📁 Імя файла", "📏 Памер", "🎯 DPI", "🎨 Глыбіня",
            "💾 Сціск", "🖼️ Фармат", "📊 Файл", "🔢 Квантаванне", "📂 Шлях", "✅ Статус"
        ])

        # Стылізацыя табліцы
        self.results_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #e0e0e0;
                border: 1px solid #cccccc;
                border-radius: 4px;
                color: #333333;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 4px;
                border-bottom: 1px solid #f0f0f0;
                color: #333333;
            }
            QTableWidget::item:selected {
                background-color: #d6eaf8;
                color: #2c3e50;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 6px;
                border: none;
                font-weight: bold;
                font-size: 10px;
            }
        """)

        # Налады табліцы
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.doubleClicked.connect(self.show_file_details)

        # Аўтаматычнае размеркаванне шырыні слупкоў
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Імя
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Памер
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # DPI
        self.results_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Глыбіня
        self.results_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Сціск
        self.results_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Фармат
        self.results_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Памер файла
        self.results_table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # Квантаванне
        self.results_table.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.ResizeToContents)  # Статус
        # Шлях займае ўсё астатняе месца
        self.results_table.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)  # Шлях

        layout.addWidget(table_title, stretch=0)
        layout.addWidget(self.results_table, stretch=1)  # Табліца займае ўсё месца
        self.table_tab.setLayout(layout)

    def create_details_tab(self):
        """Стварыць укладку дэталяў - максімальны памер"""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        details_title = QLabel("🔍 Дэтальныя звесткі пра абраны файл")
        details_title.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 12px; margin-bottom: 5px;")

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setFont(QFont("Consolas", 9))
        self.details_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 10px;
                color: #333333;
            }
        """)

        layout.addWidget(details_title, stretch=0)
        layout.addWidget(self.details_text, stretch=1)  # Тэкст займае ўсё месца
        self.details_tab.setLayout(layout)

    def create_stats_tab(self):
        """Стварыць укладку статыстыкі - максімальны памер"""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        stats_title = QLabel("📊 Статыстыка аналізу")
        stats_title.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 12px; margin-bottom: 5px;")

        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 10px;
                font-size: 11px;
                line-height: 1.4;
                color: #333333;
            }
        """)

        layout.addWidget(stats_title, stretch=0)
        layout.addWidget(self.stats_text, stretch=1)  # Тэкст займае ўсё месца
        self.stats_tab.setLayout(layout)

    def create_status_bar(self):
        """Стварыць статус-бар"""
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #34495e;
                color: white;
                font-weight: bold;
                font-size: 9px;
                height: 18px;
            }
        """)
        self.statusBar().showMessage("✅ Гатова да работы")

    def on_folder_changed(self, text):
        """Абнаўленне інфармацыі пра абраную папку"""
        if text and os.path.exists(text):
            # Падлік файлаў у папцы
            image_count = 0
            supported_formats = {'.jpg', '.jpeg', '.gif', '.tif', '.tiff', '.bmp', '.png', '.pcx'}

            try:
                for file in os.listdir(text):
                    if os.path.splitext(file)[1].lower() in supported_formats:
                        image_count += 1
            except:
                image_count = 0

            # Кароткая інфармацыя
            short_path = text
            if len(text) > 50:
                short_path = "..." + text[-47:]

            self.folder_info.setText(f"📁 Файлаў: {image_count} | 📂 {short_path}")
            self.folder_info.setStyleSheet("""
                QLabel {
                    color: #27ae60;
                    font-size: 9px;
                    font-weight: bold;
                    padding: 3px;
                    background-color: #d5f4e6;
                    border-radius: 3px;
                    border: 1px solid #2ecc71;
                }
            """)
        else:
            self.folder_info.setText("Папка не абраная")
            self.folder_info.setStyleSheet("""
                QLabel {
                    color: #e74c3c;
                    font-size: 9px;
                    font-style: italic;
                    padding: 3px;
                    background-color: #fadbd8;
                    border-radius: 3px;
                    border: 1px dashed #e74c3c;
                }
            """)

    # Астатнія метады застаюцца без зменаў (для кароткасці)
    # ... (browse_folder, start_analysis, update_progress, analysis_finished, display_results,
    # update_stats, show_file_details, export_results, update_ui, closeEvent застаюцца такімі ж)

    def browse_folder(self):
        """Абраць папку для аналізу"""
        folder = QFileDialog.getExistingDirectory(self, "Абраць папку з малюнкамі")
        if folder:
            self.path_edit.setText(folder)
            self.statusBar().showMessage(f"✅ Абраная папка: {folder}")

    def start_analysis(self):
        """Пачаць аналіз малюнкаў"""
        folder_path = self.path_edit.text()

        if not folder_path or not os.path.exists(folder_path):
            QMessageBox.warning(self, "⚠️ Памылка", "Калі ласка, абярыце сапраўдную папку")
            return

        # Блакіроўка элементаў кіравання
        self.analyze_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.export_btn.setEnabled(False)

        # Налады прагрэсу
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("🔄 Аналіз...")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                font-weight: bold;
                padding: 4px;
                background-color: #fdebd0;
                border-radius: 3px;
                border: 1px solid #f39c12;
                color: #e67e22;
            }
        """)

        # Запуск у асобным патоку
        self.analysis_thread = AnalysisThread(folder_path)
        self.analysis_thread.progress.connect(self.update_progress)
        self.analysis_thread.finished.connect(self.analysis_finished)
        self.analysis_thread.start()

        self.statusBar().showMessage(f"🔄 Аналіз малюнкаў...")

    def update_progress(self, current, total, filename):
        """Абнавіць прагрэс"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        percent = (current / total) * 100 if total > 0 else 0
        short_filename = filename
        if len(filename) > 30:
            short_filename = "..." + filename[-27:]
        self.progress_details.setText(f"{current}/{total} ({percent:.1f}%) | {short_filename}")

    def analysis_finished(self, results):
        """Апрацоўка завяршэння аналізу"""
        self.current_results = results

        # Разблакіроўка элементаў кіравання
        self.analyze_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.export_btn.setEnabled(True)

        if 'error' in results:
            QMessageBox.critical(self, "❌ Памылка", results['error'])
            self.status_label.setText("❌ Памылка")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 10px;
                    font-weight: bold;
                    padding: 4px;
                    background-color: #fadbd8;
                    border-radius: 3px;
                    border: 1px solid #e74c3c;
                    color: #c0392b;
                }
            """)
        else:
            self.display_results(results)
            self.status_label.setText(f"✅ Завершана: {len(results['results'])}")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 10px;
                    font-weight: bold;
                    padding: 4px;
                    background-color: #d5f4e6;
                    border-radius: 3px;
                    border: 1px solid #2ecc71;
                    color: #27ae60;
                }
            """)
            self.export_btn.setEnabled(True)

        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("✅ Аналіз завершаны")

    def display_results(self, results):
        """Адлюстраваць вынікі ў табліцы"""
        self.results_table.setRowCount(0)

        for i, result in enumerate(results['results']):
            self.results_table.insertRow(i)

            # Эмаджы для статуса
            status_icon = "✅" if 'error' not in result else "❌"
            status_text = "OK" if 'error' not in result else result['error'][:20] + "..."

            # Інфармацыя пра квантаванне
            quantization = result.get('quantization_short', 'N/A')

            # Запаўненне радка
            items = [
                result.get('filename', 'N/A'),
                result.get('image_size', 'N/A'),
                result.get('dpi', '72 DPI'),
                result.get('color_depth', 'N/A'),
                result.get('compression', 'N/A'),
                result.get('image_format', 'N/A'),
                result.get('file_size', 'N/A'),
                quantization,  # Новы слупок з квантаваннем
                result.get('file_path', 'N/A'),
                f"{status_icon} {status_text}"
            ]

            for col, text in enumerate(items):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if 'error' in result:
                    item.setBackground(QColor(255, 235, 238))
                    item.setForeground(QColor(192, 57, 43))
                elif i % 2 == 0:
                    item.setBackground(QColor(245, 245, 245))
                    item.setForeground(QColor(51, 51, 51))
                else:
                    item.setBackground(QColor(255, 255, 255))
                    item.setForeground(QColor(51, 51, 51))

                self.results_table.setItem(i, col, item)

        self.update_stats(results)

    def update_stats(self, results):
        """Абнавіць укладку статыстыкі"""
        from image_analyzer import ImageAnalyzer
        analyzer = ImageAnalyzer()
        stats = analyzer.get_summary_stats(results)

        stats_text = "=== СТАТЫСТЫКА АНАЛІЗУ ===\n\n"

        if 'summary' in results:
            summary = results['summary']
            stats_text += f"Агульная інфармацыя:\n"
            stats_text += f"• Папка: {summary.get('folder_path', 'N/A')}\n"
            stats_text += f"• Усяго файлаў: {summary.get('total_files', 0)}\n"
            stats_text += f"• Апрацавана: {summary.get('processed', 0)}\n\n"

        stats_text += f"Вынікі апрацоўкі:\n"
        stats_text += f"• Паспяхова: {stats.get('successful', 0)}\n"
        stats_text += f"• З памылкамі: {stats.get('errors', 0)}\n"
        stats_text += f"• Агульны памер: {stats.get('total_size', 'N/A')}\n\n"

        stats_text += "Размеркаванне па фарматах:\n"
        for fmt, count in stats.get('formats', {}).items():
            stats_text += f"• {fmt}: {count} файлаў\n"

        self.stats_text.setText(stats_text)

    def show_file_details(self, index):
        """Паказаць дэтальныя звесткі пра файл"""
        row = index.row()
        if not self.current_results or row >= len(self.current_results['results']):
            return

        result = self.current_results['results'][row]
        details = "=== ДЭТАЛЬНЫЯ ЗВЕСТКІ ===\n\n"

        if 'error' in result:
            details += f"❌ Памылка: {result['error']}\n"
        else:
            # Асноўная інфармацыя
            details += f"📁 Поўны шлях: {result.get('file_path', 'N/A')}\n"
            details += f"📄 Імя файла: {result.get('filename', 'N/A')}\n"
            details += f"🖼️ Фармат: {result.get('image_format', 'N/A')}\n"
            details += f"📏 Памер малюнка: {result.get('image_size', 'N/A')}\n"
            details += f"🎨 Глыбіня колеру: {result.get('color_depth', 'N/A')}\n"
            details += f"🎯 Дазвол: {result.get('dpi', 'N/A')}\n"
            details += f"💾 Сціск: {result.get('compression', 'N/A')}\n"
            details += f"📊 Памер файла: {result.get('file_size', 'N/A')}\n"
            details += f"🔢 Квантаванне: {result.get('quantization_short', 'N/A')}\n\n"

            # Дэталі квантавання
            if 'quantization_tables_count' in result:
                details += f"🔧 Квантаванне:\n"
                details += f"• Колькасць табліц: {result.get('quantization_tables_count', 'N/A')}\n"
                details += f"• Памер табліцы: {result.get('quantization_table_size', 'N/A')}\n\n"

            # Дадатковая інфармацыя з formats_info.py
            details += "🔧 Тэхнічныя дэталі:\n"

            if 'exif_keys_count' in result:
                details += f"• Колькасць EXIF тэгаў: {result.get('exif_keys_count', 0)}\n"

            if 'gif_palette_colors' in result:
                details += f"• Колькасць колераў у палітры GIF: {result.get('gif_palette_colors', 'N/A')}\n"

            if 'gif_frames_count' in result and result.get('gif_frames_count', 1) > 1:
                details += f"• Колькасць кадраў GIF: {result.get('gif_frames_count', 1)}\n"

            if 'jpeg_quantization_tables' in result:
                details += f"• Табліцы квантавання JPEG: {result.get('jpeg_quantization_tables', {})}\n"

            if 'tiff_tags_count' in result:
                details += f"• Колькасць TIFF тэгаў: {result.get('tiff_tags_count', 0)}\n"

        self.details_text.setText(details)

    def export_results(self):
        """Экспартаваць вынікі ў файл"""
        if not self.current_results:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Захаваць вынікі", "image_analysis_results.txt", "Text Files (*.txt)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("Image Metadata Analysis Results\n")
                    f.write("=" * 50 + "\n\n")

                    for result in self.current_results['results']:
                        f.write(f"File: {result.get('filename', 'N/A')}\n")
                        f.write(f"Full Path: {result.get('file_path', 'N/A')}\n")
                        f.write("-" * 40 + "\n")

                        for key, value in result.items():
                            if key not in ['file_path']:
                                f.write(f"{key}: {value}\n")

                        f.write("\n")

                QMessageBox.information(self, "✅ Экспарт", "Вынікі паспяхова экспартаваны!")
            except Exception as e:
                QMessageBox.critical(self, "❌ Памылка", f"Памылка экспарту: {str(e)}")

    def update_ui(self):
        """Перыядычнае абнаўленне інтэрфейсу"""
        pass

    def closeEvent(self, event):
        """Апрацоўка закрыцця акна"""
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.analysis_thread.terminate()
            self.analysis_thread.wait()
        event.accept()

# Запуск праграмы
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

    def show_file_details(self, index):
        """Паказаць дэтальныя звесткі пра файл"""
        row = index.row()
        if not self.current_results or row >= len(self.current_results['results']):
            return

        result = self.current_results['results'][row]
        details = "=== ДЭТАЛЬНЫЯ ЗВЕСТКІ ===\n\n"

        if 'error' in result:
            details += f"❌ Памылка: {result['error']}\n"
        else:
            # Асноўная інфармацыя
            details += f"📁 Поўны шлях: {result.get('file_path', 'N/A')}\n"
            details += f"📄 Імя файла: {result.get('filename', 'N/A')}\n"
            details += f"🖼️ Фармат: {result.get('image_format', 'N/A')}\n"
            details += f"📏 Памер малюнка: {result.get('image_size', 'N/A')}\n"
            details += f"🎨 Глыбіня колеру: {result.get('color_depth', 'N/A')}\n"
            details += f"🎯 Дазвол: {result.get('dpi', 'N/A')}\n"
            details += f"💾 Сціск: {result.get('compression', 'N/A')}\n"
            details += f"📊 Памер файла: {result.get('file_size', 'N/A')}\n\n"

            # Дадатковая інфармацыя з formats_info.py
            details += "🔧 Тэхнічныя дэталі:\n"

            if 'exif_keys_count' in result:
                details += f"• Колькасць EXIF тэгаў: {result.get('exif_keys_count', 0)}\n"

            if 'gif_palette_colors' in result:
                details += f"• Колькасць колераў у палітры GIF: {result.get('gif_palette_colors', 'N/A')}\n"

            if 'gif_frames_count' in result and result.get('gif_frames_count', 1) > 1:
                details += f"• Колькасць кадраў GIF: {result.get('gif_frames_count', 1)}\n"

            if 'jpeg_quantization_tables' in result:
                details += f"• Табліцы квантавання JPEG: {result.get('jpeg_quantization_tables', {})}\n"

            if 'tiff_tags_count' in result:
                details += f"• Колькасць TIFF тэгаў: {result.get('tiff_tags_count', 0)}\n"

        self.details_text.setText(details)
