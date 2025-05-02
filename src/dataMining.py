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

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from widget.RoundWidget import RoundWidget


class DataMiningTab(RoundWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        self.Data_tab = QWidget()
        # Dropdown for algorithm selection
        self.combo = QComboBox()
        self.combo.addItems(
            [
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
        )
        top_layout.addWidget(QLabel("选择算法:"))
        top_layout.addWidget(self.combo)

        # Run button
        self.run_button = QPushButton("运行")
        self.run_button.clicked.connect(self.run_algorithm)
        top_layout.addWidget(self.run_button)

        # Matplotlib canvas for visualization
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Log text box
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setPlaceholderText("Log output...")

        # Combine layouts
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.canvas, stretch=3)

        self.setLayout(main_layout)

    def run_algorithm(self):
        algorithm = self.combo.currentText()
        self.log_text.append(f"Running {algorithm}...")

        # Example visualization: random scatter
        self.ax.clear()
        x = np.random.rand(100)
        y = np.random.rand(100)
        self.ax.scatter(x, y, c="blue", alpha=0.5)
        self.ax.set_title(f"Visualization of {algorithm}")
        self.canvas.draw()

        self.log_text.append(f"{algorithm} completed.\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setWindowTitle("Data Mining and Attack Detection System")
    main_window.setGeometry(100, 100, 900, 600)

    data_tab = DataMiningTab()
    main_window.setCentralWidget(data_tab)

    main_window.show()
    sys.exit(app.exec_())
