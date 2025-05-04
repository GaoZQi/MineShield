import time
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest as SKIsolationForest
import matplotlib.pyplot as plt


def run_isolation_forest(file_path: str, ax, canvas):
    """
    在传入的 ax 上绘制 IsolationForest 的决策边界与点分布，
    绘制完成后调用 canvas.draw() 刷新画布。

    参数:
        file_path (str): CSV 文件路径，假设所有列均为数值特征或前两列为二维特征。
        ax (matplotlib.axes.Axes): 目标坐标轴对象。
        canvas (FigureCanvas): Qt5 的 FigureCanvasQTAgg 对象，用于刷新显示。
    """
    # 设置中文字体
    # 指定中文字体为 Microsoft YaHei
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei"
    ]  # :contentReference[oaicite:0]{index=0}
    # 解决负号 '-' 显示为方块的问题
    plt.rcParams["axes.unicode_minus"] = False  # :contentReference[oaicite:1]{index=1}

    # 1. 加载数据
    df = pd.read_csv(file_path)
    X = df.values
    # 只保留前两列作为二维特征
    if X.shape[1] > 2:
        X = X[:, :2]

    # 2. 算法与网格准备
    outliers_fraction = 0.15
    n_samples = X.shape[0]
    n_outliers = int(outliers_fraction * n_samples)
    rng = np.random.RandomState(42)
    algo = SKIsolationForest(contamination=outliers_fraction, random_state=42)

    xx, yy = np.meshgrid(
        np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 150),
        np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, 150),
    )

    # 3. 清空旧图
    ax.clear()

    # 4. 向原始数据中添加噪声点
    X_all = np.concatenate(
        [
            X,
            rng.uniform(
                low=X.min(axis=0) - 1, high=X.max(axis=0) + 1, size=(n_outliers, 2)
            ),
        ],
        axis=0,
    )

    # 5. 拟合与预测
    t0 = time.time()
    algo.fit(X_all)
    t1 = time.time()
    y_pred = algo.predict(X_all)

    # 6. 绘制决策边界
    Z = algo.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    # 等高线 0 表示边界
    ax.contour(
        xx, yy, Z, levels=[0], linewidths=2, colors="black"
    )  # :contentReference[oaicite:0]{index=0}

    # 7. 绘制数据点
    colors = np.array(["#377eb8", "#ff7f00"])
    ax.scatter(
        X_all[:, 0],
        X_all[:, 1],
        s=10,
        c=colors[(y_pred + 1) // 2],
        edgecolors="k",
        alpha=0.7,
    )

    # 8. 注释运行时间
    ax.text(
        0.99,
        0.01,
        f"{t1-t0:.2f}s",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=10,
    )

    # 9. 设置坐标轴范围与标签
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Isolation Forest 检测结果")  # :contentReference[oaicite:1]{index=1}

    # 10. 刷新画布
    canvas.draw()


if __name__ == "__main__":
    # 测试 run_isolation_forest 函数
    import matplotlib.pyplot as plt
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

    app = QApplication([])
    main_window = QMainWindow()
    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)

    run_isolation_forest(
        "../../../res/data/4 Isolation_Forest/train_dataset.csv", ax, canvas
    )

    main_window.show()
    app.exec_()
