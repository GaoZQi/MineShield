import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 指定中文字体为 Microsoft YaHei
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei"
]  # :contentReference[oaicite:0]{index=0}
# 解决负号 '-' 显示为方块的问题
plt.rcParams["axes.unicode_minus"] = False  # :contentReference[oaicite:1]{index=1}


def pca_analysis(file_path):
    # 读取生成的网络流量数据集（包含5个特征）
    df = pd.read_csv(file_path, encoding="utf-8")

    # 标准化数据（PCA 对数据的尺度非常敏感，因此需要标准化）
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    # 应用 PCA，设定降至 2 维
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(df_scaled)

    # 创建包含主成分的数据集
    pca_df = pd.DataFrame(
        data=principal_components,
        columns=["Principal Component 1", "Principal Component 2"],
    )

    # 输出降维后的数据
    print("降维后的数据（前五行）：")
    print(pca_df.head())

    # 输出主成分的方差解释比率（即每个主成分对方差的贡献）
    print("\n主成分的方差解释比率:")
    print(pca.explained_variance_ratio_)

    # 输出所有主成分的累计方差解释比率
    print("\n累计方差解释比率:")
    print(np.cumsum(pca.explained_variance_ratio_))


import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def plot_pca_scatter(file_path: str, ax, canvas):
    """
    从 file_path 读取数据，做标准化和 PCA 降维（2D），
    并在传入的 ax 上绘制散点图，最后调用 canvas.draw() 刷新。
    参数:
        file_path (str): 待分析的 CSV 文件路径，假设所有列均为数值特征。
        ax (matplotlib.axes.Axes): 用于绘图的坐标轴对象。
        canvas (FigureCanvas): Qt5 中的画布对象，绘图后需要调用 draw() 刷新。
    """
    # 1. 读取并标准化
    df = pd.read_csv(file_path, encoding="utf-8")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)

    # 2. PCA 降到 2 维
    pca = PCA(n_components=2, random_state=42)
    pcs = pca.fit_transform(X_scaled)

    # 3. 绘制散点图
    ax.clear()
    ax.scatter(
        pcs[:, 0], pcs[:, 1], s=50, edgecolors="black", linewidths=0.5, alpha=0.7
    )
    ax.set_title("PCA 散点图")
    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")
    ax.grid(True)

    # 4. 刷新画布
    canvas.draw()


if __name__ == "__main__":

    # 示例：调用 pca_analysis 函数进行 PCA 分析
    file_path = "../../res/data/Apriori/network_traffic_pca.csv"  # 替换为实际文件路径
    pca_analysis(file_path)
