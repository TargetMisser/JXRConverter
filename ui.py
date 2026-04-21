"""
Main window and system tray for the JXR → PNG Converter app.
Premium dark-mode PyQt5 interface with multi-language support.
"""

import json
import os
import logging
from pathlib import Path
from datetime import datetime

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget, QListWidgetItem, QFrame,
    QFileDialog, QSystemTrayIcon, QMenu, QAction, QApplication,
    QSizePolicy, QGraphicsOpacityEffect, QMessageBox, QSpacerItem, QCheckBox,
    QComboBox
)
from PyQt5.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize, pyqtSlot
)
from PyQt5.QtGui import QIcon, QFont, QColor

from styles import DARK_STYLESHEET
from resources import get_app_icon, get_tray_icon_active, get_tray_icon_idle
from converter import (
    FileWatcherThread, ConversionWorker, ConversionResult,
    find_unconverted_jxr_files
)
from translations import (
    t, set_language, get_language, detect_system_language,
    LANGUAGES, TRANSLATIONS
)

logger = logging.getLogger(__name__)

import sys

def get_app_dir():
    """Return the base directory for resources based on whether we are frozen or running as a script."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_appdata_dir():
    """Return the APPDATA directory for config saving."""
    appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
    config_dir = os.path.join(appdata, "JXRConverter")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

CONFIG_FILE = os.path.join(get_appdata_dir(), "config.json")

DEFAULT_CONFIG = {
    "watch_path": r"C:\Users\turni\Videos\NVIDIA",
    "jxr_exe_path": os.path.join(get_app_dir(), "hdrfix.exe"),
    "start_minimized": False,
    "auto_start_monitoring": True,
    "minimize_to_tray": True,
    "language": "",  # empty = auto-detect system language
}


def load_config() -> dict:
    """Load configuration from JSON file."""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
    except Exception as e:
        logger.warning(f"Error loading config: {e}")
    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    """Save configuration to JSON file."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.warning(f"Error saving config: {e}")


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.is_monitoring = False
        self.conversion_count = 0
        self.error_count = 0
        self.watcher_thread = None
        self.converter_thread = None

        # Initialize language from config or system
        saved_lang = self.config.get("language", "")
        if saved_lang and saved_lang in TRANSLATIONS:
            set_language(saved_lang)
        else:
            detected = detect_system_language()
            set_language(detected)
            self.config["language"] = detected
            save_config(self.config)

        self._setup_ui()
        self._setup_tray()
        self._connect_signals()

        # Auto-start monitoring if configured
        if self.config.get("auto_start_monitoring", True):
            QTimer.singleShot(500, self.start_monitoring)

    def _setup_ui(self):
        """Build the main UI."""
        self.setWindowTitle(t("window_title"))
        self.setWindowIcon(get_app_icon())
        self.setMinimumSize(620, 740)
        self.resize(660, 820)
        self.setStyleSheet(DARK_STYLESHEET)

        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # ── Header ──
        header_layout = QVBoxLayout()
        header_layout.setSpacing(2)

        self.title_label = QLabel(t("header_title"))
        self.title_label.setObjectName("titleLabel")
        header_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel(t("header_subtitle"))
        self.subtitle_label.setObjectName("subtitleLabel")
        header_layout.addWidget(self.subtitle_label)

        main_layout.addLayout(header_layout)

        # ── Status bar ──
        status_row = QHBoxLayout()
        self.status_label = QLabel(t("status_inactive"))
        self.status_label.setObjectName("statusInactive")
        self.status_label.setFixedHeight(34)
        status_row.addWidget(self.status_label)
        status_row.addStretch()

        self.queue_label = QLabel("")
        self.queue_label.setObjectName("subtitleLabel")
        status_row.addWidget(self.queue_label)

        main_layout.addLayout(status_row)

        # ── Config Card ──
        config_card = QFrame()
        config_card.setObjectName("configCard")
        config_layout = QVBoxLayout(config_card)
        config_layout.setSpacing(10)

        self.config_title_label = QLabel(t("config_title"))
        self.config_title_label.setObjectName("sectionTitle")
        config_layout.addWidget(self.config_title_label)

        # Watch folder
        self.watch_label = QLabel(t("watch_folder_label"))
        self.watch_label.setStyleSheet("color: #8b8ba7; font-size: 11px;")
        config_layout.addWidget(self.watch_label)

        watch_row = QHBoxLayout()
        self.watch_input = QLineEdit(self.config.get("watch_path", ""))
        self.watch_input.setPlaceholderText(t("watch_folder_placeholder"))
        watch_row.addWidget(self.watch_input)

        self.watch_browse_btn = QPushButton("📁")
        self.watch_browse_btn.setObjectName("browseBtn")
        self.watch_browse_btn.setToolTip(t("browse_tooltip"))
        self.watch_browse_btn.clicked.connect(self._browse_watch_folder)
        watch_row.addWidget(self.watch_browse_btn)
        config_layout.addLayout(watch_row)

        # hdrfix.exe path
        self.exe_label = QLabel(t("exe_path_label"))
        self.exe_label.setStyleSheet("color: #8b8ba7; font-size: 11px;")
        config_layout.addWidget(self.exe_label)

        exe_row = QHBoxLayout()
        self.exe_input = QLineEdit(self.config.get("jxr_exe_path", ""))
        self.exe_input.setPlaceholderText(t("exe_path_placeholder"))
        exe_row.addWidget(self.exe_input)

        self.exe_browse_btn = QPushButton("📁")
        self.exe_browse_btn.clicked.connect(self._browse_exe)
        exe_row.addWidget(self.exe_browse_btn)
        config_layout.addLayout(exe_row)

        # Minimize to tray toggle
        self.tray_checkbox = QCheckBox(t("tray_checkbox"))
        self.tray_checkbox.setChecked(self.config.get("minimize_to_tray", True))
        self.tray_checkbox.setCursor(Qt.PointingHandCursor)
        config_layout.addWidget(self.tray_checkbox)

        # ── Language selector ──
        lang_row = QHBoxLayout()
        self.lang_label = QLabel(t("language_label"))
        self.lang_label.setStyleSheet("color: #8b8ba7; font-size: 11px;")
        lang_row.addWidget(self.lang_label)

        self.lang_combo = QComboBox()
        self.lang_combo.setObjectName("langCombo")
        self.lang_combo.setCursor(Qt.PointingHandCursor)
        # Populate with flag + language name
        lang_flags = {
            "it": "🇮🇹", "en": "🇬🇧", "es": "🇪🇸", "de": "🇩🇪", "fr": "🇫🇷",
            "pt": "🇧🇷", "ja": "🇯🇵", "zh": "🇨🇳", "ko": "🇰🇷", "ru": "🇷🇺",
        }
        current_lang = get_language()
        current_index = 0
        for i, (code, name) in enumerate(LANGUAGES.items()):
            flag = lang_flags.get(code, "🌐")
            self.lang_combo.addItem(f"{flag}  {name}", code)
            if code == current_lang:
                current_index = i
        self.lang_combo.setCurrentIndex(current_index)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)
        lang_row.addWidget(self.lang_combo, stretch=1)
        config_layout.addLayout(lang_row)

        main_layout.addWidget(config_card)

        # ── Action Buttons ──
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.toggle_btn = QPushButton(t("start_monitoring"))
        self.toggle_btn.setObjectName("primaryBtn")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_monitoring)
        btn_row.addWidget(self.toggle_btn)

        self.convert_all_btn = QPushButton(t("convert_existing"))
        self.convert_all_btn.setObjectName("secondaryBtn")
        self.convert_all_btn.setCursor(Qt.PointingHandCursor)
        self.convert_all_btn.setToolTip(t("convert_existing_tooltip"))
        self.convert_all_btn.clicked.connect(self._convert_existing)
        btn_row.addWidget(self.convert_all_btn)

        main_layout.addLayout(btn_row)

        # ── Stats Card ──
        stats_card = QFrame()
        stats_card.setObjectName("statsCard")
        stats_layout = QHBoxLayout(stats_card)
        stats_layout.setSpacing(20)

        # Conversions count
        conv_col = QVBoxLayout()
        conv_col.setAlignment(Qt.AlignCenter)
        self.stat_converted = QLabel("0")
        self.stat_converted.setObjectName("statValue")
        self.stat_converted.setAlignment(Qt.AlignCenter)
        conv_col.addWidget(self.stat_converted)
        self.conv_stat_label = QLabel(t("stat_converted"))
        self.conv_stat_label.setObjectName("statLabel")
        self.conv_stat_label.setAlignment(Qt.AlignCenter)
        conv_col.addWidget(self.conv_stat_label)
        stats_layout.addLayout(conv_col)

        # Separator
        sep1 = QFrame()
        sep1.setFixedWidth(1)
        sep1.setStyleSheet("background-color: #2a2a4a;")
        stats_layout.addWidget(sep1)

        # Errors count
        err_col = QVBoxLayout()
        err_col.setAlignment(Qt.AlignCenter)
        self.stat_errors = QLabel("0")
        self.stat_errors.setObjectName("statValue")
        self.stat_errors.setAlignment(Qt.AlignCenter)
        err_col.addWidget(self.stat_errors)
        self.err_stat_label = QLabel(t("stat_errors"))
        self.err_stat_label.setObjectName("statLabel")
        self.err_stat_label.setAlignment(Qt.AlignCenter)
        err_col.addWidget(self.err_stat_label)
        stats_layout.addLayout(err_col)

        # Separator
        sep2 = QFrame()
        sep2.setFixedWidth(1)
        sep2.setStyleSheet("background-color: #2a2a4a;")
        stats_layout.addWidget(sep2)

        # Last file
        last_col = QVBoxLayout()
        last_col.setAlignment(Qt.AlignCenter)
        self.stat_last_file = QLabel("—")
        self.stat_last_file.setObjectName("statValue")
        self.stat_last_file.setStyleSheet("font-size: 14px; color: #a5b4fc;")
        self.stat_last_file.setAlignment(Qt.AlignCenter)
        self.stat_last_file.setWordWrap(True)
        last_col.addWidget(self.stat_last_file)
        self.last_stat_label = QLabel(t("stat_last_file"))
        self.last_stat_label.setObjectName("statLabel")
        self.last_stat_label.setAlignment(Qt.AlignCenter)
        last_col.addWidget(self.last_stat_label)
        stats_layout.addLayout(last_col)

        main_layout.addWidget(stats_card)

        # ── Log Card ──
        log_card = QFrame()
        log_card.setObjectName("logCard")
        log_layout = QVBoxLayout(log_card)

        log_header = QHBoxLayout()
        self.log_title_label = QLabel(t("log_title"))
        self.log_title_label.setObjectName("sectionTitle")
        log_header.addWidget(self.log_title_label)
        log_header.addStretch()

        self.clear_btn = QPushButton(t("clear_btn"))
        self.clear_btn.setObjectName("secondaryBtn")
        self.clear_btn.setFixedHeight(28)
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self._clear_log)
        log_header.addWidget(self.clear_btn)
        log_layout.addLayout(log_header)

        self.log_list = QListWidget()
        self.log_list.setMinimumHeight(180)
        self.log_list.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        log_layout.addWidget(self.log_list)

        main_layout.addWidget(log_card, stretch=1)

    def _setup_tray(self):
        """Set up system tray icon and menu."""
        self.tray_icon = QSystemTrayIcon(get_tray_icon_idle(), self)

        self.tray_menu = QMenu()
        self.tray_menu.setStyleSheet(DARK_STYLESHEET)

        self.tray_toggle_action = QAction(t("tray_start"), self)
        self.tray_toggle_action.triggered.connect(self.toggle_monitoring)
        self.tray_menu.addAction(self.tray_toggle_action)

        self.tray_menu.addSeparator()

        self.tray_show_action = QAction(t("tray_show"), self)
        self.tray_show_action.triggered.connect(self._show_window)
        self.tray_menu.addAction(self.tray_show_action)

        self.tray_menu.addSeparator()

        self.tray_quit_action = QAction(t("tray_quit"), self)
        self.tray_quit_action.triggered.connect(self._quit_app)
        self.tray_menu.addAction(self.tray_quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self._tray_activated)
        self.tray_icon.setToolTip(t("tray_tooltip_idle"))
        self.tray_icon.show()

    def _connect_signals(self):
        """Connect internal signals."""
        self.watch_input.textChanged.connect(self._on_config_changed)
        self.exe_input.textChanged.connect(self._on_config_changed)
        self.tray_checkbox.stateChanged.connect(self._on_config_changed)

    # ── Language ──

    def _on_language_changed(self, index):
        """Handle language selector change."""
        lang_code = self.lang_combo.itemData(index)
        if lang_code and lang_code != get_language():
            set_language(lang_code)
            self.config["language"] = lang_code
            save_config(self.config)
            self._refresh_all_text()

    def _refresh_all_text(self):
        """Refresh all visible text after a language change."""
        # Window title
        self.setWindowTitle(t("window_title"))

        # Header
        self.title_label.setText(t("header_title"))
        self.subtitle_label.setText(t("header_subtitle"))

        # Status
        if self.is_monitoring:
            self.status_label.setText(t("status_active"))
        else:
            self.status_label.setText(t("status_inactive"))

        # Config section
        self.config_title_label.setText(t("config_title"))
        self.watch_label.setText(t("watch_folder_label"))
        self.watch_input.setPlaceholderText(t("watch_folder_placeholder"))
        self.watch_browse_btn.setToolTip(t("browse_tooltip"))
        self.exe_label.setText(t("exe_path_label"))
        self.exe_input.setPlaceholderText(t("exe_path_placeholder"))
        self.tray_checkbox.setText(t("tray_checkbox"))
        self.lang_label.setText(t("language_label"))

        # Action buttons
        if self.is_monitoring:
            self.toggle_btn.setText(t("stop_monitoring"))
        else:
            self.toggle_btn.setText(t("start_monitoring"))
        self.convert_all_btn.setText(t("convert_existing"))
        self.convert_all_btn.setToolTip(t("convert_existing_tooltip"))

        # Stats labels
        self.conv_stat_label.setText(t("stat_converted"))
        self.err_stat_label.setText(t("stat_errors"))
        self.last_stat_label.setText(t("stat_last_file"))

        # Log
        self.log_title_label.setText(t("log_title"))
        self.clear_btn.setText(t("clear_btn"))

        # Tray menu
        if self.is_monitoring:
            self.tray_toggle_action.setText(t("tray_stop"))
            self.tray_icon.setToolTip(t("tray_tooltip_active"))
        else:
            self.tray_toggle_action.setText(t("tray_start"))
            self.tray_icon.setToolTip(t("tray_tooltip_idle"))
        self.tray_show_action.setText(t("tray_show"))
        self.tray_quit_action.setText(t("tray_quit"))

    # ── Monitoring Control ──

    def toggle_monitoring(self):
        if self.is_monitoring:
            self.stop_monitoring()
        else:
            self.start_monitoring()

    def start_monitoring(self):
        """Start watching for new .jxr files."""
        watch_path = self.watch_input.text().strip()
        exe_path = self.exe_input.text().strip()

        # Validate paths
        if not watch_path or not os.path.isdir(watch_path):
            self._log_message(t("error_watch_invalid"), error=True)
            return

        if not exe_path or not os.path.isfile(exe_path):
            self._log_message(t("error_exe_not_found"), error=True)
            return

        # Start watcher thread
        self.watcher_thread = FileWatcherThread(watch_path)
        self.watcher_thread.file_detected.connect(self._on_file_detected)

        # Start converter thread
        self.converter_thread = ConversionWorker(exe_path)
        self.converter_thread.conversion_started.connect(self._on_conversion_started)
        self.converter_thread.conversion_finished.connect(self._on_conversion_finished)
        self.converter_thread.queue_size_changed.connect(self._on_queue_changed)

        self.watcher_thread.start()
        self.converter_thread.start()

        self.is_monitoring = True
        self._update_ui_state()
        self._log_message(t("monitoring_started", path=watch_path))

    def stop_monitoring(self):
        """Stop watching."""
        if self.watcher_thread:
            self.watcher_thread.stop()
            self.watcher_thread.wait(3000)
            self.watcher_thread = None

        if self.converter_thread:
            self.converter_thread.stop()
            self.converter_thread.wait(3000)
            self.converter_thread = None

        self.is_monitoring = False
        self._update_ui_state()
        self._log_message(t("monitoring_stopped"))

    def _update_ui_state(self):
        """Update UI elements based on monitoring state."""
        if self.is_monitoring:
            self.toggle_btn.setText(t("stop_monitoring"))
            self.toggle_btn.setObjectName("stopBtn")
            self.status_label.setText(t("status_active"))
            self.status_label.setObjectName("statusActive")
            self.tray_toggle_action.setText(t("tray_stop"))
            self.tray_icon.setIcon(get_tray_icon_active())
            self.tray_icon.setToolTip(t("tray_tooltip_active"))
            self.watch_input.setEnabled(False)
            self.exe_input.setEnabled(False)
        else:
            self.toggle_btn.setText(t("start_monitoring"))
            self.toggle_btn.setObjectName("primaryBtn")
            self.status_label.setText(t("status_inactive"))
            self.status_label.setObjectName("statusInactive")
            self.tray_toggle_action.setText(t("tray_start"))
            self.tray_icon.setIcon(get_tray_icon_idle())
            self.tray_icon.setToolTip(t("tray_tooltip_idle"))
            self.watch_input.setEnabled(True)
            self.exe_input.setEnabled(True)

        # Force stylesheet re-evaluation
        self.toggle_btn.style().unpolish(self.toggle_btn)
        self.toggle_btn.style().polish(self.toggle_btn)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

    # ── Slots ──

    @pyqtSlot(str)
    def _on_file_detected(self, file_path: str):
        """When a new .jxr file is detected by the watcher."""
        if self.converter_thread:
            self.converter_thread.add_file(file_path)

    @pyqtSlot(str)
    def _on_conversion_started(self, file_path: str):
        """When conversion begins."""
        name = Path(file_path).name
        self._log_message(t("converting", name=name))

    @pyqtSlot(object)
    def _on_conversion_finished(self, result: ConversionResult):
        """When a conversion completes."""
        name = Path(result.input_path).name
        if result.success:
            self.conversion_count += 1
            self.stat_converted.setText(str(self.conversion_count))
            self.stat_last_file.setText(name.replace('.jxr', '.png'))
            self._log_message(f"✅ {name} → {result.message}")

            # Show tray notification
            if not self.isVisible() or self.isMinimized():
                self.tray_icon.showMessage(
                    t("tray_conversion_done"),
                    t("tray_conversion_msg", name=name),
                    QSystemTrayIcon.Information, 2000
                )
        else:
            self.error_count += 1
            self.stat_errors.setText(str(self.error_count))
            self._log_message(f"❌ {name} → {result.message}", error=True)

    @pyqtSlot(int)
    def _on_queue_changed(self, size: int):
        """Update queue size display."""
        if size > 0:
            self.queue_label.setText(t("queue_label", size=size))
        else:
            self.queue_label.setText("")

    # ── Actions ──

    def _browse_watch_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, t("browse_watch_dialog"),
            self.watch_input.text() or r"C:\Users\turni\Videos"
        )
        if folder:
            self.watch_input.setText(folder)

    def _browse_exe(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, t("browse_exe_dialog"),
            self.exe_input.text() or r"C:\Users\turni\Videos",
            t("browse_exe_filter")
        )
        if file_path:
            self.exe_input.setText(file_path)

    def _convert_existing(self):
        """Convert all existing .jxr files that don't have a .png counterpart."""
        watch_path = self.watch_input.text().strip()
        exe_path = self.exe_input.text().strip()

        if not watch_path or not os.path.isdir(watch_path):
            self._log_message(t("error_watch_invalid"), error=True)
            return

        if not exe_path or not os.path.isfile(exe_path):
            self._log_message(t("error_jxr_exe_not_found"), error=True)
            return

        unconverted = find_unconverted_jxr_files(watch_path)

        if not unconverted:
            self._log_message(t("no_files_to_convert"))
            return

        self._log_message(t("files_found", count=len(unconverted)))

        # Ensure converter is running
        if not self.converter_thread or not self.converter_thread.isRunning():
            self.converter_thread = ConversionWorker(exe_path)
            self.converter_thread.conversion_started.connect(self._on_conversion_started)
            self.converter_thread.conversion_finished.connect(self._on_conversion_finished)
            self.converter_thread.queue_size_changed.connect(self._on_queue_changed)
            self.converter_thread.start()

        for f in unconverted:
            self.converter_thread.add_file(f)

    def _clear_log(self):
        self.log_list.clear()

    def _log_message(self, message: str, error: bool = False):
        """Add a message to the log list."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        item = QListWidgetItem(f"[{timestamp}]  {message}")

        if error:
            item.setForeground(QColor("#f87171"))
        elif "✅" in message:
            item.setForeground(QColor("#4ade80"))
        elif "⏳" in message:
            item.setForeground(QColor("#fbbf24"))
        elif "ℹ️" in message:
            item.setForeground(QColor("#60a5fa"))
        else:
            item.setForeground(QColor("#e2e8f0"))

        self.log_list.insertItem(0, item)

        # Keep log manageable
        while self.log_list.count() > 500:
            self.log_list.takeItem(self.log_list.count() - 1)

    def _on_config_changed(self):
        """Save config when paths change."""
        self.config["watch_path"] = self.watch_input.text().strip()
        self.config["jxr_exe_path"] = self.exe_input.text().strip()
        self.config["minimize_to_tray"] = self.tray_checkbox.isChecked()
        save_config(self.config)

    # ── Tray ──

    def _tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self._show_window()

    def _show_window(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def _quit_app(self):
        """Properly shut down the application."""
        self.stop_monitoring()
        self.tray_icon.hide()
        QApplication.instance().quit()

    # ── Window Events ──

    def closeEvent(self, event):
        """Handle window close event."""
        if self.config.get("minimize_to_tray", True):
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                t("tray_minimized_title"),
                t("tray_minimized_msg"),
                QSystemTrayIcon.Information, 2000
            )
        else:
            self._quit_app()
            event.accept()
