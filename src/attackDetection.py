import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt


class AttackDetectionTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据挖掘与攻击检测展示系统 - 数据挖掘")
        self.resize(900, 600)

        # 左侧导航列表
        self.list_widget = QListWidget()
        self.list_widget.setFrameShape(QListWidget.NoFrame)

        # 添加导航项
        for idx, text in enumerate(
            [
                "日志检测自动化SQL注入",
                "恶意URL请求检测",
                "恶意邮件检测",
                "恶意扫描数据包检测",
                "DDoS 攻击检测",
                "IDS入侵检测",
                "MLP",
                "端口扫描攻击检测",
                "SQL注入攻击检测",
                "XSS攻击检测",
            ]
        ):
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
        self.data_tab = QWidget()
        self.attack_tab = QWidget()
        self.stack.addWidget(self.data_tab)
        self.stack.addWidget(self.attack_tab)

        # 整体布局
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

    def on_tab_changed(self, index: int):
        self.stack.setCurrentIndex(index)
        title_map = {0: "数据挖掘", 1: "攻击检测"}


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setWindowTitle("Data Mining and Attack Detection System")
    main_window.setGeometry(100, 100, 900, 600)

    data_tab = AttackDetectionTab()
    main_window.setCentralWidget(data_tab)

    main_window.show()
    sys.exit(app.exec_())
