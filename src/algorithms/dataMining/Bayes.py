import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# 设置 matplotlib 支持中文
import matplotlib

matplotlib.rcParams["font.sans-serif"] = ["SimHei"]  # 支持中文字体，如黑体
matplotlib.rcParams["axes.unicode_minus"] = False  # 显示负号


def naive_bayes_classifier(
    csv_path,
    ax,
    canva,
    label_column="quality",
    test_size=0.2,
    encoding="utf-8",
    sep=";",
):
    ax.clear()
    """
    参数：
    - csv_path：CSV 文件路径
    - label_column：标签列名
    - test_size：测试集比例
    - encoding：编码方式
    - sep：分隔符，默认适配分号
    """
    # 1. 读取数据
    df = pd.read_csv(csv_path, encoding=encoding, sep=sep)
    df = df.dropna()
    print(f"数据维度: {df.shape}")

    # 2. 特征与标签分离
    X = df.drop(columns=[label_column])
    y = df[label_column]
    class_names = sorted(y.unique().astype(str))  # 以字符串形式用于显示

    # 3. 数据划分
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    # 4. 模型训练
    model = GaussianNB()
    model.fit(X_train, y_train)

    # 5. 预测与评估
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("\n准确率：", round(acc * 100, 2), "%")
    print(
        "\n分类报告：\n",
        classification_report(y_test, y_pred, target_names=class_names),
    )

    # 6. 混淆矩阵可视化
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
    )
    ax.set_title("朴素贝叶斯混淆矩阵")
    ax.set_xlabel("预测标签")
    ax.set_ylabel("真实标签")
    plt.tight_layout()
    canva.draw()


# 调用
if __name__ == "__main__":
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import tkinter as tk
    from matplotlib.figure import Figure

    # 创建 Tkinter 窗口
    root = tk.Tk()
    root.title("朴素贝叶斯分类器")
    root.geometry("800x600")

    # 创建 Matplotlib Figure 和 Axes 对象
    fig = Figure(figsize=(6, 4))
    # 创建 Canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    ax = fig.add_subplot(111)
    naive_bayes_classifier(
        "../../res/data/winequality-white.csv",
        ax,
        canvas,
    )
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # 显示窗口
    root.mainloop()
    # 关闭 Tkinter 窗口
    root.destroy()
