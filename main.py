"""
JXR → PNG Auto-Converter
Entry point for the application.

Monitors NVIDIA screenshot folders for new .jxr HDR files
and automatically converts them to PNG using jxr_to_png.exe.
"""

import sys
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


def main():
    # Ensure high DPI scaling works properly on Windows
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt

    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running in tray

    # Check for single instance using a lock file approach
    lock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".lock")

    # Simple single-instance check
    import socket
    _lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        _lock_socket.bind(('127.0.0.1', 47291))
    except socket.error:
        from PyQt5.QtWidgets import QMessageBox
        from translations import t
        QMessageBox.warning(
            None,
            t("already_running_title"),
            t("already_running_msg")
        )
        sys.exit(0)

    from ui import MainWindow

    window = MainWindow()
    window.show()

    logger.info("Application started.")

    exit_code = app.exec_()

    # Cleanup
    _lock_socket.close()
    logger.info("Application exited.")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
