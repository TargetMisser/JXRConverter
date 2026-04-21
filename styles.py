"""
Centralized QSS stylesheet for the JXR → PNG Converter app.
Premium dark theme with purple/blue accents.
"""

DARK_STYLESHEET = """
/* ── Global ── */
* {
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 13px;
    color: #e2e8f0;
}

QMainWindow {
    background-color: #0f0f1a;
}

QWidget#centralWidget {
    background-color: #0f0f1a;
}

/* ── Cards / Frames ── */
QFrame#configCard, QFrame#logCard, QFrame#statsCard {
    background-color: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 12px;
    padding: 16px;
}

QFrame#configCard:hover, QFrame#logCard:hover, QFrame#statsCard:hover {
    border: 1px solid #3a3a6a;
}

/* ── Labels ── */
QLabel {
    background: transparent;
    border: none;
}

QLabel#titleLabel {
    font-size: 22px;
    font-weight: bold;
    color: #ffffff;
}

QLabel#subtitleLabel {
    font-size: 12px;
    color: #8b8ba7;
    margin-bottom: 8px;
}

QLabel#sectionTitle {
    font-size: 14px;
    font-weight: 600;
    color: #c4b5fd;
    margin-bottom: 4px;
}

QLabel#statusLabel {
    font-size: 13px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 8px;
}

QLabel#statusActive {
    background-color: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.3);
}

QLabel#statusInactive {
    background-color: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

QLabel#statValue {
    font-size: 28px;
    font-weight: bold;
    color: #ffffff;
}

QLabel#statLabel {
    font-size: 11px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Line Edits ── */
QLineEdit {
    background-color: #12122a;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 8px 12px;
    color: #e2e8f0;
    selection-background-color: #6366f1;
}

QLineEdit:focus {
    border: 1px solid #6366f1;
}

QLineEdit:hover {
    border: 1px solid #3a3a6a;
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
        stop:0 #6366f1, stop:1 #8b5cf6);
    color: #ffffff;
    padding: 10px 24px;
    font-size: 14px;
}

QPushButton#primaryBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7c7ff7, stop:1 #a78bfa);
}

QPushButton#primaryBtn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4f46e5, stop:1 #7c3aed);
}

QPushButton#stopBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #dc2626, stop:1 #ef4444);
    color: #ffffff;
    padding: 10px 24px;
    font-size: 14px;
}

QPushButton#stopBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #ef4444, stop:1 #f87171);
}

QPushButton#stopBtn:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #b91c1c, stop:1 #dc2626);
}

QPushButton#browseBtn {
    background-color: #2a2a4a;
    color: #c4b5fd;
    padding: 8px 14px;
    min-width: 30px;
}

QPushButton#browseBtn:hover {
    background-color: #3a3a6a;
}

QPushButton#secondaryBtn {
    background-color: #1e1e3a;
    color: #a5b4fc;
    border: 1px solid #2a2a4a;
    padding: 8px 18px;
}

QPushButton#secondaryBtn:hover {
    background-color: #2a2a4a;
    border: 1px solid #6366f1;
}

QPushButton#secondaryBtn:pressed {
    background-color: #1a1a30;
}

/* ── List Widget (Log) ── */
QListWidget {
    background-color: #12122a;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 4px;
    outline: none;
}

QListWidget::item {
    background-color: transparent;
    border-bottom: 1px solid #1a1a35;
    padding: 8px 10px;
    border-radius: 4px;
    margin: 1px 2px;
}

QListWidget::item:hover {
    background-color: rgba(99, 102, 241, 0.08);
}

QListWidget::item:selected {
    background-color: rgba(99, 102, 241, 0.15);
    color: #e2e8f0;
}

/* ── Scrollbar ── */
QScrollBar:vertical {
    background-color: #0f0f1a;
    width: 8px;
    margin: 0;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #2a2a4a;
    min-height: 30px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #3a3a6a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

/* ── Tool Tips ── */
QToolTip {
    background-color: #1a1a2e;
    color: #e2e8f0;
    border: 1px solid #3a3a6a;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}

/* ── Menu (System Tray) ── */
QMenu {
    background-color: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 24px;
    border-radius: 4px;
    margin: 2px 4px;
}

QMenu::item:selected {
    background-color: rgba(99, 102, 241, 0.2);
}

QMenu::separator {
    height: 1px;
    background-color: #2a2a4a;
    margin: 4px 8px;
}

/* ── ComboBox (Language Selector) ── */
QComboBox {
    background-color: #12122a;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 7px 12px;
    color: #e2e8f0;
    font-size: 13px;
    min-height: 20px;
}

QComboBox:hover {
    border: 1px solid #3a3a6a;
}

QComboBox:focus {
    border: 1px solid #6366f1;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid #2a2a4a;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    background-color: #1a1a2e;
}

QComboBox::down-arrow {
    width: 10px;
    height: 10px;
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%238b8ba7' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
}

QComboBox QAbstractItemView {
    background-color: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 4px;
    selection-background-color: rgba(99, 102, 241, 0.2);
    selection-color: #e2e8f0;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    border-radius: 4px;
    min-height: 24px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: rgba(99, 102, 241, 0.12);
}

/* ── CheckBox ── */
QCheckBox {
    spacing: 8px;
    color: #e2e8f0;
    font-size: 13px;
    background: transparent;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background-color: #12122a;
    border: 1px solid #2a2a4a;
    border-radius: 4px;
}

QCheckBox::indicator:hover {
    border: 1px solid #3a3a6a;
}

QCheckBox::indicator:checked {
    background-color: #6366f1;
    border: 1px solid #6366f1;
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
}
"""
