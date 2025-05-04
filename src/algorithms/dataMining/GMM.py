import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.mixture import GaussianMixture
import pandas as pd


class GMMClustering:
    def __init__(
        self,
        test_data_path,
        ax,
        canvas,
        model_file="../res/model/GMM/gmm_attack_detection_model.pkl",
        scaler_file="../res/model/GMM/gmm_scaler.pkl",
        umap_file="../res/model/GMM/gmm_umap.pkl",
    ):
        self.model_file = model_file
        self.scaler_file = scaler_file
        self.umap_file = umap_file
        self.test_data_path = test_data_path
        self.model = None
        self.scaler = None
        self.umap = None
        self.X_test_scaled = None
        self.X_test_umap = None
        self.test_labels = None

        self.run(ax, canvas)

    def load_model(self):
        """加载训练好的 GMM 模型、标准化器和UMAP模型"""
        self.model = joblib.load(self.model_file)
        self.scaler = joblib.load(self.scaler_file)
        self.umap = joblib.load(self.umap_file)  # 加载UMAP模型

    def load_and_preprocess_data(self):
        """加载并预处理测试数据"""
        column_names = [
            "duration",
            "protocol_type",
            "service",
            "flag",
            "src_bytes",
            "dst_bytes",
            "land",
            "wrong_fragment",
            "urgent",
            "hot",
            "num_failed_logins",
            "logged_in",
            "num_compromised",
            "root_shell",
            "su_attempted",
            "num_root",
            "num_file_creations",
            "num_shells",
            "num_access_files",
            "num_outbound_cmds",
            "is_hot_login",
            "is_guest_login",
            "count",
            "srv_count",
            "serror_rate",
            "srv_serror_rate",
            "rerror_rate",
            "srv_rerror_rate",
            "same_srv_rate",
            "diff_srv_rate",
            "srv_diff_host_rate",
            "dst_host_count",
            "dst_host_srv_count",
            "dst_host_same_srv_rate",
            "dst_host_diff_srv_rate",
            "dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate",
            "dst_host_serror_rate",
            "dst_host_srv_serror_rate",
            "dst_host_rerror_rate",
            "dst_host_srv_rerror_rate",
            "attack_type",
        ]

        df = pd.read_csv(self.test_data_path, header=None, names=column_names)
        df["attack_type"] = df["attack_type"].apply(
            lambda x: 0 if x == "normal." else 1
        )

        # 将分类特征转换为数值型
        df["protocol_type"] = pd.Categorical(df["protocol_type"]).codes
        df["service"] = pd.Categorical(df["service"]).codes
        df["flag"] = pd.Categorical(df["flag"]).codes

        X = df.drop("attack_type", axis=1)

        # 标准化数据
        self.X_test_scaled = self.scaler.transform(X)

        # 使用训练时的UMAP模型进行降维
        self.X_test_umap = self.umap.transform(self.X_test_scaled)

    def predict_and_plot(self, ax, canvas):
        ax.clear()
        """使用 GMM 进行聚类预测并可视化结果"""
        # 使用 GMM 进行预测
        self.test_labels = self.model.predict(self.X_test_umap)

        # 为每个簇分配实际意义的名称
        cluster_names = {
            0: "Normal Traffic",  # Cluster 0: Normal Traffic
            1: "DoS Attack",  # Cluster 1: DoS Attack
            2: "Probe Attack",  # Cluster 2: Probe Attack
            3: "R2L Attack",  # Cluster 3: R2L Attack
            4: "U2R Attack",  # Cluster 4: U2R Attack
        }

        # 创建一个图形并分配不同的颜色

        # 为每个簇分配不同的颜色和标记，增加透明度和点的大小
        for cluster_id in np.unique(self.test_labels):
            ax.scatter(
                self.X_test_umap[self.test_labels == cluster_id, 0],
                self.X_test_umap[self.test_labels == cluster_id, 1],
                label=cluster_names[cluster_id],
                alpha=0.7,
                s=30,
                edgecolors="black",
                marker="o",
            )

        # 添加标签和标题
        ax.set_title("GMM Clustering on Test Set")
        ax.set_xlabel("UMAP Component 1")
        ax.set_ylabel("UMAP Component 2")
        ax.legend()

        # 显示图形
        canvas.draw()

    def run(self, ax, canvas):
        # 创建 GMMClustering 实例
        # 加载模型和数据
        self.load_model()
        self.load_and_preprocess_data()

        # 预测并可视化
        self.predict_and_plot(ax, canvas)


if __name__ == "__main__":
    test_data_path = "../../../res/data/7 GMM/kddcup.data_10_percent_corrected.csv"
    model_file = "../../../res/model/GMM/gmm_attack_detection_model.pkl"
    scaler_file = "../../../res/model/GMM/gmm_scaler.pkl"
    umap_file = "../../../res/model/GMM/gmm_umap.pkl"

    gmm = GMMClustering(
        test_data_path=test_data_path,
        model_file=model_file,
        scaler_file=scaler_file,
        umap_file=umap_file,
    )
