from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPainterPath
from PyQt5.QtCore import Qt, QRectF


class RoundWidget(QWidget):
    """
    A QWidget with customizable rounded corners and background color,
    without affecting child widget properties.

    Usage:
        widget = RoundWidget(radius=15, color=QColor(100, 150, 200))
    """

    def __init__(self, radius=10, color=QColor(255, 255, 255), flag=1, parent=None):
        super().__init__(parent)
        self._radius = radius
        self._bg_color = color
        self.flag = flag  # 1: 圆角矩形，2: 顶部圆角底部直角

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
        if self.flag == 1:
            painter.drawRoundedRect(self.rect(), self._radius, self._radius)
        else:
            # 创建顶部圆角底部直角的路径
            path = QPainterPath()
            rect = QRectF(0, 0, self.width(), self.height())

            # 顶部左圆角
            path.moveTo(rect.left(), rect.top() + self.radius)
            path.arcTo(
                rect.left(), rect.top(), self.radius * 2, self.radius * 2, 180, -90
            )

            # 顶部右圆角
            path.lineTo(rect.right() - self.radius, rect.top())
            path.arcTo(
                rect.right() - self.radius * 2,
                rect.top(),
                self.radius * 2,
                self.radius * 2,
                90,
                -90,
            )

            # 底部直角
            path.lineTo(rect.right(), rect.bottom())
            path.lineTo(rect.left(), rect.bottom())
            path.closeSubpath()
            painter.fillPath(path, self._bg_color)

        super().paintEvent(event)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = RoundWidget(radius=20, color=QColor(100, 150, 200))
    widget.resize(300, 200)
    widget.show()
    sys.exit(app.exec_())
