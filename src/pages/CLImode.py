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
from PyQt5.QtWidgets import (
    QLineEdit,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PyQt5.QtCore import QProcess

sys.path.append("..")
from widget.RoundWidget import RoundWidget
from widget.FluentListWidget import FluentListWidget


class ExampleTab(RoundWidget):

    def __init__(self, tab_name="Example"):
        super().__init__()
        self.setWindowTitle("数据挖掘与攻击检测展示系统 - 攻击检测")
        self.setBackgroundColor(QColor(250, 250, 250, 200))
        self.setRadius(20)
        self.setBorder(QColor(238, 238, 238), 2)
        self.setContentsMargins(0, 0, 0, 0)
        """为每个模块创建输入框、按钮和结果显示区域"""
        layout = QVBoxLayout()

        title_label = QLabel(tab_name)
        title_label.setObjectName("H1")
        layout.addWidget(title_label)

        # 输入框：日志文件路径
        log_path_input = QLineEdit()
        log_path_input.setPlaceholderText("请输入待检测文件路径")
        layout.addWidget(log_path_input)

        # 浏览按钮
        browse_button = QPushButton("浏览...")
        # browse_button.clicked.connect(lambda: self.browse_file(log_path_input))
        layout.addWidget(browse_button)

        # 开始检测按钮
        start_button = QPushButton("开始检测")
        # start_button.clicked.connect()
        layout.addWidget(start_button)

        # 使用 RoundWidget 优化回显框
        result_display_widget = RoundWidget(
            radius=10, color=QColor(255, 255, 255)
        )  # 设置圆角和背景色
        result_layout = QVBoxLayout(result_display_widget)

        # 显示结果的文本框
        result_display = QTextEdit()
        result_display.setReadOnly(True)
        layout.addWidget(result_display)

        self.result_display = result_display
        self.log_path_input = log_path_input

        self.setLayout(layout)


if __name__ == "__main__":
    from QSSLoader import QSSLoader
    from PyQt5.QtGui import QFont

    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 12))
    app.setStyleSheet(QSSLoader.load_qss_files("../../style"))
    main_window = QMainWindow()
    main_window.setWindowTitle("Data Mining and Attack Detection System")
    main_window.setGeometry(100, 100, 1650, 1000)

    data_tab = ExampleTab()
    main_window.setCentralWidget(data_tab)

    main_window.show()
    sys.exit(app.exec_())
