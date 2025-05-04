import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix

class OneClassSVMPredictor:
    def __init__(self, model_path='../../res/model/One-Class_SVM_model.pkl'):
        """
        初始化加载模型，默认模型路径为 model/One-Class_SVM_model.pkl
        """
        self.model_dict = joblib.load(model_path)
        self.model = self.model_dict['model']
        self.scaler = self.model_dict['scaler']
        self.label_encoders = self.model_dict['encoders']
        self.columns = self.model_dict['columns']

    def preprocess(self, df):
        categorical_cols = ['protocol_type', 'service', 'flag']
        for col in categorical_cols:
            df[col] = self.label_encoders[col].transform(df[col])

        X = df.drop(columns=['label', 'difficulty'])
        X = X[self.columns]
        X_scaled = self.scaler.transform(X)
        y_true = df['label'].apply(lambda x: 1 if x == 'normal' else -1)
        return X_scaled, y_true

    def predict(self, df):
        X_scaled, y_true = self.preprocess(df)
        y_pred = self.model.predict(X_scaled)
        return y_pred, y_true

    def evaluate(self, y_true, y_pred):
        print("One-Class SVM Intrusion Detection Report:")
        print(classification_report(y_true, y_pred, target_names=['Attack', 'Normal']))

        cm = confusion_matrix(y_true, y_pred, labels=[1, -1])
        print("\nConfusion Matrix:")
        print(cm)

    def predict_and_report(self, test_file_path):
        """
        简洁预测统计输出（无文件保存）
        """
        df = pd.read_csv(test_file_path)
        y_pred, y_true = self.predict(df)

        normal_count = (y_pred == 1).sum()
        attack_count = (y_pred == -1).sum()
        total = len(y_pred)

        print("\n预测结果:")
        print(f"预测总数据量: {total}")
        print(f"预测正常流量数: {normal_count}")
        print(f"预测异常流量数: {attack_count}")

        self.evaluate(y_true, y_pred)

    def run_user_input_predict(self):
        """
        用户输入测试文件路径，执行预测与输出
        """
        print("\n请输入测试集 CSV 文件路径（例如 train/data/One_Class_SVM_data/KDDTest+.csv）：")
        test_file_path = input("测试文件路径: ").strip()
        self.predict_and_report(test_file_path)

if __name__ == "__main__":
    model = OneClassSVMPredictor()
    model.run_user_input_predict()
