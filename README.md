# 接口文档

## 1.zsy

### 1.1 Dimensionality Reduction

```python
#数据集读取部分，传入csv的文件路径
df = pd.read_csv(csv_path, encoding=encoding)

#可视化部分代码，唯一输出
    plt.figure(figsize=(8, 6))
    plt.scatter(
        result_df["PC1"],
        result_df["PC2"],
        c=result_df["cluster"],
        cmap='viridis',
        alpha=0.7,
        edgecolors='black',
        linewidths=0.5
    )
    plt.title("Title Dimensionality Reduction + Clustering Result (PCA + KMeans)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.grid(True)
    plt.show()
```

### 1.2 Linear_Regression

```python
#数据集读取部分
df = pd.read_csv(csv_path, encoding=encoding)

#输出部分，先构建DataFrame和均方误差MSE
result_df = pd.DataFrame({
    "True Length": y_test.values,
    "Predicted Length": y_pred.round(2)
})
result_df["Error"] = (result_df["True Length"] - result_df["Predicted Length"]).abs().round(2)
#再打印出MSE
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error (MSE):", round(mse, 2))
#最后生成可视化散点图
plt.scatter(range(len(y_test)), y_test, label="True", color="blue")
plt.scatter(range(len(y_pred)), y_pred, label="Predicted", color="orange")
```

### 1.3 SQLDetectModel

```python
#代码中写死的调用位置
class SQLDetectModel:
    def __init__(self, model_pkl="../model/xgboost_model.pkl", le_pkl="../model/sqllabel_encoder.pkl", vectorizer_pkl="../model/vectorizer.pkl"):
#日志读取逻辑
log_path = input("请输入日志文件路径：")
	def process_log_and_predict(log_path, model):

#所有的输出信息
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
```

## 2.cwc

### 2.1 ac_predict

```python
#模型文件的读取
model_file = '../model/agglomerative_attack_detection_model.pkl'
    scaler_file = '../model/agglomerative_scaler.pkl'
    umap_file = '../model/agglomerative_umap.pkl'
    test_data_path = '../dataset/ac_train'
agglomerative_predict = AgglomerativeClusteringPredict(model_file=model_file, scaler_file=scaler_file, umap_file=umap_file, test_data_path=test_data_path)

#打印可视化聚类成果
plt.scatter(self.X_test_umap[self.test_labels == label, 0], self.X_test_umap[self.test_labels == label, 1],
            color=color, label=f"{label_name}", alpha=0.7, s=40, edgecolors='black')
#图表输出
plt.title("Agglomerative Clustering on Test Set")
plt.xlabel("UMAP Component 1")
plt.ylabel("UMAP Component 2")
plt.legend(loc='upper right', title='Cluster Labels')
plt.show()
```

### 2.2 gmm_predict

```python
#相同的读取逻辑
model_file = '../model/gmm_attack_detection_model.pkl'
    scaler_file = '../model/gmm_scaler.pkl'
    umap_file = '../model/gmm_umap.pkl'
    test_data_path = '../dataset/kddcup.data_10_percent_corrected'

    gmm_clustering = GMMClustering(model_file=model_file, scaler_file=scaler_file, umap_file=umap_file, test_data_path=test_data_path)

#plt绘制图形输出
# 创建一个图形并分配不同的颜色
plt.figure(figsize=(10, 8))

# 为每个簇分配不同的颜色和标记，增加透明度和点的大小
for cluster_id in np.unique(self.test_labels):
  plt.scatter(self.X_test_umap[self.test_labels == cluster_id, 0],
    self.X_test_umap[self.test_labels == cluster_id, 1],
    label=cluster_names[cluster_id], alpha=0.7, s=30, edgecolors='black', marker='o')
# 添加标签和标题
plt.title("GMM Clustering on Test Set")
plt.xlabel("UMAP Component 1")
plt.ylabel("UMAP Component 2")
plt.legend()
# 显示图形
plt.show()
```

### 2.3 mlp_predict

