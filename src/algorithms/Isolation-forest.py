import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
import os

# 1. 加载模型和标准化器
with open('../../res/model/isolation_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('../../res/model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

test_path = input("请输入测试集 CSV 文件路径: ").strip()
if not os.path.exists(test_path):
    print("错误：文件路径不存在！")
df_test = pd.read_csv(test_path)

# 3. 特征选择
features = ['duration', 'src_bytes', 'dst_bytes', 'wrong_fragment', 'urgent']
X_test = df_test[features]
X_scaled_test = scaler.transform(X_test)

# 4. 预测（1表示正常，-1表示异常）
predictions = model.predict(X_scaled_test)

# 5. 输出预测结果
df_test['prediction'] = predictions
df_test['attack_type'] = df_test['prediction'].apply(lambda x: 'PortScan' if x == -1 else 'Normal')

# 显示完整预测结果
print(df_test[['prediction', 'attack_type']].to_string())

print("预测完成，完整结果已显示。")
