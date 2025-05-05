from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPainter, QPen
import sys

from mod.QSSLoader import QSSLoader
from widget.RoundComboBox import RoundComboBox


class alorgorithmDialog(QDialog):
    def __init__(self, parent=None, items=None, title="选择项", choose=None):

        super().__init__(parent)
        # 隐藏标题栏
        # 初始化返回值
        self.selected_algorithm = choose
        self.setContentsMargins(5, 5, 5, 5)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置弹窗固定大小
        self.setFixedWidth(300)
        # 主布局
        layout = QVBoxLayout(self)
        # layout.setContentsMargins(20, 20, 20, 20)
        # layout.setSpacing(15)

        # 弹窗内容标签
        label = QLabel("设置数据挖掘算法", self)
        label.setObjectName("P1")
        layout.addWidget(label)

        tip = QLabel("算法：", self)
        tip.setObjectName("P2")
        layout.addWidget(tip)

        # 下拉列表
        self.combex = RoundComboBox(self)
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
        btn_layout.setSpacing(5)

        # btn_layout.addStretch()
        layout.addSpacing(15)  # 添加间距
        layout.addLayout(btn_layout)
        layout.setSpacing(10)
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
        painter.drawRoundedRect(rect, 10, 10)

        # 绘制边框
        border_color = QColor(200, 200, 200)
        pen = QPen(border_color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        inner_rect = rect.adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(inner_rect, 10, 10)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    import ctypes

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # —— STEP 0: 系统 DPI 感知 —— #
    # Windows 8.1+
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        ctypes.windll.user32.SetProcessDPIAware()

    # —— STEP 1: Qt 高 DPI 支持 —— #
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyleSheet(QSSLoader.load_qss_files("../../style"))
    app.setFont(QFont("Microsoft YaHei UI", 12))
    dialog = alorgorithmDialog()

    algorithms = {
        "Dimensionality Reduction": "DimensionalityReduction",
        "Linear Regression": "LinearRegression",
        "K-Means": "Kemeans",
        "Random-Forest": "RandomForest",
        "Isolation Forest": "IsolationForest",
        "Apriori": "Apriori",
        "PCA": "PCA",
        "GMM": "GMM",
        "Agglomerative Clustering": "AgglomerativeClustering",
        "Bayes": "Bayes",
        "Decision Tree": "DecisionTree",
    }
    items = list(algorithms.keys())
    dialog.combex.addItems(items)
    dialog.setWindowTitle("选择算法")
    dialog.setWindowModality(Qt.ApplicationModal)  # 设置为模态窗口
    dialog.setAttribute(Qt.WA_DeleteOnClose)  # 关闭时删除窗口
    dialog.show()
    sys.exit(app.exec_())
