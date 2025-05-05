from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate
from PyQt5.QtCore import QRect, Qt, QByteArray
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPixmap
from PyQt5.QtWidgets import QStyle
from PyQt5.QtSvg import QSvgRenderer


class ComboBoxItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(30)  # 增加高度留出阴影空间
        return size

    def paint(self, painter, option, index):
        painter.setRenderHint(QPainter.Antialiasing)

        # 原始项尺寸
        original_rect = option.rect

        # 绘制背景
        bg_color = (
            QColor("#f0f0f0")
            if option.state & QStyle.State_Selected
            else QColor("#fdfdfd")
        )
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(original_rect, 10, 10)

        # 绘制文本
        text_rect = original_rect.adjusted(12, 0, -7, 0)
        painter.setPen(QColor("#1a1a1a"))
        painter.drawText(
            text_rect, Qt.AlignLeft | Qt.AlignVCenter, index.data(Qt.DisplayRole)
        )


class RoundComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.setItemDelegate(ComboBoxItemDelegate(self))
        # 初始化SVG渲染器
        self.svg_data = QByteArray(
            b"""
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                <path d="M5.22 8.22a.749.749 0 0 0 0 1.06l6.25 6.25a.749.749 0 0 0 1.06 0l6.25-6.25a.749.749 0 1 0-1.06-1.06L12 13.939 6.28 8.22a.749.749 0 0 0-1.06 0Z"/>
            </svg>
        """
        )
        self.renderer = QSvgRenderer(self.svg_data)

    def setup_styles(self):
        self.setFixedHeight(30)
        self.setStyleSheet(
            """
            QComboBox {
                padding-left: 15px;
                color: #1a1a1a;
                background-color: #fdfdfd;
            }
            QComboBox::drop-down { 
                width: 40px;
                border: none; 
            }
            /* 下拉列表样式 */
            QComboBox QAbstractItemView {
                background-color: transparent;
                border: 2px solid #f1f1f1;
                border-radius: 10px;
                outline: none;
            }
            /* 滚动条样式 */
            QScrollBar:vertical {
                background: transparent;
                width: 5px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #cccccc;
                border-radius: 5px;
                min-height: 15px;
            }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
            QScrollBar::add-page:vertical, 
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        bg_rect = self.rect().adjusted(1, 1, -1, -1)
        painter.setBrush(QBrush(QColor("#fdfdfd")))
        painter.setPen(QPen(QColor("#f1f1f1"), 2))
        painter.drawRoundedRect(bg_rect, 10, 10)

        # 绘制当前选中项文本
        text_rect = QRect(15, 0, self.width() - 35, self.height())
        painter.setPen(QColor("#1a1a1a"))
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self.currentText())

        # 绘制自定义SVG箭头
        arrow_size = 12
        arrow_rect = QRect(
            self.width() - 22,
            (self.height() - arrow_size) // 2,
            arrow_size,
            arrow_size,
        )
        arrow_pixmap = QPixmap(arrow_size, arrow_size)
        arrow_pixmap.fill(Qt.transparent)

        pix_painter = QPainter(arrow_pixmap)
        self.renderer.render(pix_painter)
        pix_painter.end()

        # 应用颜色滤镜
        arrow_pixmap = self.recolor_pixmap(arrow_pixmap, QColor("#1a1a1a"))
        painter.drawPixmap(arrow_rect, arrow_pixmap)

    def recolor_pixmap(self, pixmap, color):
        """修改SVG颜色"""
        image = pixmap.toImage()
        for x in range(image.width()):
            for y in range(image.height()):
                if image.pixelColor(x, y).alpha() > 0:
                    image.setPixelColor(x, y, color)
        return QPixmap.fromImage(image)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    combo = RoundComboBox()
    combo.addItems([f"Option {i}" for i in range(1, 20)])  # 添加更多项测试滚动条
    combo.show()
    sys.exit(app.exec_())
