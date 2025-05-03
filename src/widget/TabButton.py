from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QSize, QRectF
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtGui import QPainterPath


class TabButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)

        # 颜色配置
        self.normal_bg = QColor(245, 245, 245, 190)
        self.hover_bg = QColor("#e0e0e0")
        self.pressed_bg = QColor("#bdbdbd")
        self.checked_bg = QColor(253, 253, 253, 190)
        self.text_color = QColor("#424242")
        self.checked_text_color = Qt.black

        # 尺寸配置
        self.radius = 15  # 顶部圆角半径
        self.padding = 15

        # 控件设置
        self.setFont(QFont("Microsoft YaHei", 12, weight=QFont.Bold))
        self.setMinimumSize(100, 55)
        self.setCheckable(True)
        self.setStyleSheet("border: none; background: transparent;")
        self.setAttribute(Qt.WA_Hover)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        # 创建顶部圆角底部直角的路径
        path = QPainterPath()
        rect = QRectF(0, 0, self.width(), self.height())

        # 顶部左圆角
        path.moveTo(rect.left(), rect.top() + self.radius)
        path.arcTo(rect.left(), rect.top(), self.radius * 2, self.radius * 2, 180, -90)

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

        # 状态判断
        is_checked = self.isChecked()
        is_hover = self.underMouse()
        is_pressed = self.isDown()

        # 背景颜色
        if is_checked:
            bg_color = self.checked_bg
        elif is_pressed:
            bg_color = self.pressed_bg
        elif is_hover:
            bg_color = self.hover_bg
        else:
            bg_color = self.normal_bg

        # 绘制背景
        painter.fillPath(path, bg_color)

        # 绘制文字
        text_color = self.checked_text_color if is_checked else self.text_color
        painter.setPen(text_color)

        # 文字区域（向下偏移2px保证视觉居中）
        text_rect = QRectF(
            self.padding, 2, self.width() - self.padding * 2, self.height()  # 向下微调
        )
        painter.drawText(text_rect, Qt.AlignCenter, self.text())

        # # 选中状态指示条（顶部）
        # if is_checked:
        #     indicator = QRectF(0, 0, self.width(), 3)
        #     painter.fillRect(indicator, self.checked_bg)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setWindowTitle("Tab Button Example")
    main_window.setGeometry(100, 100, 300, 200)

    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)

    tab_button = TabButton("Tab 1")
    layout.addWidget(tab_button)

    main_window.setCentralWidget(central_widget)
    main_window.show()

    sys.exit(app.exec_())
