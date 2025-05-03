from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
)
from PyQt5.QtCore import Qt
from QSSLoader import QSSLoader
from PyQt5.QtGui import QFont, QColor, QPainter, QPen


class PopupDialog(QDialog):
    def __init__(self, parent=None, items=None, title="选择项", choose=None):

        super().__init__(parent)
        # 隐藏标题栏
        # 初始化返回值
        self.selected_algorithm = choose
        self.setContentsMargins(10, 10, 10, 10)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置弹窗固定大小
        self.setFixedWidth(600)
        # 主布局
        layout = QVBoxLayout(self)
        # layout.setContentsMargins(20, 20, 20, 20)
        # layout.setSpacing(15)

        # 弹窗内容标签
        label = QLabel("数据挖掘算法", self)
        label.setObjectName("P1")
        layout.addWidget(label)

        # 下拉列表
        self.combex = QComboBox(self)
        if items:
            self.combex.addItems(items)
        layout.addWidget(self.combex)
        # 按钮布局
        btn_layout = QHBoxLayout()
        # btn_layout.addStretch()

        # 取消按钮
        cancel_btn = QPushButton("取消", self)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        # 确定按钮
        ok_btn = QPushButton("确定", self)
        ok_btn.setObjectName("OKButton")
        ok_btn.clicked.connect(self.on_ok)
        btn_layout.addWidget(ok_btn)
        btn_layout.setSpacing(10)

        # btn_layout.addStretch()
        layout.addLayout(btn_layout)
        layout.setSpacing(50)
        layout.setAlignment(Qt.AlignTop)  # 设置对齐方式为顶部对齐

    def on_ok(self):
        # 保存选择并关闭
        self.selected_algorithm = self.combex.currentText()
        print("Selected algorithm:", self.selected_algorithm)
        super().accept()

    def paintEvent(self, event):
        # 绘制圆角背景和边框
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # 填充背景
        background_color = QColor(255, 255, 255)
        painter.setBrush(background_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 15, 15)

        # 绘制边框
        border_color = QColor(200, 200, 200)
        pen = QPen(border_color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        inner_rect = rect.adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(inner_rect, 15, 15)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setStyleSheet(QSSLoader.load_qss_files("../style"))
    app.setFont(QFont("Microsoft YaHei UI", 12))
    dialog = PopupDialog()
    dialog.show()
    sys.exit(app.exec_())
