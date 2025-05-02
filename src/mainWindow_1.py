import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from QSSLoader import QSSLoader
from dataMining import DataMiningTab
from attackDetection import AttackDetectionTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据挖掘与攻击检测展示系统 - 数据挖掘")
        self.resize(900, 600)

        # 左侧导航列表
        self.list_widget = QListWidget()
        self.list_widget.setFrameShape(QListWidget.NoFrame)

        # 添加导航项
        for idx, text in enumerate(["数据挖掘", "攻击检测"]):
            item = QListWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            # item.setSizeHint(QSize(200, 50))
            # 可配置图标：
            # item.setIcon(QIcon(f"icons/{text}.png"))
            self.list_widget.addItem(item)
        self.list_widget.setCurrentRow(0)
        self.list_widget.currentRowChanged.connect(self.on_tab_changed)

        # 右侧堆栈页面
        self.stack = QStackedWidget()
        self.data_tab = DataMiningTab()
        self.attack_tab = AttackDetectionTab()
        self.stack.addWidget(self.data_tab)
        self.stack.addWidget(self.attack_tab)

        # 整体布局
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.stack)
        self.setCentralWidget(central_widget)

    def on_tab_changed(self, index: int):
        self.stack.setCurrentIndex(index)
        title_map = {0: "数据挖掘", 1: "攻击检测"}
        self.setWindowTitle(f"数据挖掘与攻击检测展示系统 - {title_map.get(index, '')}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 12))
    # 加载 QSS 样式
    window = MainWindow()
    style_dir = "../style"
    window.setStyleSheet(QSSLoader.load_qss_files(style_dir))
    window.show()
    sys.exit(app.exec_())
