"""
Inline SVG icons and pixmaps for the JXR → PNG Converter app.
No external icon files needed.
"""

from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QFont, QLinearGradient
from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgRenderer
from io import BytesIO


APP_ICON_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6366f1"/>
      <stop offset="100%" style="stop-color:#8b5cf6"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="60" height="60" rx="14" fill="url(#bg)"/>
  <path d="M18 20 L28 20 L28 26 L22 26 L22 38 L28 38 L28 44 L18 44 Z"
        fill="white" opacity="0.9"/>
  <path d="M32 22 L46 32 L32 42 Z"
        fill="white" opacity="0.9"/>
  <rect x="16" y="18" width="2" height="28" rx="1" fill="white" opacity="0.4"/>
</svg>"""

TRAY_ICON_ACTIVE_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6366f1"/>
      <stop offset="100%" style="stop-color:#8b5cf6"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="30" height="30" rx="7" fill="url(#bg)"/>
  <circle cx="16" cy="16" r="5" fill="white" opacity="0.9"/>
  <circle cx="16" cy="16" r="8" fill="none" stroke="white" stroke-width="1.5" opacity="0.4"/>
</svg>"""

TRAY_ICON_IDLE_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <rect x="1" y="1" width="30" height="30" rx="7" fill="#3a3a6a"/>
  <circle cx="16" cy="16" r="5" fill="white" opacity="0.5"/>
  <circle cx="16" cy="16" r="8" fill="none" stroke="white" stroke-width="1.5" opacity="0.2"/>
</svg>"""


def svg_to_pixmap(svg_string: str, size: int = 64) -> QPixmap:
    """Convert an SVG string to a QPixmap."""
    renderer = QSvgRenderer(svg_string.encode('utf-8'))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


def svg_to_icon(svg_string: str, size: int = 64) -> QIcon:
    """Convert an SVG string to a QIcon."""
    return QIcon(svg_to_pixmap(svg_string, size))


def get_app_icon() -> QIcon:
    """Get the application icon."""
    icon = QIcon()
    for s in [16, 24, 32, 48, 64]:
        icon.addPixmap(svg_to_pixmap(APP_ICON_SVG, s))
    return icon


def get_tray_icon_active() -> QIcon:
    """Get the active (monitoring) tray icon."""
    icon = QIcon()
    for s in [16, 24, 32]:
        icon.addPixmap(svg_to_pixmap(TRAY_ICON_ACTIVE_SVG, s))
    return icon


def get_tray_icon_idle() -> QIcon:
    """Get the idle (not monitoring) tray icon."""
    icon = QIcon()
    for s in [16, 24, 32]:
        icon.addPixmap(svg_to_pixmap(TRAY_ICON_IDLE_SVG, s))
    return icon
