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
    QDialog,
    QLineEdit,
    QFileDialog,
    QTableWidgetItem,
    QTableWidget,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from widget.RoundWidget import RoundWidget
from QSSLoader import QSSLoader
from widget.IconButton import IconButton
from alorgorithmDialog import alorgorithmDialog as PopupDialog
from algorithms import *


class DataMiningTab(RoundWidget):
    def __init__(self):
        super().__init__()
        self.setBackgroundColor(QColor(253, 253, 253, 190))
        self.setContentsMargins(36, 0, 36, 36)  # 设置内边距
        self.algorithms = {
            "Dimensionality Reduction": DimensionalityReduction,
            "Linear Regression": LinearRegression,
            "K-Means": Kemeans,
            "Random-Forest": RandomForest,
            "Isolation Forest": IsolationForest,
            "Apriori": Apriori,
            "PCA": PCA,
            "GMM": GMM,
            "Agglomerative Clustering": AgglomerativeClustering,
            "Bayes": Bayes,
            "Decision Tree": DecisionTree,
        }
        self.dataURL = None
        self.choose = list(self.algorithms.keys())[0]
        main_layout = QHBoxLayout()
        alorgorithm_layout = QHBoxLayout()
        alorgorithm_layout.setContentsMargins(0, 0, 0, 0)
        data_layout = QHBoxLayout()
        self.Data_tab = QWidget()
        # Dropdown for algorithm selection
        self.tip = "算法："
        self.algorithm_label = QLabel(self.tip + self.choose)
        self.algorithm_label.setObjectName("H1")
        self.algorithm_label.setMinimumWidth(720)
        svg_data = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
        <path d="M7.72 21.78a.75.75 0 0 0 1.06-1.06L5.56 17.5h14.69a.75.75 0 0 0 0-1.5H5.56l3.22-3.22a.75.75 0 1 0-1.06-1.06l-4.5 4.5a.75.75 0 0 0 0 1.06l4.5 4.5Zm8.56-9.5a.75.75 0 1 1-1.06-1.06L18.44 8H3.75a.75.75 0 0 1 0-1.5h14.69l-3.22-3.22a.75.75 0 0 1 1.06-1.06l4.5 4.5a.75.75 0 0 1 0 1.06l-4.5 4.5Z"></path>
        </svg>
        """
        algorithm_button = IconButton(
            svg_data,
            "算法选择",
        )
        algorithm_button.clicked.connect(self.show_popup)
        alorgorithm_layout.addWidget(self.algorithm_label)
        alorgorithm_layout.addSpacing(10)
        alorgorithm_layout.addWidget(algorithm_button)
        alorgorithm_layout.setAlignment(Qt.AlignLeft)
        # main_layout.addLayout(alorgorithm_layout)

        data_tip = QLabel("数据集")
        data_tip.setObjectName("H2")
        # main_layout.addWidget(data_tip)

        data_URL_layout = QHBoxLayout()
        self.dataURLText = QLineEdit()
        self.dataURLText.setPlaceholderText("数据集路径")
        self.dataURLText.setReadOnly(True)
        data_URL_layout.addWidget(self.dataURLText)
        choose_button = QPushButton("选择数据集")
        choose_button.setObjectName("chooseButton")
        choose_button.clicked.connect(self.choose_file)
        data_URL_layout.addWidget(choose_button)
        data_layout.addLayout(data_URL_layout)

        # Table for displaying data
        self.table = QTableWidget()

        # Run button
        self.run_button = QPushButton("运行")
        self.run_button.setObjectName("OKButton")
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.run_algorithm)

        # Matplotlib canvas for visualization
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        config_layout = QVBoxLayout()
        config_layout.addLayout(alorgorithm_layout)
        config_layout.addWidget(data_tip)
        config_layout.addLayout(data_layout)
        config_layout.addWidget(self.table)
        config_layout.addWidget(self.run_button)
        config_layout.setAlignment(Qt.AlignTop)
        # Combine layouts
        pic_tip = QLabel("处理结果")
        pic_tip.setObjectName("H1")
        pic_layout = QVBoxLayout()
        pic_layout.addWidget(pic_tip)
        pic_layout.addWidget(self.canvas, stretch=3)
        main_layout.addLayout(config_layout, 2)  # 左边3份
        main_layout.addSpacing(20)  # 左右间距
        main_layout.addLayout(pic_layout, 2)  # 右边2份
        main_layout.setStretch(0, 1)  # 第一个子布局（左边）权重3
        main_layout.setStretch(1, 2)  # 第二个子布局（右边）权重2
        self.setLayout(main_layout)

    def run_algorithm(self):
        # 获取当前选择的算法
        selected_algorithm = self.algorithm_label.text().replace(self.tip, "")
        if selected_algorithm not in self.algorithms:
            return
        # 获取算法函数
        algorithm_func = self.algorithms[selected_algorithm]
        # 运行算法并获取结果
        self.figure.clf()
        self.ax = self.figure.add_subplot(111)

        algorithm_func(self.dataURL, self.ax, self.canvas)
        # x = np.random.rand(100)
        # y = np.random.rand(100)
        # self.ax.scatter(x, y, c="blue", alpha=0.5)
        # self.canvas.draw()

    def show_popup(self):
        dialog = PopupDialog(
            self, items=self.algorithms, title="数据挖掘算法", choose=self.choose
        )
        if dialog.exec_() == QDialog.Accepted:
            selected = dialog.selected_algorithm
            # 更新标签或下拉框
            print("Selected algorithm:", selected)
            self.algorithm_label.setText(self.tip + selected)

    def choose_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择数据集", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_name:
            self.dataURLText.setText(file_name)
            self.dataURL = file_name
            self.run_button.setEnabled(True)
            self.load_csv_data()  # ← 加载数据
        else:
            self.dataURLText.clear()
            self.dataURL = None
            self.run_button.setEnabled(False)
            self.table.clear()

    def load_csv_data(self):
        if not self.dataURL:
            return
        import csv

        with open(self.dataURL, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        if not rows:
            self.table.clear()
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        row_count = len(rows)
        col_count = max(len(row) for row in rows)

        self.table.clear()
        self.table.setRowCount(row_count)
        self.table.setColumnCount(col_count)
        # （可选）将第一行作为水平表头
        self.table.setHorizontalHeaderLabels(rows[0])
        data_rows = rows[1:]
        for i, row in enumerate(data_rows):
            for j, cell in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(cell))

        # 如果不需要特殊表头，就全部按数据填入：
        # 隐藏水平表头（列名）
        self.table.horizontalHeader().setVisible(False)
        # 隐藏垂直表头（行号）
        self.table.verticalHeader().setVisible(False)

        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(cell))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    app.setFont(QFont("Microsoft YaHei UI", 12))
    app.setStyleSheet(QSSLoader.load_qss_files("../style"))
    main_window.setWindowTitle("Data Mining and Attack Detection System")
    main_window.setGeometry(100, 100, 1650, 1000)

    data_tab = DataMiningTab()
    main_window.setCentralWidget(data_tab)

    main_window.show()
    sys.exit(app.exec_())
