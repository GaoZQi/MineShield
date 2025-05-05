from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QPixmap, QIcon, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QSize, QByteArray
from PyQt5.QtSvg import QSvgRenderer


class IconButton(QPushButton):
    def __init__(self, svg_data: str, tooltip: str = "", parent=None):
        super().__init__(parent)
        # 基础样式配置
        # self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)

        # 颜色配置
        self.background_color = QColor("#f9f9f9")
        self.border_color = QColor("#d1d1d1")
        self.hover_color = QColor("#e0e0e0")
        self.pressed_color = QColor("#c0c0c0")
        self.border_width = 2  # 可自由调整的边框宽度
        self.radius = 5  # 圆角半径

        # 控件设置
        self.setFlat(True)
        self.setStyleSheet("border: none; background: transparent;")
        self.setAttribute(Qt.WA_Hover)  # 必须启用悬停检测
        self.setIconSize(QSize(12, 12))

        # 加载SVG图标
        self.svg_icon = self.load_svg_icon(svg_data)
        self.setIcon(self.svg_icon)

    def load_svg_icon(self, svg_data: str) -> QIcon:
        """从SVG字符串加载图标"""
        renderer = QSvgRenderer(QByteArray(svg_data.encode("utf-8")))
        pixmap = QPixmap(self.iconSize())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    def sizeHint(self) -> QSize:
        """建议按钮尺寸"""
        return QSize(24, 24)

    def paintEvent(self, event):
        """自定义绘制实现"""
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # ===== 1. 计算绘制区域 =====
        border_offset = self.border_width / 2
        main_rect = QRectF(
            border_offset,
            border_offset,
            self.width() - self.border_width,
            self.height() - self.border_width,
        )
        path = QPainterPath()
        path.addRoundedRect(main_rect, self.radius, self.radius)

        # ===== 2. 确定状态颜色 =====
        if self.isDown():
            bg_color = self.pressed_color
        elif self.underMouse():
            bg_color = self.hover_color
        else:
            bg_color = self.background_color

        # ===== 3. 绘制背景 =====
        painter.fillPath(path, bg_color)

        # ===== 4. 绘制边框 =====
        if self.border_width > 0:
            border_pen = QPen(
                self.border_color,
                self.border_width,
                Qt.SolidLine,
                Qt.RoundCap,  # 圆形端点
                Qt.RoundJoin,  # 圆形连接
            )
            painter.strokePath(path, border_pen)

        # ===== 5. 绘制图标 =====
        icon_size = self.iconSize()
        icon_rect = QRectF(
            (self.width() - icon_size.width()) / 2,
            (self.height() - icon_size.height()) / 2,
            icon_size.width(),
            icon_size.height(),
        )
        self.icon().paint(painter, icon_rect.toRect(), Qt.AlignCenter)


if __name__ == "__main__":
    import sys

    # 示例SVG数据（左右箭头图标）
    demo_svg = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
    <path d="M7.72 21.78a.75.75 0 0 0 1.06-1.06L5.56 17.5h14.69a.75.75 0 0 0 0-1.5H5.56l3.22-3.22a.75.75 0 1 0-1.06-1.06l-4.5 4.5a.75.75 0 0 0 0 1.06l4.5 4.5Zm8.56-9.5a.75.75 0 1 1-1.06-1.06L18.44 8H3.75a.75.75 0 0 1 0-1.5h14.69l-3.22-3.22a.75.75 0 0 1 1.06-1.06l4.5 4.5a.75.75 0 0 1 0 1.06l-4.5 4.5Z"></path>
    </svg>
    """

    # 创建演示窗口
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("高级圆角按钮演示")
    window.setGeometry(300, 300, 400, 300)
    layout = QVBoxLayout(window)

    # 创建按钮实例
    button = IconButton(demo_svg, "双向切换按钮")
    layout.addWidget(button)
    layout.setAlignment(Qt.AlignCenter)

    # 显示窗口
    window.show()
    sys.exit(app.exec_())
