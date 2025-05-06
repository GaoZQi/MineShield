import pandas as pd
import numpy as np
import math
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from urllib import parse as urlparse
import urllib
import warnings
warnings.filterwarnings("ignore")
import os
# -------- 🔍 特征提取函数 ----------
def extract_features(request_str):
    lower = request_str.lower()
    decoded = urllib.parse.unquote(request_str)
    parsed = urlparse.urlparse(decoded)
    url_len = len(request_str)

    # 参数解析
    params = urllib.parse.parse_qs(parsed.query)
    param_lengths = [len(v[0]) if v else 0 for v in params.values()]
    avg_param_len = np.mean(param_lengths) if param_lengths else 0

    # SQL关键词检测
    sql_keywords = ['select', 'insert', 'update', 'union', 'drop', 'script', 'iframe']
    has_sql_keyword = int(any(k in lower for k in sql_keywords))

    # 是否是base64（简单判定）
    is_base64 = int(('=' in request_str) and any(part.isalnum() and len(part) > 8 for part in request_str.split()))

    # 是否存在重复参数
    repeated_params = int(len(params) != len(set(params)))

    # 双重编码检测
    has_double_encoding = int('%25' in request_str)

    # 其他特征
    param_count = request_str.count('=')
    special_chars = ['\'', '"', '<', '>', '#', '&', '%', '`', ';', '\\']
    special_char_count = sum(request_str.count(c) for c in special_chars)
    is_encoded = 1 if request_str.count('%') >= 3 else 0
    keyword_count = sum(lower.count(k) for k in sql_keywords)
    path_depth = len(parsed.path.strip('/').split('/')) if parsed.path else 0
    digit_ratio = sum(c.isdigit() for c in request_str) / url_len
    alpha_ratio = sum(c.isalpha() for c in request_str) / url_len
    symbol_ratio = sum((not c.isalnum()) for c in request_str) / url_len

    tmp_dict = {}
    for c in request_str:
        tmp_dict[c] = tmp_dict.get(c, 0) + 1
    entropy = -sum((v / url_len) * math.log(v / url_len, 2) for v in tmp_dict.values())

    return pd.Series([
        avg_param_len, has_double_encoding, has_sql_keyword, is_base64, repeated_params,
        url_len, param_count, special_char_count, is_encoded,
        keyword_count, path_depth,
        digit_ratio, alpha_ratio, symbol_ratio, entropy
    ])

# 特征名顺序需与训练一致
feature_names = [
    'avg_param_len', 'has_double_encoding', 'has_sql_keyword', 'is_base64', 'repeated_params',
    'len', 'param_count', 'special_char_count', 'is_encoded',
    'keyword_count', 'path_depth',
    'digit_ratio', 'alpha_ratio', 'symbol_ratio', 'entropy'
]

# -------- 📦 预测数据预处理 ----------
def preprocess_data(file, label):
    data = pd.read_csv(file, delimiter='\t', encoding='utf-8')
    features = data['request'].apply(extract_features)
    features.columns = feature_names
    features['label'] = label
    return features

# -------- 🔮 主预测函数 ----------
def run_predict():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 输入攻击请求文件
    abnormal_file = input("请输入攻击请求文件路径（如 injec_.csv）：").strip()
    normal_file = os.path.join(BASE_DIR,'../../../res/data/I SVM-SQL/pass_.csv')
    model_file = os.path.join(BASE_DIR,'../../../res/model/SVC-SQL/svc_model.pkl')
    scaler_file = os.path.join(BASE_DIR,'../../../res/model/SVC-SQL/scaler.pkl')

    print("\n📦 正在读取和处理测试数据...")
    normal_data = preprocess_data(normal_file, 0)
    abnormal_data = preprocess_data(abnormal_file, 1)
    test_data = pd.concat([normal_data, abnormal_data], axis=0)

    y_true = test_data['label'].values
    X_test = test_data.drop(['label'], axis=1)

    print("⚙️ 加载 scaler 并进行标准化...")
    scaler = joblib.load(scaler_file)
    X_test = X_test[scaler.feature_names_in_]
    X_scaled = scaler.transform(X_test)

    print("🤖 加载模型进行预测...")
    model = joblib.load(model_file)
    y_pred = model.predict(X_scaled)

    # 输出结果
    acc = accuracy_score(y_true, y_pred)
    print(f"\n🎯 模型预测准确率：{acc:.4f}")
    print("\n📄 分类报告：\n", classification_report(y_true, y_pred, target_names=['正常请求', '攻击请求']))

    cm = confusion_matrix(y_true, y_pred)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['正常请求（预测）', '攻击请求（预测）'],
                yticklabels=['正常请求（实际）', '攻击请求（实际）'])
    plt.xlabel('预测结果')
    plt.ylabel('真实标签')
    plt.title('预测混淆矩阵')
    plt.tight_layout()

# -------- 🚀 启动入口 ----------
if __name__ == '__main__':
    run_predict()
