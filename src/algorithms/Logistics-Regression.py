import joblib
import warnings
warnings.filterwarnings("ignore")
def get_ngrams(query) -> list:
    tempQuery = str(query)
    ngrams = []
    for i in range(0, len(tempQuery) - 3):
        ngrams.append(tempQuery[i:i + 3])
    return ngrams


class Model:
    def __init__(self):
        self.vectorizer = joblib.load('../../res/model/vectorizer-LOG.pkl')
        self.model = joblib.load('../../res/model/lg-urldetect.pkl')

    def predict(self, url: str) -> bool:
        """
        :param url: url
        :return: 1 or 0
        """
        req = self.vectorizer.transform([url])
        result = self.model.predict(req)
        return result[0]


if __name__ == '__main__':
    url = input("请输入要检测的URL：")
    model = Model()
    result = model.predict(url)
    if result:
        print("该URL为恶意请求")
    else:
        print("该URL为正常请求")
