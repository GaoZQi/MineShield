import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTextEdit,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from QSSLoader import QSSLoader
from dataMining import DataMiningTab
from attackDetection import AttackDetectionTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("数据挖掘与攻击检测展示系统")
        self.setGeometry(100, 100, 900, 600)

        self.data_tab = DataMiningTab()
        self.attack_tab = AttackDetectionTab()
        self.selected_tab = self.data_tab

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QVBoxLayout()
        tab_layout = QHBoxLayout()

        self.data_tab_button = QPushButton("数据挖掘")
        self.aAttack_tab_button = QPushButton("攻击检测")

        self.data_tab_button.clicked.connect(self.change_Datatab)
        self.aAttack_tab_button.clicked.connect(self.change_Attacktab)

        tab_layout.addWidget(self.data_tab_button)
        tab_layout.addWidget(self.aAttack_tab_button)

        self.main_layout.addLayout(tab_layout)
        self.main_layout.addWidget(self.data_tab)
        self.main_layout.addWidget(self.attack_tab)
        self.attack_tab.hide()

        self.central_widget.setLayout(self.main_layout)

    def change_Datatab(self):
        self.selected_tab.hide()
        self.data_tab.show()
        self.selected_tab = self.data_tab
        self.setWindowTitle("数据挖掘与攻击检测展示系统 - 数据挖掘")

    def change_Attacktab(self):
        self.selected_tab.hide()
        self.attack_tab.show()
        self.selected_tab = self.attack_tab
        self.setWindowTitle("数据挖掘与攻击检测展示系统 - 攻击检测")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Microsoft YaHei UI", 12)
    app.setFont(font)
    window = MainWindow()
    style_file = "../style/main.qss"
    style_sheet = QSSLoader.read_qss_file(style_file)
    window.setStyleSheet(style_sheet)
    window.show()
    sys.exit(app.exec_())
