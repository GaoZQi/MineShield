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

    def __init__(self, tab_name="Example", func_name="Example", script_url=""):
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

        tip_label = QLabel(func_name)
        tip_label.setObjectName("H2")
        layout.addWidget(title_label)

        # 输入框：日志文件路径
        log_path_input = QLineEdit()
        log_path_input.setPlaceholderText("请输入待检测文件路径")
        layout.addWidget(log_path_input)

        # 浏览按钮
        browse_button = QPushButton("浏览...")
        browse_button.clicked.connect(lambda: self.browse_file(log_path_input))
        layout.addWidget(browse_button)

        # 开始检测按钮
        start_button = QPushButton("开始检测")
        start_button.clicked.connect(
            lambda: self.start_detection(script_url, log_path_input.text())
        )
        layout.addWidget(start_button)

        # 显示结果的文本框
        result_display = QTextEdit()
        result_display.setReadOnly(True)
        layout.addWidget(result_display)

        self.result_display = result_display
        self.log_path_input = log_path_input

        self.setLayout(layout)

    def browse_file(self, log_path_input):
        """打开文件对话框选择日志文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择要上传的文件", "", "文件 (*)"
        )
        if file_path:
            log_path_input.setText(file_path)

    def start_detection(self, script_name, log_file_path):
        """启动后端 Python 文件进行检测"""
        if not log_file_path:
            return

        current_widget = self.stack.currentWidget()

        current_widget.result_display.clear()

        # 获取 XGBoost.py 文件所在的路径
        script_dir = os.path.dirname(os.path.abspath(f"algorithms/{script_name}"))

        # 启动后端 Python 文件进行检测
        process = QProcess(self)
        process.readyReadStandardOutput.connect(lambda: self.handle_stdout(process))
        process.readyReadStandardError.connect(lambda: self.handle_stderr(process))

        # 设置工作目录为 XGBoost.py 所在的目录
        process.setWorkingDirectory(script_dir)

        # 使用conda环境中的Python解释器
        python_executable = "C:\\Users\\GAiLO\\anaconda3\\envs\\python-310\\python.exe"

        # 启动后端 Python 脚本
        command = [python_executable, script_name]
        process.start(command[0], command[1:])

        # 等待进程启动并模拟输入路径
        process.waitForStarted()

        # 模拟输入日志文件路径
        process.write(log_file_path.encode() + b"\n")  # 模拟按下回车键

    def handle_stdout(self, process):
        """捕获并显示标准输出"""
        data = process.readAllStandardOutput().data().decode()
        current_widget = self.stack.currentWidget()
        current_widget.result_display.append(data)

    def handle_stderr(self, process):
        """捕获并显示标准错误输出"""
        error_data = process.readAllStandardError().data().decode()
        current_widget = self.stack.currentWidget()
        current_widget.result_display.append(f"错误信息：\n{error_data}")


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
