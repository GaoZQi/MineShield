import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
import matplotlib


# 设置 matplotlib 支持中文
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]  # 使用黑体
matplotlib.rcParams["axes.unicode_minus"] = False  # 正常显示负号


def decision_tree_classifier_chinese(
    csv_path,
    ax,
    canvas,
    label_column="Purchased",  # 假设中文字段
    test_size=0.2,
    encoding="utf-8",
    max_depth=None,
    min_samples_split=2,
    criterion="gini",
    cv_folds=5,
    figsize=(15, 12),
):
    """
    中文可视化美化版决策树分类器：
    - 展示决策树结构（不保存图像）
    - 使用中文标签、美化图形
    """
    # 加载数据
    df = pd.read_csv(csv_path, encoding=encoding)
    df = df.dropna()

    X = df.drop(columns=[label_column])
    y = df[label_column]

    # 特征列编码
    cat_cols = X.select_dtypes(include=["object"]).columns
    encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan)
    if not cat_cols.empty:
        X[cat_cols] = encoder.fit_transform(X[cat_cols])

    # 标签编码
    le = LabelEncoder()
    y = le.fit_transform(y)

    # 数据划分
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=42
    )

    # 决策树与网格搜索
    base_model = DecisionTreeClassifier(
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        criterion=criterion,
        random_state=42,
    )

    param_grid = {"max_depth": [3, 5, 7, None], "min_samples_split": [2, 5, 10]}

    grid_search = GridSearchCV(base_model, param_grid, cv=cv_folds)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_

    # 中文类别名
    class_names = le.inverse_transform([i for i in range(len(le.classes_))])

    # 决策树图形展示（中文、彩色、圆角）
    plot_tree(
        best_model,
        feature_names=X.columns,  # 中文特征名
        class_names=class_names,  # 中文类别名
        filled=True,
        rounded=True,
        fontsize=12,
    )

    # 调整子图布局，确保居中显示
    ax.set_title("决策树结构", fontsize=12)
    canvas.draw()

    return best_model, grid_search.best_params_


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
    model, best_params = decision_tree_classifier_chinese(
        csv_path="../../res/data/sample1.csv",
        ax=ax,
        canvas=canvas,
        label_column="Purchased",
        max_depth=5,
        cv_folds=3,
        figsize=(25, 15),
    )

    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # 显示窗口
    root.mainloop()
    # 关闭 Tkinter 窗口
    root.destroy()
