"""
Centralized QSS stylesheet for the JXR → PNG Converter app.
Premium dark theme with purple/blue accents.
"""

DARK_STYLESHEET = """
/* ── Global ── */
* {
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 13px;
    color: #e4e1e6;
}

QMainWindow {
    background-color: #0e0e11;
}

QWidget#centralWidget {
    background-color: #0e0e11;
}

/* ── Cards / Frames ── */
QFrame#configCard, QFrame#logCard, QFrame#statsCard {
    background-color: #1b1b1e;
    border: 1px solid #2a2a2d;
    border-radius: 12px;
    padding: 16px;
}

QFrame#configCard:hover, QFrame#logCard:hover, QFrame#statsCard:hover {
    border: 1px solid #504254;
}

/* ── Labels ── */
QLabel {
    background: transparent;
    border: none;
}

QLabel#titleLabel {
    font-size: 24px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
}

QLabel#subtitleLabel {
    font-size: 12px;
    color: #d4c0d7;
    margin-bottom: 8px;
}

QLabel#sectionTitle {
    font-size: 14px;
    font-weight: 700;
    color: #ebb2ff;
    margin-bottom: 4px;
}

QLabel#statusLabel {
    font-size: 13px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 8px;
}

QLabel#statusActive {
    background-color: rgba(0, 210, 253, 0.1);
    color: #00d2fd;
    border: 1px solid rgba(0, 210, 253, 0.3);
}

QLabel#statusInactive {
    background-color: rgba(255, 180, 171, 0.1);
    color: #ffb4ab;
    border: 1px solid rgba(255, 180, 171, 0.3);
}

QLabel#statValue {
    font-size: 32px;
    font-weight: 800;
    color: #ffffff;
}

QLabel#statLabel {
    font-size: 11px;
    color: #9d8ba0;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

/* ── Line Edits ── */
QLineEdit {
    background-color: #131316;
    border: 1px solid #2a2a2d;
    border-radius: 8px;
    padding: 8px 12px;
    color: #e4e1e6;
    selection-background-color: #bc13fe;
}

QLineEdit:focus {
    border: 1px solid #00d2fd;
    background-color: rgba(0, 210, 253, 0.05);
}

QLineEdit:hover {
    border: 1px solid #504254;
}

/* ── Push Buttons ── */
QPushButton {
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton#primaryBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #bc13fe, stop:1 #ebb2ff);
    color: #320047;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton#primaryBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #d13dff, stop:1 #f8d8ff);
}

QPushButton#primaryBtn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #9800d0, stop:1 #bc13fe);
}

QPushButton#stopBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #93000a, stop:1 #ffb4ab);
    color: #ffffff;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton#stopBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #ba1a1a, stop:1 #ffdad6);
}

QPushButton#stopBtn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #690005, stop:1 #93000a);
}

QPushButton#browseBtn {
    background-color: rgba(188, 19, 254, 0.1);
    color: #ebb2ff;
    border: 1px solid rgba(188, 19, 254, 0.3);
    padding: 8px 14px;
    min-width: 30px;
}

QPushButton#browseBtn:hover {
    background-color: rgba(188, 19, 254, 0.2);
    border: 1px solid #bc13fe;
}

QPushButton#secondaryBtn {
    background-color: #1b1b1e;
    color: #a2e7ff;
    border: 1px solid #504254;
    padding: 8px 18px;
}

QPushButton#secondaryBtn:hover {
    background-color: #2a2a2d;
    border: 1px solid #00d2fd;
    color: #00d2fd;
}

QPushButton#secondaryBtn:pressed {
    background-color: #131316;
}

/* ── List Widget (Log) ── */
QListWidget {
    background-color: #131316;
    border: 1px solid #2a2a2d;
    border-radius: 8px;
    padding: 4px;
    outline: none;
}

QListWidget::item {
    background-color: transparent;
    border-bottom: 1px solid #1b1b1e;
    padding: 10px 12px;
    border-radius: 4px;
    margin: 1px 2px;
}

QListWidget::item:hover {
    background-color: rgba(0, 210, 253, 0.05);
}

QListWidget::item:selected {
    background-color: rgba(188, 19, 254, 0.15);
    color: #e4e1e6;
}

/* ── Scrollbar ── */
QScrollBar:vertical {
    background-color: #0e0e11;
    width: 6px;
    margin: 0;
    border-radius: 3px;
}

QScrollBar::handle:vertical {
    background-color: #353438;
    min-height: 30px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background-color: #504254;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

/* ── Tool Tips ── */
QToolTip {
    background-color: #1b1b1e;
    color: #e4e1e6;
    border: 1px solid #504254;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}

/* ── Menu (System Tray) ── */
QMenu {
    background-color: #1b1b1e;
    border: 1px solid #2a2a2d;
    border-radius: 8px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 24px;
    border-radius: 4px;
    margin: 2px 4px;
}

QMenu::item:selected {
    background-color: rgba(188, 19, 254, 0.2);
}

QMenu::separator {
    height: 1px;
    background-color: #2a2a2d;
    margin: 4px 8px;
}

/* ── ComboBox (Language Selector) ── */
QComboBox {
    background-color: #131316;
    border: 1px solid #2a2a2d;
    border-radius: 8px;
    padding: 7px 12px;
    color: #e4e1e6;
    font-size: 13px;
    min-height: 20px;
}

QComboBox:hover {
    border: 1px solid #504254;
}

QComboBox:focus {
    border: 1px solid #00d2fd;
    background-color: rgba(0, 210, 253, 0.05);
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid #2a2a2d;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    background-color: #1b1b1e;
}

QComboBox::down-arrow {
    width: 10px;
    height: 10px;
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%23d4c0d7' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
}

QComboBox QAbstractItemView {
    background-color: #1b1b1e;
    border: 1px solid #2a2a2d;
    border-radius: 8px;
    padding: 4px;
    selection-background-color: rgba(188, 19, 254, 0.2);
    selection-color: #e4e1e6;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    border-radius: 4px;
    min-height: 24px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: rgba(0, 210, 253, 0.1);
}

/* ── CheckBox ── */
QCheckBox {
    spacing: 8px;
    color: #e4e1e6;
    font-size: 13px;
    background: transparent;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background-color: #131316;
    border: 1px solid #2a2a2d;
    border-radius: 4px;
}

QCheckBox::indicator:hover {
    border: 1px solid #504254;
}

QCheckBox::indicator:checked {
    background-color: #bc13fe;
    border: 1px solid #bc13fe;
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23320047' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
}
"""
