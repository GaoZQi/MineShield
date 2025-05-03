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
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from widget.RoundWidget import RoundWidget
from QSSLoader import QSSLoader
from widget.IconButton import IconButton


class DataMiningTab(RoundWidget):
    def __init__(self):
        super().__init__()
        self.setBackgroundColor(QColor("#f9f9f9"))
        self.setContentsMargins(36, 36, 36, 36)  # 设置内边距
        self.algorithms = [
            "KMeans",
            "DBSCAN",
            "Hierarchical Clustering",
            "PCA",
            "LDA",
            "Logistic Regression",
            "Random Forest",
            "SVM",
            "Decision Tree",
            "Naive Bayes",
            "Gradient Boosting",
            "XGBoost",
            "LightGBM",
            "Isolation Forest",
            "Autoencoder",
            "One-Class SVM",
            "KNN",
            "Neural Network",
            "AdaBoost",
            "Bagging",
            "Ridge Regression",
        ]
        main_layout = QVBoxLayout()
        alorgorithm_layout = QHBoxLayout()
        alorgorithm_layout.setContentsMargins(0, 0, 0, 0)
        data_layout = QHBoxLayout()
        self.Data_tab = QWidget()
        # Dropdown for algorithm selection
        self.tip = "算法："
        self.algorithm_label = QLabel(self.tip + self.algorithms[0])
        self.algorithm_label.setObjectName("H1")
        svg_data = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
        <path d="M7.72 21.78a.75.75 0 0 0 1.06-1.06L5.56 17.5h14.69a.75.75 0 0 0 0-1.5H5.56l3.22-3.22a.75.75 0 1 0-1.06-1.06l-4.5 4.5a.75.75 0 0 0 0 1.06l4.5 4.5Zm8.56-9.5a.75.75 0 1 1-1.06-1.06L18.44 8H3.75a.75.75 0 0 1 0-1.5h14.69l-3.22-3.22a.75.75 0 0 1 1.06-1.06l4.5 4.5a.75.75 0 0 1 0 1.06l-4.5 4.5Z"></path>
        </svg>
        """
        algorithm_button = IconButton(
            svg_data,
            "算法选择",
        )

        alorgorithm_layout.addWidget(self.algorithm_label)
        alorgorithm_layout.addSpacing(10)
        alorgorithm_layout.addWidget(algorithm_button)
        alorgorithm_layout.setAlignment(Qt.AlignLeft)

        self.combo = QComboBox()
        self.combo.addItems(self.algorithms)
        data_layout.addWidget(self.combo)

        # Run button
        self.run_button = QPushButton("运行")
        self.run_button.clicked.connect(self.run_algorithm)
        data_layout.addWidget(self.run_button)

        # Matplotlib canvas for visualization
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Combine layouts
        main_layout.addLayout(alorgorithm_layout)
        main_layout.addLayout(data_layout)
        pic_tip = QLabel("处理结果")
        pic_tip.setObjectName("H2")
        main_layout.addWidget(pic_tip)
        main_layout.addWidget(self.canvas, stretch=3)

        self.setLayout(main_layout)

    def run_algorithm(self):
        algorithm = self.combo.currentText()
        # Example visualization: random scatter
        self.ax.clear()
        x = np.random.rand(100)
        y = np.random.rand(100)
        self.ax.scatter(x, y, c="blue", alpha=0.5)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    app.setFont(QFont("Microsoft YaHei UI", 12))
    app.setStyleSheet(QSSLoader.load_qss_files("../style"))
    main_window.setWindowTitle("Data Mining and Attack Detection System")
    main_window.setGeometry(100, 100, 900, 600)

    data_tab = DataMiningTab()
    main_window.setCentralWidget(data_tab)

    main_window.show()
    sys.exit(app.exec_())
