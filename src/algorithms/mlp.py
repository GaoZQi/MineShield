import pandas as pd
import joblib  # 用于加载训练的 MLPClassifier 模型
from tensorflow.keras.models import load_model  # 用于加载训练的 Keras 模型
import tensorflow as tf  # 导入 TensorFlow
from io import StringIO
from sklearn.metrics import accuracy_score

# 自定义 Keras 指标
def recall_m(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)
    true_positives = tf.reduce_sum(tf.round(tf.clip_by_value(y_true * y_pred, 0, 1)))
    possible_positives = tf.reduce_sum(tf.round(tf.clip_by_value(y_true, 0, 1)))
    recall = true_positives / (possible_positives + tf.keras.backend.epsilon())
    return recall

def precision_m(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)
    true_positives = tf.reduce_sum(tf.round(tf.clip_by_value(y_true * y_pred, 0, 1)))
    predicted_positives = tf.reduce_sum(tf.round(tf.clip_by_value(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + tf.keras.backend.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + tf.keras.backend.epsilon()))


class ModelPredictor:
    def __init__(self, mlp_model_path, keras_model_path, onehot_encoder_path, scaler_path):
        """
        初始化模型预测类。

        :param mlp_model_path: 训练好的 MLPClassifier 模型路径。
        :param keras_model_path: 训练好的 Keras 模型路径。
        :param onehot_encoder_path: 训练时保存的 OneHotEncoder 文件路径。
        :param scaler_path: 训练时保存的 scaler 文件路径。
        """
        self.mlp_model_path = mlp_model_path
        self.keras_model_path = keras_model_path
        self.onehot_encoder_path = onehot_encoder_path
        self.scaler_path = scaler_path
        self.mlp_model = None
        self.keras_model = None
        self.onehot_encoder = None
        self.scaler = None

    def load_models(self):
        """加载保存的模型、OneHotEncoder 和 scaler"""
        self.mlp_model = joblib.load(self.mlp_model_path)
        self.keras_model = load_model(self.keras_model_path, custom_objects={'f1_m': f1_m, 'precision_m': precision_m, 'recall_m': recall_m})
        self.onehot_encoder = joblib.load(self.onehot_encoder_path)
        self.scaler = joblib.load(self.scaler_path)

    def preprocess_data(self, sample):
        """对输入的样例数据进行预处理"""
        # 将 CSV 格式的单行数据读取到 pandas DataFrame
        sample_data = pd.read_csv(StringIO(sample), header=None)

        # 给每一列命名（你提供的输入样例中列名没有，所以需要手动设置）
        columns = [
            'id', 'dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate',
            'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit',
            'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean', 'dmean',
            'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm',
            'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'is_ftp_login', 'ct_ftp_cmd',
            'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst', 'is_sm_ips_ports', 'attack_cat', 'label'
        ]
        sample_data.columns = columns

        # 删除不必要的列（如 attack_cat 和 label）
        sample_data = sample_data.drop(columns=['attack_cat', 'label'], errors='ignore')  # 删除 'attack_cat' 和 'label' 列

        # 将列名转换为字符串类型
        sample_data.columns = sample_data.columns.astype(str)

        # 对类别特征进行 OneHot 编码
        categorical_columns = ['proto', 'service', 'state']
        sample_categorical = sample_data[categorical_columns]
        sample_onehot = self.onehot_encoder.transform(sample_categorical)

        # 合并 OneHot 编码后的特征与其他数值特征
        sample_data = sample_data.drop(columns=categorical_columns)
        sample_data = pd.concat([sample_data, pd.DataFrame(sample_onehot.toarray())], axis=1)

        # 将列名转换为字符串类型
        sample_data.columns = sample_data.columns.astype(str)

        # 标准化样例数据
        sample_scaled = self.scaler.transform(sample_data)  # 使用训练时的 scaler 对样例数据进行标准化

        return sample_scaled


    def predict(self, sample):
        """使用训练好的模型进行预测"""
        # 对输入样例数据进行预处理
        sample_scaled = self.preprocess_data(sample)

        # 检查模型是否加载成功
        if self.mlp_model is None or self.keras_model is None:
            print("Models are not loaded. Please load the models first.")
            return

        # MLPClassifier 模型预测
        prediction_mlp = self.mlp_model.predict(sample_scaled)  # 预测

        # Keras 模型预测
        prediction_keras = self.keras_model.predict(sample_scaled)  # 预测
        prediction_keras = (prediction_keras > 0.5).astype(int)  # 二分类: 大于0.5预测为1，否者为0

        # 输出预测结果
        if prediction_mlp == 1 or prediction_keras == 1:
            return "Predicted: Attack"
        else:
            return "Predicted: Normal"
        
    def evaluate(self, test_data_path):
        """加载测试数据并输出预测准确率"""
        # 读取测试数据
        df = pd.read_csv(test_data_path)
        
        # 特征与标签分离
        X_test = df.drop(columns=['label', 'attack_cat'])
        y_test = df['label']
        
        # 对类别特征进行 OneHot 编码
        categorical_columns = ['proto', 'service', 'state']
        X_test_categorical = X_test[categorical_columns]
        X_test_onehot = self.onehot_encoder.transform(X_test_categorical)

        # 合并 OneHot 编码后的特征与其他数值特征
        X_test = X_test.drop(columns=categorical_columns)
        X_test = pd.concat([X_test, pd.DataFrame(X_test_onehot.toarray())], axis=1)

        # 确保所有列名都是字符串类型
        X_test.columns = X_test.columns.astype(str)

        # 标准化测试数据
        X_test_scaled = self.scaler.transform(X_test)  # 使用训练时的 scaler 对测试数据进行标准化

        # 预测结果
        y_pred_mlp = self.mlp_model.predict(X_test_scaled)
        y_pred_keras = (self.keras_model.predict(X_test_scaled) > 0.5).astype(int)

        # 计算准确率
        accuracy_mlp = accuracy_score(y_test, y_pred_mlp)
        accuracy_keras = accuracy_score(y_test, y_pred_keras)

        print(f"MLP Classifier Accuracy: {accuracy_mlp:.4f}")
        print(f"Keras Model Accuracy: {accuracy_keras:.4f}")

        

if __name__ == '__main__':
    # 初始化模型预测器
    mlp_model_path = '../../res/model/mlp_model_trained.pkl'
    keras_model_path = '../../res/model/keras_mlp_model_trained.keras'
    onehot_encoder_path = '../../res/model/onehot_encoder.pkl'
    scaler_path = '../../res/model/scaler-mlp.pkl'

    predictor = ModelPredictor(mlp_model_path=mlp_model_path, keras_model_path=keras_model_path, onehot_encoder_path=onehot_encoder_path, scaler_path=scaler_path)

    # 加载模型
    predictor.load_models()

    # 输入测试集样例，按 CSV 格式传入
    sample = "51213,0.999352,tcp,http,FIN,10,10,800,1190,19.01232,62,252,5763.734863,8573.555664,2,2,111.039111,98.288445,6662.074451,165.358922,255,1472115402,1201817275,255,0.288347,0.114102,0.174245,80,119,1,149,5,1,2,2,1,5,0,0,1,2,5,0,Analysis,1"

    # 进行预测并输出结果
    result = predictor.predict(sample)
    print(result)

    # 评估并输出测试准确率
    test_data_path = '../../res/data/MLP/UNSW_NB15_testing-set.csv'  # 替换为测试集路径
    predictor.evaluate(test_data_path)
