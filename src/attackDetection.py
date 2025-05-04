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
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTextEdit, QFileDialog, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QProcess
from widget.RoundWidget import RoundWidget

class AttackDetectionTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据挖掘与攻击检测展示系统 - 攻击检测")
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
            self.list_widget.addItem(item)
        self.list_widget.setCurrentRow(0)
        self.list_widget.currentRowChanged.connect(self.on_tab_changed)

        # 右侧堆栈页面
        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_attack_module("XGBoost.py"))
        self.stack.addWidget(self.create_attack_module("Logistics-Regression.py"))
        self.stack.addWidget(self.create_attack_module("SVM.py"))
        self.stack.addWidget(self.create_attack_module("KNN.py"))
        self.stack.addWidget(self.create_attack_module("DDOS.py"))
        self.stack.addWidget(self.create_attack_module("One_Class_SVM.py"))
        self.stack.addWidget(self.create_attack_module("Isolation-forest.py"))

        # 整体布局
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.list_widget)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

    def create_attack_module(self, script_name):
        """为每个模块创建输入框、按钮和结果显示区域"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

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
        start_button.clicked.connect(lambda: self.start_detection(script_name, log_path_input.text()))
        layout.addWidget(start_button)

        # 使用 RoundWidget 优化回显框
        result_display_widget = RoundWidget(radius=10, color=QColor(255, 255, 255))  # 设置圆角和背景色
        result_layout = QVBoxLayout(result_display_widget)

        # 显示结果的文本框
        result_display = QTextEdit()
        result_display.setReadOnly(True)
        layout.addWidget(result_display)

        widget.result_display = result_display
        widget.log_path_input = log_path_input
        return widget

    def browse_file(self, log_path_input):
        """打开文件对话框选择日志文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择要上传的文件", "", "文件 (*)")
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
        python_executable = 'C:\\Users\\GAiLO\\anaconda3\\envs\\python-310\\python.exe'

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
