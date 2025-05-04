import joblib
import os
import re
import nltk
import urlextract
from html import unescape
from email import parser, policy
import warnings
warnings.filterwarnings("ignore")
class Model:
    def __init__(self):
        """
        初始化模型，加载已保存的向量器、SVM模型和标签编码器
        """
        self.vectorizer = joblib.load('../../res/model/vectorizer-SVM.pkl')     # 加载TF-IDF向量器
        self.model = joblib.load('../../res/model/svm-emaildetect.pkl')     # 加载训练好的SVM模型
        self.encoder = joblib.load('../../res/model/labelencoder.pkl')      # 加载标签编码器
        self.extractor = urlextract.URLExtract()                  # 初始化URL提取器
        self.stopwords_list = nltk.corpus.stopwords.words('english')  # 获取英文停用词
        for i in range(97, 123):                                  # 添加单个字符a-z为停用词
            self.stopwords_list.append(chr(i))
        self.token = nltk.stem.SnowballStemmer('english')         # 初始化词干提取器

    def email_to_text(self, email):
        """
        提取邮件正文内容（优先使用text/plain，其次text/html）

        :param email: EmailMessage对象
        :return: 文本内容字符串
        """
        html = None
        for part in email.walk():
            ctype = part.get_content_type()
            if ctype not in ('text/plain', 'text/html'):
                continue
            try:
                content = part.get_content()
            except LookupError:
                content = str(part.get_payload())
            if ctype == 'text/plain':
                return content
            else:
                html = content
        return self.html_to_plain_text(html) if html else ""

    def html_to_plain_text(self, html):
        """
        将HTML内容转换为纯文本

        :param html: HTML文本
        :return: 清洗后的纯文本
        """
        text = re.sub('<head.*?>.*?</head>', '', html, flags=re.M | re.S | re.I)
        text = re.sub(r'<[aA]\s.*?>', 'HYPERLINK', text, flags=re.M | re.S | re.I)
        text = re.sub(r'<img\s.*?>', 'IMAGE', text, flags=re.M | re.S | re.I)
        text = re.sub('<.*?>', '', text, flags=re.M | re.S)
        text = re.sub(r'(\s*\n)+', '\n', text, flags=re.M | re.S)
        return unescape(text)

    def word_split(self, email):
        """
        对邮件文本进行分词、清洗、去停用词和词干提取

        :param email: EmailMessage对象
        :return: 预处理后的字符串
        """
        text = self.email_to_text(email)
        text = text.lower()
        text = re.sub(r'\W+', ' ', text, flags=re.M)
        urls = list(set(self.extractor.find_urls(text)))
        urls.sort(key=lambda item: len(item), reverse=True)
        for url in urls:
            text = text.replace(url, "URL")
        text = re.sub(r'\d+(?:\.\d*[eE]\d+)?', 'NUMBER', text)
        content = nltk.word_tokenize(text)
        all_words = [self.token.stem(word) for word in content if word not in self.stopwords_list]
        return ' '.join(all_words)

    def predict(self, file_path: str) -> bool:
        """
        预测邮件是否为恶意邮件

        :param file_path: 邮件文件路径（EML格式或RFC822格式）
        :return: True 表示恶意邮件，False 表示正常邮件
        """
        with open(file_path, 'rb') as f:
            email = parser.BytesParser(policy=policy.default).parse(f)
        text = self.word_split(email)
        tfidf = self.vectorizer.transform([text])
        result = self.model.predict(tfidf)
        return bool(result[0])

if __name__ == '__main__':
    path = input("请输入邮件文件路径：")  # 示例输入：trec07p/data/inmail.1
    model = Model()
    result = model.predict(path)
    if result:
        print("该邮件为恶意邮件")
    else:
        print("该邮件为正常邮件")
