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
from pages.CLImode import CLITab


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
            {
                "title": "日志检测自动化SQL注入",
                "func_name": "XGBoost",
                "script": "./algorithms/attackDetection/XGBoost.py",
                "widget": CLITab,
            },
            {
                "title": "恶意URL请求检测",
                "func_name": "Logistics Regression",
                "script": "./algorithms/attackDetection/Logistics-Regression.py",
                "widget": CLITab,
            },
            {
                "title": "恶意邮件检测",
                "func_name": "SVM",
                "script": "./algorithms/attackDetection/SVM-Email.py",
                "widget": CLITab,
            },
            {
                "title": "恶意扫描数据包检测",
                "func_name": "KNN",
                "script": "./algorithms/attackDetection/KNN.py",
                "widget": CLITab,
            },
            {
                "title": "DDoS 攻击检测",
                "func_name": "梯度提升树",
                "script": "./algorithms/attackDetection/DDoS.py",
                "widget": CLITab,
            },
            {
                "title": "IDS入侵检测",
                "func_name": "One-Class SVM",
                "script": "./algorithms/attackDetection/One_Class_SVM.py",
                "widget": CLITab,
            },
            {
                "title": "恶意数据包检测",
                "func_name": "MLP",
                "script": "./algorithms/attackDetection/MLP.py",
                "widget": CLITab,
            },
            {
                "title": "端口扫描攻击检测",
                "func_name": "Isolation Forest",
                "script": "./algorithms/attackDetection/Isolation_Forest.py",
                "widget": CLITab,
            },
            {
                "title": "SQL注入攻击检测",
                "func_name": "SVM",
                "script": "./algorithms/attackDetection/.py",
                "widget": CLITab,
            },
            {
                "title": "XSS攻击检测",
                "func_name": "LSTM",
                "script": "./algorithms/attackDetection/.py",
                "widget": CLITab,
            },
        ]

        # 添加导航项及对应页面
        for item in items:
            tab = QListWidgetItem(item["title"])
            # item.setTextAlignment(Qt.AlignCenter)
            self.list_widget.addItem(tab)
            # 每个导航项对应一个实例页面
            self.stack.addWidget(
                item["widget"](item["title"], item["func_name"], item["script"])
            )

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
