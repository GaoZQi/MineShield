import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


def predict_content_length_from_csv(
    csv_path, ax, canvas, encoding="utf-8", test_size=0.2
):
    """
    读取CSV文件，使用title + content文本训练线性回归模型预测content长度

    参数:
    - csv_path: str, CSV文件路径
    - encoding: str, 文件编码（默认UTF-8）
    - test_size: float, 测试集占比（默认0.2）

    返回:
    - result_df: DataFrame，包含真实长度、预测长度和误差
    - mse: float，均方误差
    """
    # 读取数据
    df = pd.read_csv(csv_path, encoding=encoding)
    df = df.dropna(subset=["title", "content"])

    # 构造伪标签：content长度
    df["target"] = df["content"].apply(len)

    # 文本合并并向量化
    combined_text = df["title"] + " " + df["content"]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(combined_text)
    y = df["target"]

    # 划分训练和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    # 模型训练与预测
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # 构建结果表格
    result_df = pd.DataFrame(
        {"True Length": y_test.values, "Predicted Length": y_pred.round(2)}
    )
    result_df["Error"] = (
        (result_df["True Length"] - result_df["Predicted Length"]).abs().round(2)
    )

    # 输出MSE
    mse = mean_squared_error(y_test, y_pred)
    print(result_df)
    print("Mean Squared Error (MSE):", round(mse, 2))

    ax.clear()
    ax.scatter(range(len(y_test)), y_test, label="True", color="blue")
    ax.scatter(range(len(y_pred)), y_pred, label="Predicted", color="orange")
    ax.set_title("Content Length Prediction (Linear Regression)")
    ax.set_xlabel("Sample Index")
    ax.set_ylabel("Content Length")
    ax.legend()
    ax.grid(True)
    canvas.draw()
