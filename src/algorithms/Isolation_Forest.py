import time
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest as SKIsolationForest
from sklearn.datasets import make_blobs, make_moons


def load_datasets_from_folder(folder_path):
    datasets = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            # 使用pandas读取CSV文件
            data = pd.read_csv(file_path)

            # 假设数据集的格式是二维的，如果是其他格式，可以进行调整
            # 转换为numpy数组（如果需要）
            datasets.append(data.values)

    return datasets


def run_isolation_forest(folder_path, ax=None, canvas=None):
    matplotlib.rcParams["contour.negative_linestyle"] = "solid"

    # Example settings
    n_samples = 300
    outliers_fraction = 0.15
    n_outliers = int(outliers_fraction * n_samples)
    n_inliers = n_samples - n_outliers

    anomaly_algorithms = [
        (
            "Isolation Forest",
            SKIsolationForest(contamination=outliers_fraction, random_state=42),
        ),
    ]

    # Load datasets from the folder (传递folder_path作为参数)
    datasets = load_datasets_from_folder(folder_path)

    # Compare given classifiers under given settings
    xx, yy = np.meshgrid(np.linspace(-7, 7, 150), np.linspace(-7, 7, 150))

    plt.figure(figsize=(len(anomaly_algorithms) * 2 + 3, 12.5))
    plt.subplots_adjust(
        left=0.02, right=0.98, bottom=0.001, top=0.96, wspace=0.05, hspace=0.01
    )

    plot_num = 1
    rng = np.random.RandomState(42)

    for i_dataset, X in enumerate(datasets):
        # Add outliers
        X = np.concatenate(
            [X, rng.uniform(low=-6, high=6, size=(n_outliers, 2))], axis=0
        )
        # n_features = X.shape[1]
        # X = np.concatenate(
        #     [X, rng.uniform(low=-6, high=6, size=(n_outliers, n_features))], axis=0
        # )

        for name, algorithm in anomaly_algorithms:
            t0 = time.time()
            algorithm.fit(X)
            t1 = time.time()
            plt.subplot(len(datasets), len(anomaly_algorithms), plot_num)
            if i_dataset == 0:
                plt.title(name, size=18)

            # Fit the data and tag outliers
            y_pred = algorithm.fit(X).predict(X)

            # Plot the levels lines and the points
            Z = algorithm.predict(np.c_[xx.ravel(), yy.ravel()])
            Z = Z.reshape(xx.shape)
            plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors="black")

            colors = np.array(["#377eb8", "#ff7f00"])
            plt.scatter(X[:, 0], X[:, 1], s=10, color=colors[(y_pred + 1) // 2])

            plt.xlim(-7, 7)
            plt.ylim(-7, 7)
            plt.xticks(())
            plt.yticks(())
            plt.text(
                0.99,
                0.01,
                ("%.2fs" % (t1 - t0)).lstrip("0"),
                transform=plt.gca().transAxes,
                size=15,
                horizontalalignment="right",
            )
            plot_num += 1

    plt.show()


# 调用修改后的函数，并传入文件夹路径
folder_path = "../../res"  # 替换为实际路径
run_isolation_forest(folder_path)
