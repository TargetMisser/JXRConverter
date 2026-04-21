"""
Centralized QSS stylesheet for the JXR → PNG Converter app.
Premium dark theme with purple/blue accents.
"""

DARK_STYLESHEET = """
/* ── Global ── */
* {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    color: #ffffff;
}

QMainWindow {
    background-color: #101217;
}

QWidget#centralWidget {
    background-color: #101217;
}

/* ── Cards / Frames ── */
QFrame#configCard, QFrame#logCard, QFrame#statsCard {
    background-color: #1A1D23;
    border: 1px solid #2A2F3A;
    border-radius: 12px;
    padding: 24px;
}

QFrame#configCard:hover, QFrame#logCard:hover, QFrame#statsCard:hover {
    border: 1px solid #3A404F;
}

/* ── Labels ── */
QLabel {
    background: transparent;
    border: none;
}

QLabel#titleLabel {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
}

QLabel#subtitleLabel {
    font-size: 14px;
    color: #C5C6CB;
    margin-bottom: 12px;
}

QLabel#sectionTitle {
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

QLabel#statusLabel {
    font-size: 13px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 8px;
}

QLabel#statusActive {
    background-color: rgba(43, 108, 238, 0.1);
    color: #2B6CEE;
    border: 1px solid rgba(43, 108, 238, 0.3);
}

QLabel#statusInactive {
    background-color: rgba(255, 180, 171, 0.1);
    color: #ffb4ab;
    border: 1px solid rgba(255, 180, 171, 0.3);
}

QLabel#statValue {
    font-size: 36px;
    font-weight: 800;
    color: #ffffff;
}

QLabel#statLabel {
    font-size: 12px;
    color: #8E9195;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

/* ── Line Edits ── */
QLineEdit {
    background-color: #101217;
    border: 1px solid #2A2F3A;
    border-radius: 8px;
    padding: 10px 14px;
    color: #ffffff;
    selection-background-color: #2B6CEE;
}

QLineEdit:focus {
    border: 1px solid #2B6CEE;
    background-color: rgba(43, 108, 238, 0.05);
}

QLineEdit:hover {
    border: 1px solid #3A404F;
}

/* ── Push Buttons ── */
QPushButton {
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
}

QPushButton#primaryBtn {
    background-color: #2B6CEE;
    color: #ffffff;
    padding: 12px 28px;
    font-size: 15px;
    font-weight: 700;
}

QPushButton#primaryBtn:hover {
    background-color: #1a5bdd;
}

QPushButton#primaryBtn:pressed {
    background-color: #124ebd;
}

QPushButton#stopBtn {
    background-color: #93000a;
    color: #ffffff;
    padding: 12px 28px;
    font-size: 15px;
    font-weight: 700;
}

QPushButton#stopBtn:hover {
    background-color: #ba1a1a;
}

QPushButton#stopBtn:pressed {
    background-color: #690005;
}

QPushButton#browseBtn {
    background-color: rgba(43, 108, 238, 0.1);
    color: #2B6CEE;
    border: 1px solid rgba(43, 108, 238, 0.3);
    padding: 8px 16px;
    border-radius: 8px;
}

QPushButton#browseBtn:hover {
    background-color: rgba(43, 108, 238, 0.2);
    border: 1px solid #2B6CEE;
}

QPushButton#secondaryBtn {
    background-color: #1A1D23;
    color: #C5C6CB;
    border: 1px solid #2A2F3A;
    padding: 8px 18px;
    border-radius: 8px;
}

QPushButton#secondaryBtn:hover {
    background-color: #2A2F3A;
    border: 1px solid #3A404F;
    color: #ffffff;
}

QPushButton#secondaryBtn:pressed {
    background-color: #101217;
}

/* ── List Widget (Log) ── */
QListWidget {
    background-color: #101217;
    border: 1px solid #2A2F3A;
    border-radius: 8px;
    padding: 6px;
    outline: none;
}

QListWidget::item {
    background-color: transparent;
    border-bottom: 1px solid #1A1D23;
    padding: 12px 14px;
    border-radius: 4px;
    margin: 1px 2px;
}

QListWidget::item:hover {
    background-color: rgba(43, 108, 238, 0.05);
}

QListWidget::item:selected {
    background-color: rgba(43, 108, 238, 0.15);
    color: #ffffff;
}

/* ── Scrollbar ── */
QScrollBar:vertical {
    background-color: #101217;
    width: 8px;
    margin: 0;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #2A2F3A;
    min-height: 40px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #3A404F;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

/* ── Tool Tips ── */
QToolTip {
    background-color: #1A1D23;
    color: #ffffff;
    border: 1px solid #2A2F3A;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
}

/* ── Menu (System Tray) ── */
QMenu {
    background-color: #1A1D23;
    border: 1px solid #2A2F3A;
    border-radius: 8px;
    padding: 6px;
}

QMenu::item {
    padding: 8px 24px;
    border-radius: 4px;
    margin: 2px 4px;
}

QMenu::item:selected {
    background-color: rgba(43, 108, 238, 0.2);
}

QMenu::separator {
    height: 1px;
    background-color: #2A2F3A;
    margin: 4px 8px;
}

/* ── ComboBox (Language Selector) ── */
QComboBox {
    background-color: #101217;
    border: 1px solid #2A2F3A;
    border-radius: 8px;
    padding: 8px 14px;
    color: #ffffff;
    font-size: 13px;
    min-height: 20px;
}

QComboBox:hover {
    border: 1px solid #3A404F;
}

QComboBox:focus {
    border: 1px solid #2B6CEE;
    background-color: rgba(43, 108, 238, 0.05);
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid #2A2F3A;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    background-color: #1A1D23;
}

QComboBox::down-arrow {
    width: 10px;
    height: 10px;
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%23C5C6CB' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
}

QComboBox QAbstractItemView {
    background-color: #1A1D23;
    border: 1px solid #2A2F3A;
    border-radius: 8px;
    padding: 4px;
    selection-background-color: rgba(43, 108, 238, 0.2);
    selection-color: #ffffff;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    border-radius: 4px;
    min-height: 24px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: rgba(43, 108, 238, 0.1);
}

/* ── CheckBox ── */
QCheckBox {
    spacing: 8px;
    color: #ffffff;
    font-size: 13px;
    background: transparent;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background-color: #101217;
    border: 1px solid #2A2F3A;
    border-radius: 4px;
}

QCheckBox::indicator:hover {
    border: 1px solid #3A404F;
}

QCheckBox::indicator:checked {
    background-color: #2B6CEE;
    border: 1px solid #2B6CEE;
    image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
}
"""

