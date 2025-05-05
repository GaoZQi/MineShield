import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QButtonGroup,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from QSSLoader import QSSLoader
from dataMining import DataMiningTab
from attackDetection_1 import AttackDetectionTab
from widget.RoundWidget import RoundWidget
from widget.MicaWindow import MicaWindow
from widget.TabButton import TabButton
import sys
import ctypes


class MainWindow(MicaWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据挖掘与攻击检测展示系统")
        self.setGeometry(100, 100, 920, 600)
        self.setContentsMargins(5, 5, 5, 5)  # 设置内边距

        # —— STEP 1: 创建堆栈和按钮组 ——
        self.stack = QStackedWidget()

        self.btn_group = QButtonGroup(self)  # 默认为 Exclusive
        self.btn_group.buttonClicked[int].connect(self.onTabChanged)
        self.btn_group.setExclusive(True)

        # —— STEP 2: 创建各个页面并添加进堆栈 ——
        self.data_tab = DataMiningTab()
        self.attack_tab = AttackDetectionTab()
        self.stack.addWidget(self.data_tab)  # index 0
        self.stack.addWidget(self.attack_tab)  # index 1

        # —— STEP 3: 创建按钮并加入按钮组 ——
        tab_bar = RoundWidget(radius=13, color=QColor(249, 249, 249, 200))
        tab_bar.setBorder(QColor(238, 238, 238), 0)
        tab_bar.setContentsMargins(0, 0, 0, 0)  # 新增：去除按钮容器边距
        h_layout = QHBoxLayout(tab_bar)
        h_layout.setContentsMargins(2, 2, 2, 2)

        for idx, (text, widget) in enumerate(
            [("数据挖掘", self.data_tab), ("攻击检测", self.attack_tab)]
        ):
            btn = TabButton(text)

            if idx == 0:
                btn.setChecked(True)  # 默认选中第一页
                self.setWindowTitle(self.windowTitle() + " - 数据挖掘")
            self.btn_group.addButton(btn, idx)  # ID 对应堆栈 index
            h_layout.addWidget(btn)
        # h_layout.addStretch()

        # —— STEP 4: 布局组合 ——
        central = QWidget()
        central.setContentsMargins(0, 0, 0, 0)
        v_layout = QVBoxLayout(central)
        v_layout.addWidget(tab_bar)
        v_layout.addWidget(self.stack)
        self.setCentralWidget(central)

    def onTabChanged(self, index: int):
        """按钮组发射此信号时切换堆栈页面并更新窗口标题"""
        self.stack.setCurrentIndex(index)
        title_map = {0: "数据挖掘", 1: "攻击检测"}
        self.setWindowTitle(f"数据挖掘与攻击检测展示系统 - {title_map.get(index, '')}")


if __name__ == "__main__":
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

    # —— STEP 3: 字体设置 —— #
    font = QFont("Microsoft YaHei UI", 8)
    app = QApplication(sys.argv)
    font.setHintingPreference(QFont.PreferNoHinting)
    app.setFont(font)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    window = MainWindow()
    # 加载 QSS 样式
    style_dir = "../style"
    window.setStyleSheet(QSSLoader.load_qss_files(style_dir))
    window.show()
    sys.exit(app.exec_())
