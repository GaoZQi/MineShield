from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt


class RoundWidget(QWidget):
    """
    A QWidget with customizable rounded corners and background color,
    without affecting child widget properties.

    Usage:
        widget = RoundWidget(radius=15, color=QColor(100, 150, 200))
    """

    def __init__(self, radius=10, color=QColor(255, 255, 255), parent=None):
        super().__init__(parent)
        self._radius = radius
        self._bg_color = color

    def setRadius(self, radius: int):
        """Set the corner radius (in pixels) and repaint the widget."""
        self._radius = radius
        self.update()

    def setBackgroundColor(self, color: QColor):
        """Set the background color and repaint the widget."""
        self._bg_color = color
        self.update()

    def paintEvent(self, event):
        """Override paintEvent to draw a rounded rectangle as the background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._bg_color)
        painter.drawRoundedRect(self.rect(), self._radius, self._radius)
        super().paintEvent(event)
