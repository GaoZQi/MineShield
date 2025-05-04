import joblib
import re

class SQLDetectModel:
    def __init__(self, model_pkl="../../res/model/xgboost_model.pkl", le_pkl="../../res/model/sqllabel_encoder.pkl", vectorizer_pkl="../../res/model/vectorizer.pkl"):
        # 初始化时加载模型、标签编码器和vectorizer
        self.model = joblib.load(model_pkl)
        self.le = joblib.load(le_pkl)
        self.vectorizer = joblib.load(vectorizer_pkl)  # 加载保存的vectorizer

    def predict(self, user_agent):
        # 将输入的User-Agent进行处理
        user_agent = user_agent.strip()

        # 将User-Agent转化为特征向量
        X_new = self.vectorizer.transform([user_agent])

        # 使用加载的模型进行预测
        prediction = self.model.predict(X_new)

        # 将预测的标签解码为原始标签
        decoded_prediction = self.le.inverse_transform(prediction)

        # 返回预测结果
        return decoded_prediction[0]  # 预测结果为 0 或 1

def process_log_and_predict(log_path, model):
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # 使用正则表达式从日志中提取 User-Agent
                match = re.search(r'".*?" "(.*?)"$', line)  # 提取最后的User-Agent部分
                
                if match:
                    user_agent = match.group(1)  # 提取User-Agent
                    print(f"正在检测的User-Agent: {user_agent}")  # 打印User-Agent
                    result = model.predict(user_agent)

                    if result == 1:
                        print(f"该User-Agent ({user_agent}) 为恶意请求")
                    else:
                        print(f"该User-Agent ({user_agent}) 为正常请求")
            except IndexError:
                # 如果日志格式错误或无法解析User-Agent，跳过
                print(f"无法解析的日志行: {line}")
                continue

if __name__ == '__main__':
    # 提供日志文件路径
    log_path = input("请输入日志文件路径：")

    # 加载训练好的模型
    model = SQLDetectModel()

    # 处理日志并进行预测
    process_log_and_predict(log_path, model)
