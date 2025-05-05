import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


class GBDTPredictor:
    def __init__(self, data_path=None):
        """
        初始化模型加载器
        现在模型路径固定，数据集路径可以通过参数传入
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # 固定模型路径
        self.model_path = os.path.normpath(
            os.path.join(base_dir, "../../../res/model/GBDT/ddos_gbdt_model.pkl")
        )

        # 如果没有提供数据集路径，使用默认路径
        self.data_path = (
            data_path if data_path else "../../../res/data/DDos/DDoS_dataset.csv"
        )

        # 加载模型和标准化器
        self.model = joblib.load(self.model_path)
        self.scaler = StandardScaler()

    def predict(self):
        """
        对给定数据集进行 DDoS 攻击预测，并输出每个样本的 DDoS 攻击概率
        """
        # 1. 加载数据
        data = pd.read_csv(self.data_path)

        # 2. 删除无关特征：'Source IP' 和 'Dest IP' 列
        data = data.drop(columns=["Source IP", "Dest IP"])

        # 3. 对类别特征进行标签编码
        label_encoder = LabelEncoder()
        data["Highest Layer"] = label_encoder.fit_transform(data["Highest Layer"])
        data["Transport Layer"] = label_encoder.fit_transform(data["Transport Layer"])

        # 4. 假设 'target' 列是目标变量，我们丢弃它，只保留特征
        X = data.drop(columns=["target"])  # 特征

        # 5. 数据标准化
        X_scaled = self.scaler.fit_transform(X)  # 使用训练数据的标准化参数

        # 6. 获取每个样本的 DDoS 攻击概率
        y_prob = self.model.predict_proba(X_scaled)[
            :, 1
        ]  # 获取每个样本属于类别 1（DDoS 攻击）的概率

        # 7. 将预测概率添加到原数据中
        data["ddos_probability"] = y_prob  # 添加 DDoS 攻击的概率列

        # 8. 保存结果到 CSV 文件
        result_path = os.path.join(
            os.path.dirname(self.data_path), "prediction_with_probabilities.csv"
        )
        data.to_csv(result_path, index=False)
        print(f"预测结果已保存到 {result_path}")

        # 返回所有样本的 DDoS 攻击概率
        return data["ddos_probability"]


def main():
    # 获取用户输入的数据集路径
    data_path = input("请输入数据集文件路径（默认路径为 test/DDos_predict.csv）：")

    # 如果用户没有输入路径，则使用默认路径
    if not data_path:
        data_path = "../../res/data/DDos/DDoS_dataset.csv"

    # 初始化预测器，传入数据集路径
    predictor = GBDTPredictor(data_path=data_path)

    # 调用预测方法
    probabilities = predictor.predict()

    # 输出预测的 DDoS 攻击概率
    print("DDoS 攻击概率：")
    print(probabilities)


if __name__ == "__main__":
    main()
