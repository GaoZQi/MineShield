import pickle
import numpy as np
import re
import nltk
import matplotlib.pyplot as plt
from urllib.parse import unquote
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import pandas as pd
import os
import sys
import warnings
warnings.filterwarnings("ignore")
# 设置中文显示
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 获取当前脚本所在目录，支持相对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 拼接模型和 tokenizer 路径（支持相对路径）
model_path = os.path.join(BASE_DIR, "../../../res/model/LSTM-XSS/xss_model.h5")
tokenizer_path = os.path.join(BASE_DIR, "../../../res/model/LSTM-XSS/tokenizer-XSS.pkl")

# ----------------------------
# 加载模型和 tokenizer
# ----------------------------
model = load_model(model_path)
with open(tokenizer_path, "rb") as f:
    tokenizer = pickle.load(f)

# ----------------------------
# 分词函数
# ----------------------------
def GeneSeg(payload):
    payload = payload.lower()
    payload = unquote(unquote(payload))
    payload = re.sub(r'\d+', "0", payload)
    payload = re.sub(r'(http|https)://[a-zA-Z0-9\.@&/#!#\?]+', "http://u", payload)
    r = r'''(?x)[\w\.]+?\(|\)|"\w+?"|'\w+?'|http://\w|</\w+>|<\w+>|<\w+|\w+=|>|[\w\.]+'''
    return nltk.regexp_tokenize(payload, r)

# ----------------------------
# 让用户输入 CSV 数据路径（可以是相对路径）
# ----------------------------
data_file_input = input("请输入带标签的 CSV 数据集路径（包含 id, Sentence, label 三列）: ").strip()
data_file_path = os.path.abspath(os.path.join(os.getcwd(), data_file_input))

if not os.path.isfile(data_file_path):
    print(f"❌ 文件不存在：{data_file_path}")
    sys.exit()

# ----------------------------
# 读取 CSV 数据（兼容中文编码）
# ----------------------------
try:
    data = pd.read_csv(data_file_path)
except UnicodeDecodeError:
    print("⚠️ UTF-8 解码失败，尝试使用 gb18030 编码读取...")
    data = pd.read_csv(data_file_path, encoding='gb18030')

# ----------------------------
# 检查列是否合法
# ----------------------------
if not {'id', 'Sentence', 'label'}.issubset(data.columns):
    print("❌ 数据集必须包含列名：id, Sentence, label")
    sys.exit()

# ----------------------------
# 预处理数据
# ----------------------------
tokens_list = [GeneSeg(sentence) for sentence in data['Sentence']]
sequences = tokenizer.texts_to_sequences(tokens_list)
padded_sequences = pad_sequences(sequences, maxlen=model.input_shape[1])

# ----------------------------
# 模型预测
# ----------------------------
predictions = model.predict(padded_sequences, verbose=0)
predicted_labels = (predictions > 0.5).astype(int).flatten()
true_labels = data['label'].astype(int).values

# ----------------------------
# 输出前20条预测结果
# ----------------------------
print("\n📢 前20条预测结果：")
for i, (idx, sentence, pred, label) in enumerate(zip(data['id'][:20], data['Sentence'][:20], predicted_labels[:20], true_labels[:20])):
    pred_text = "XSS攻击" if pred == 1 else "正常"
    real_text = "XSS攻击" if label == 1 else "正常"
    print(f"{i+1}. ID: {idx}  [预测: {pred_text}]  [实际: {real_text}] 内容: {sentence[:80]}...")

# ----------------------------
# 混淆矩阵 + 分类报告
# ----------------------------
cm = confusion_matrix(true_labels, predicted_labels)
print("\n📄 分类报告：\n")
print(classification_report(true_labels, predicted_labels, target_names=["正常", "XSS攻击"]))

plt.figure(figsize=(6, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["正常", "XSS攻击"], yticklabels=["正常", "XSS攻击"])
plt.title("混淆矩阵")
plt.xlabel("预测标签")
plt.ylabel("真实标签")
plt.tight_layout()

# ----------------------------
# 总体统计
# ----------------------------
total = len(predicted_labels)
count_attack = np.sum(predicted_labels)
count_normal = total - count_attack
print(f"\n✅ 总共预测 {total} 条请求：")
print(f"   - 预测为正常：{count_normal} 条")
print(f"   - 预测为 XSS 攻击：{count_attack} 条")
