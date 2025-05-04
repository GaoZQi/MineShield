import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import umap
from sklearn.cluster import AgglomerativeClustering
import numpy as np


class AgglomerativeClusteringPredict:
    def __init__(self, model_file, scaler_file, umap_file, test_data_path):
        self.model_file = model_file
        self.scaler_file = scaler_file
        self.umap_file = umap_file
        self.test_data_path = test_data_path
        self.agglomerative = None
        self.scaler = None
        self.umap = None
        self.X_test_scaled = None
        self.X_test_umap = None
        self.test_labels = None
        self.attack_type_mapping = {
            0: "Normal Traffic",
            1: "DoS Attack",
            2: "DoS Attack",
            3: "Probe Attack",
            4: "U2R Attack",
            5: "R2L Attack",
            6: "R2L Attack",
            7: "DoS Attack",
            8: "DoS Attack",
            9: "Probe Attack",
            10: "Probe Attack",
        }

    def load_model(self):
        """加载训练好的聚类模型、标准化器和UMAP模型"""
        self.agglomerative = joblib.load(self.model_file)
        self.scaler = joblib.load(self.scaler_file)
        self.umap = joblib.load(self.umap_file)

    def load_and_preprocess_data(self):
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

        # 修改映射：为每个攻击类型指定一个标签
        attack_type_mapping = {
            "normal.": 0,  # 正常流量
            "neptune.": 1,  # DoS攻击
            "smurf.": 2,  # DoS攻击
            "snmpgetattack.": 3,  # 探测攻击
            "warezmaster.": 4,  # U2R攻击
            "mailbomb.": 5,  # R2L攻击
            "guess_passwd.": 6,  # R2L攻击
            "back.": 7,  # DoS攻击
            "ftp_write.": 8,  # DoS攻击
            "imap.": 9,  # 探测攻击
            "satan.": 10,  # 探测攻击
        }

        # 这里将`attack_type`列的值替换为映射后的数值
        df["attack_type"] = (
            df["attack_type"].map(attack_type_mapping).fillna(-1)
        )  # 未知的攻击类型标记为-1

        # 将分类特征转换为数值型
        df["protocol_type"] = pd.Categorical(df["protocol_type"]).codes
        df["service"] = pd.Categorical(df["service"]).codes
        df["flag"] = pd.Categorical(df["flag"]).codes

        X = df.drop("attack_type", axis=1)

        # 标准化数据
        self.X_test_scaled = self.scaler.transform(X)

        # 使用UMAP进行降维
        self.X_test_umap = self.umap.transform(self.X_test_scaled)

    def predict_and_plot(self):
        """使用层次聚类进行预测并可视化结果"""
        # 使用层次聚类进行预测
        self.test_labels = self.agglomerative.fit_predict(self.X_test_umap)

        # 显示聚类结果
        unique_labels = set(self.test_labels)
        plt.figure(figsize=(10, 8))
        colormap = plt.cm.get_cmap("tab10", len(unique_labels))  # 获取色图

        for i, label in enumerate(unique_labels):
            color = colormap(i)  # 给每个簇分配不同颜色
            label_name = self.attack_type_mapping.get(
                label, "Unknown"
            )  # 获取对应的标签名称
            plt.scatter(
                self.X_test_umap[self.test_labels == label, 0],
                self.X_test_umap[self.test_labels == label, 1],
                color=color,
                label=f"{label_name}",
                alpha=0.7,
                s=40,
                edgecolors="black",
            )

        plt.title("Agglomerative Clustering on Test Set")
        plt.xlabel("UMAP Component 1")
        plt.ylabel("UMAP Component 2")
        plt.legend(loc="upper right", title="Cluster Labels")
        plt.show()


if __name__ == "__main__":
    model_file = "../../res/model/agglomerative_attack_detection_model.pkl"
    scaler_file = "../../res/model/agglomerative_scaler.pkl"
    umap_file = "../../res/model/agglomerative_umap.pkl"
    test_data_path = "../../res/data/ac_train"

    agglomerative_predict = AgglomerativeClusteringPredict(
        model_file=model_file,
        scaler_file=scaler_file,
        umap_file=umap_file,
        test_data_path=test_data_path,
    )

    # 加载模型和数据
    agglomerative_predict.load_model()
    agglomerative_predict.load_and_preprocess_data()

    # 预测并可视化
    agglomerative_predict.predict_and_plot()