```python
#照常传入模型文件
mlp_model_path = '../model/mlp_model_trained.pkl'
    keras_model_path = '../model/keras_mlp_model_trained.keras'
    onehot_encoder_path = '../model/onehot_encoder.pkl'
    scaler_path = '../model/scaler.pkl'

    predictor = ModelPredictor(mlp_model_path=mlp_model_path, keras_model_path=keras_model_path, onehot_encoder_path=onehot_encoder_path, scaler_path=scaler_path)

#测试集样例，写死了并输出预测结果
sample = "51213,0.999352,tcp,http,FIN,10,10,800,1190,19.01232,62,252,5763.734863,8573.555664,2,2,111.039111,98.288445,6662.074451,165.358922,255,1472115402,1201817275,255,0.288347,0.114102,0.174245,80,119,1,149,5,1,2,2,1,5,0,0,1,2,5,0,Analysis,1"

	# 进行预测并输出结果
    result = predictor.predict(sample)
    print(result)

#实际输入的测试集路径
    test_data_path = '../dataset/UNSW_NB15_testing-set.csv'  # 替换为测试集路径
    predictor.evaluate(test_data_path)
    # 计算准确率的实际输出类型
    from sklearn.metrics import accuracy_score
    accuracy_mlp = accuracy_score(y_test, y_pred_mlp)
    accuracy_keras = accuracy_score(y_test, y_pred_keras)

    print(f"MLP Classifier Accuracy: {accuracy_mlp:.4f}")
    print(f"Keras Model Accuracy: {accuracy_keras:.4f}")
```

## 3.cyq

### 3.1 K_means

```python
#输入文件
print(f"\nProcessing file: {file_path}")
texts = self.load_data(file_path)
    def load_data(self, file_path):
        df = pd.read_csv(file_path)
        if 'title' not in df.columns:
            raise ValueError("文件中缺少 'title' 列")
        titles = df['title'].dropna().astype(str).tolist()
        if len(titles) < 5:
            raise ValueError("文本数据不足，至少需要5条以上记录")
        return titles
    
#输出的图表
def show_clusters(self, reduced_data, labels):
        plt.figure(figsize=(14, 8))
        plt.scatter(
            reduced_data[:, 0], reduced_data[:, 1],
            c=labels, cmap='tab10', s=50,
            edgecolors='black', linewidths=0.5, alpha=0.7
        )
        plt.title("K-Means Clustering")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.grid(True)
        plt.colorbar(label='Cluster ID')
        plt.tight_layout()
        plt.show()

def show_wordcloud(self, texts):
        all_text = " ".join(texts)
        cleaned_text = re.sub(r'\b[a-zA-Z]\b', '', all_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        wordcloud = WordCloud(
            width=1000, height=500,
            background_color='white',
            stopwords=self.stop_words_set,
            max_words=100
        ).generate(cleaned_text)

        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title("Word Cloud")
        plt.tight_layout()
        plt.show()
        
def print_top_keywords(self, X_dense, labels):
        for cluster_id in range(self.n_clusters):
            cluster_indices = [i for i, label in enumerate(labels) if label == cluster_id]
            if not cluster_indices:
                print(f"Cluster {cluster_id}: (empty)")
                continue
            cluster_tfidf_avg = X_dense[cluster_indices].mean(axis=0)
            print(f"Cluster {cluster_id} → {top_keywords}")
```

### 3.2 One_Class_SVM_predict

```python
#各预测数输出
        print("\n预测结果:")
        print(f"预测总数据量: {total}")
        print(f"预测正常流量数: {normal_count}")
        print(f"预测异常流量数: {attack_count}")
        
#结果输出函数与输出
    def evaluate(self, y_true, y_pred):
        print("One-Class SVM Intrusion Detection Report:")
        print(classification_report(y_true, y_pred, target_names=['Attack', 'Normal']))

        cm = confusion_matrix(y_true, y_pred, labels=[1, -1])
        print("\nConfusion Matrix:")
        print(cm)
	self.evaluate(y_true, y_pred)
```

### 3.3 Random_forest_predict

```python
#预测与可视化输出
def predict_and_visualize(self, test_csv_path):
        df = self.read_csv_safely(test_csv_path)
        df['text'] = df['Title'] + ' ' + df['Description']
        X_test = self.vectorizer.transform(df['text'])
        y_pred = self.model.predict(X_test)

        # 分类报告 + 可视化
        if 'Class Index' in df.columns:
            y_true = self.label_encoder.transform(df['Class Index'])
            class_names = [str(c) for c in self.label_encoder.classes_]
            report = classification_report(y_true, y_pred, target_names=class_names, digits=4)
            print("Classification Report:\n")
            print(report)
            self.plot_confusion_matrix(y_true, y_pred)
        else:
            print("No 'Class Index' column found. Skipping classification report and confusion matrix.")

        print("📡 Generating UMAP scatter plot... Please wait.")
        
#plot_umap_scatter的输出
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df_umap, x='UMAP1', y='UMAP2', hue='Label', palette='tab10', s=30)
        plt.title("UMAP Scatter Plot (Colored by Predicted Label)")
        plt.tight_layout()
        plt.show()
        
#plot_confusion_matrix的输出
        fig, ax = plt.subplots(figsize=(8, 6))
        disp.plot(cmap="Blues", ax=ax, colorbar=True)
        plt.title("Confusion Matrix: True vs Predicted")
        plt.tight_layout()
        plt.show()
```

