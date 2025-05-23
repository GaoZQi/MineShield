import joblib
import warnings
import os
warnings.filterwarnings("ignore")


def get_ngrams(query) -> list:
    tempQuery = str(query)
    ngrams = []
    for i in range(0, len(tempQuery) - 3):
        ngrams.append(tempQuery[i : i + 3])
    return ngrams


class Model:
    def __init__(self):
        """
        初始化模型、编码器、特征名
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.vectorizer = joblib.load(
            os.path.normpath(
                os.path.join(base_dir, "../../../res/model/Logistics_Regression/vectorizer-LOG.pkl")
            )
        )
        self.model = joblib.load(
            os.path.normpath(
                os.path.join(base_dir, "../../../res/model/Logistics_Regression/lg-urldetect.pkl")
            )
        )

    def predict(self, url: str) -> bool:
        """
        :param url: url
        :return: 1 or 0
        """
        req = self.vectorizer.transform([url])
        result = self.model.predict(req)
        return result[0]


if __name__ == "__main__":
    url = input("请输入要检测的URL：")
    model = Model()
    result = model.predict(url)
    if result:
        print("该URL为恶意请求")
    else:
        print("该URL为正常请求")
