import sys
import os

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
)
from PyQt5.QtCore import Qt
from widget.RoundWidget import RoundWidget
from widget.FluentListWidget import FluentListWidget
from pages.CLImode import ExampleTab


class AttackDetectionTab(RoundWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据挖掘与攻击检测展示系统 - 攻击检测")
        self.setBackgroundColor(QColor(250, 250, 250, 200))
        self.setRadius(10)
        self.setBorder(QColor(238, 238, 238), 2)
        self.setContentsMargins(10, 10, 10, 10)

        # 左侧导航列表
        self.list_widget = FluentListWidget()
        self.list_widget.setContentsMargins(0, 0, 0, 0)
        self.list_widget.setFrameShape(FluentListWidget.NoFrame)

        # 右侧堆栈页面
        self.stack = QStackedWidget()

        # 导航项文本列表
        items = [
            "日志检测自动化SQL注入",
            "恶意URL请求检测",
            "恶意邮件检测",
            "恶意扫描数据包检测",
            "DDoS 攻击检测",
            "IDS入侵检测",
            "恶意数据包检测",
            "端口扫描攻击检测",
            "SQL注入攻击检测",
            "XSS攻击检测",
        ]

        # 添加导航项及对应页面
        for text in items:
            item = QListWidgetItem(text)
            # item.setTextAlignment(Qt.AlignCenter)
            self.list_widget.addItem(item)
            # 每个导航项对应一个实例页面
            self.stack.addWidget(ExampleTab(text))

        # 默认选中第一个
        self.list_widget.setCurrentRow(0)

        # 连接信号：列表行变化切换堆栈页面
        self.list_widget.currentRowChanged.connect(self.stack.setCurrentIndex)

        # 整体布局
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)


if __name__ == "__main__":
    from QSSLoader import QSSLoader
    from PyQt5.QtGui import QFont

    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 12))
    app.setStyleSheet(QSSLoader.load_qss_files("../style"))
    main_window = QMainWindow()
    main_window.setWindowTitle("Data Mining and Attack Detection System")
    main_window.setGeometry(100, 100, 1650, 1000)

    data_tab = AttackDetectionTab()
    main_window.setCentralWidget(data_tab)

    main_window.show()
    sys.exit(app.exec_())
