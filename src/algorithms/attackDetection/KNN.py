import joblib
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

# 60,0,64,4444,80,0,2,8192,20,12345,1,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1

class AttackKNNDetector:
    def __init__(self):
        """
        初始化模型、编码器、特征名
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = joblib.load(
            os.path.normpath(
                os.path.join(base_dir, "../../../res/model/KNN/knn_attack_model.pkl")
            )
        )
        self.encoder = joblib.load(
            os.path.normpath(
                os.path.join(base_dir, "../../../res/model/KNN/label_encoder.pkl")
            )
        )
        self.feature_names = joblib.load(
            os.path.normpath(
                os.path.join(base_dir, "../../../res/model/KNN/feature_names.pkl")
            )
        )

    def parse_text_to_dataframe(self, text: str) -> pd.DataFrame:
        """
        将输入的原始文本（CSV格式）转换为模型需要的DataFrame
        :param text: 一行CSV格式文本，例如：'60,0,0,12345,80,...'
        :return: DataFrame对象（包含特征列）
        """
        values = text.strip().split(",")
        df = pd.DataFrame([values], columns=self.feature_names)
        df = df.apply(pd.to_numeric, errors="coerce")  # 保证数值型
        return df

    def predict_from_text(self, text: str) -> str:
        """
        从CSV格式字符串预测标签
        :param text: 字符串，如 '60,0,0,12345,80,...'
        :return: 预测标签（如 'normal' 或 'malicious'）
        """
        df = self.parse_text_to_dataframe(text)
        pred = self.model.predict(df)
        return self.encoder.inverse_transform(pred)[0]


if __name__ == "__main__":
    # 示例输入（用你的特征顺序拼一行字符串）
    text = input("请输入CSV格式特征数据：\n")
    model = AttackKNNDetector()
    result = model.predict_from_text(text)
    print("预测结果：", result)
