import sys
import os

from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
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


class CLITab(RoundWidget):
    def __init__(self, tab_name="Example", algorithm_name="Example", script=""):
        super().__init__()
        self.setWindowTitle("数据挖掘与攻击检测展示系统 - 攻击检测")
        self.setBackgroundColor(QColor(250, 250, 250, 200))
        self.setRadius(10)
        self.setBorder(QColor(238, 238, 238), 2)
        self.setContentsMargins(5, 5, 5, 5)

        layout = QVBoxLayout()

        title_label = QLabel(tab_name)
        title_label.setObjectName("H1")
        layout.addWidget(title_label)

        tip_label = QLabel("核心算法：" + algorithm_name)
        tip_label.setObjectName("H2")
        layout.addWidget(tip_label)
        file_layout = QHBoxLayout()
        # 输入框：日志文件路径
        log_path_input = QLineEdit()
        log_path_input.setPlaceholderText("请输入待检测文件路径")
        file_layout.addWidget(log_path_input)

        # 浏览按钮
        browse_button = QPushButton("选择文件")
        browse_button.clicked.connect(lambda: self.browse_file(log_path_input))
        file_layout.addWidget(browse_button)
        layout.addLayout(file_layout)
        # 开始检测按钮（初始禁用）
        start_button = QPushButton("开始检测")
        start_button.setObjectName("OKButton")
        start_button.setEnabled(False)
        start_button.clicked.connect(
            lambda: self.start_detection(script, log_path_input.text())
        )
        layout.addWidget(start_button)

        # 显示结果的文本框
        result_display = QTextEdit()
        result_display.setReadOnly(True)
        layout.addWidget(result_display)

        self.result_display = result_display
        self.log_path_input = log_path_input
        self.start_button = start_button

        # 输入框文本变化时检查启用状态
        log_path_input.textChanged.connect(self.check_start_button)

        self.setLayout(layout)

    def check_start_button(self):
        """检查是否启用开始检测按钮"""
        if self.log_path_input.text():
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def browse_file(self, log_path_input):
        """打开文件对话框选择日志文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择要上传的文件", "", "文件 (*)"
        )
        if file_path:
            log_path_input.setText(file_path)
            self.result_display.clear()  # 清空日志

    def start_detection(self, script, log_file_path):
        if not log_file_path:
            return

        self.result_display.clear()

        process = QProcess(self)
        process.readyReadStandardOutput.connect(lambda: self.handle_stdout(process))
        process.readyReadStandardError.connect(lambda: self.handle_stderr(process))

        python_executable = sys.executable
        if not python_executable:
            self.result_display.append("Python解释器未找到")
            return

        abs_script = os.path.abspath(script)
        self.result_display.append(f"启动脚本: {abs_script}")

        process.start(python_executable, [abs_script])

        process.waitForStarted()
        process.write(log_file_path.encode() + b"\n")

    def handle_stdout(self, process):
        data = process.readAllStandardOutput().data()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("gbk", errors="replace")
        self.result_display.append(text)

    def handle_stderr(self, process):
        error_data = process.readAllStandardError().data()
        try:
            text = error_data.decode("utf-8")
        except UnicodeDecodeError:
            text = error_data.decode("gbk", errors="replace")
        self.result_display.append(f"错误信息：\n{text}")


if __name__ == "__main__":
    from QSSLoader import QSSLoader

    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 12))
    app.setStyleSheet(QSSLoader.load_qss_files("../../style"))
    main_window = QMainWindow()
    main_window.setWindowTitle("Data Mining and Attack Detection System")
    main_window.setGeometry(100, 100, 1650, 1000)

    data_tab = CLITab()
    main_window.setCentralWidget(data_tab)

    main_window.show()
    sys.exit(app.exec_())
