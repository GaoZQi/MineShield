import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from random import randint
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA


class MilitaryTextClassifier:
    def __init__(self, file_path, ax, canvas, test_size=0.2, max_features=500):
        self.test_size = test_size
        self.max_features = max_features
        self.label_encoder = LabelEncoder()
        self.vectorizer = TfidfVectorizer(
            max_features=max_features, stop_words="english"
        )
        self.model = RandomForestClassifier(n_estimators=100)
        self.random_seed = randint(0, 999999)

        self.military_map = {
            "drone": "Drone",
            "uav": "Drone",
            "unmanned": "Drone",
            "quadcopter": "Drone",
            "mq-9": "Drone",
            "reaper": "Drone",
            "global hawk": "Drone",
            "loyal wingman": "Drone",
            "ucav": "Drone",
            "suicide drone": "Drone",
            "kamikaze drone": "Drone",
            "missile": "Missile",
            "ballistic": "Missile",
            "interceptor": "Missile",
            "cruise missile": "Missile",
            "hypersonic": "Missile",
            "silo": "Missile",
            "warhead": "Missile",
            "launch vehicle": "Missile",
            "air force": "Air Force",
            "fighter": "Air Force",
            "jet": "Air Force",
            "stealth": "Air Force",
            "f-16": "Air Force",
            "f-35": "Air Force",
            "f-22": "Air Force",
            "bomber": "Air Force",
            "airstrike": "Air Force",
            "navy": "Navy",
            "warship": "Navy",
            "destroyer": "Navy",
            "frigate": "Navy",
            "submarine": "Navy",
            "aircraft carrier": "Navy",
            "carrier strike group": "Navy",
            "army": "Army",
            "tank": "Army",
            "infantry": "Army",
            "ground": "Army",
            "combat": "Army",
            "brigade": "Army",
            "platoon": "Army",
            "artillery": "Army",
            "radar": "Other",
            "sonar": "Other",
            "sensor": "Other",
            "laser": "Other",
            "jamming": "Other",
            "tracking system": "Other",
            "defense": "Defense Systems",
            "air defense": "Defense Systems",
            "iron dome": "Defense Systems",
            "patriot": "Defense Systems",
            "s-400": "Defense Systems",
            "s-300": "Defense Systems",
            "aegis": "Defense Systems",
            "missile shield": "Defense Systems",
            "anti-air": "Defense Systems",
        }
        self.run(file_path, ax, canvas)

    def load_and_prepare_data(self, file_path):
        df = pd.read_csv(file_path)
        print(f"\n✅ 数据读取完成，共 {len(df)} 条新闻。")

        self.military_map = {k.lower(): v for k, v in self.military_map.items()}
        df["military_subcategory"] = (df["title"] + " " + df["content"]).apply(
            lambda text: next(
                (v for k, v in self.military_map.items() if k in str(text).lower()),
                "Other",
            )
        )
        return df

    def run(self, file_path, ax, canvas):
        df = self.load_and_prepare_data(file_path)

        X_text = df["title"] + " " + df["content"]
        X = self.vectorizer.fit_transform(X_text).toarray()
        y = self.label_encoder.fit_transform(df["military_subcategory"])

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_seed
        )

        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X)

        # PCA降维到2D
        pca = PCA(n_components=2, random_state=42)
        reduced_X = pca.fit_transform(X)

        # 散点图
        scatter = ax.scatter(
            reduced_X[:, 0],
            reduced_X[:, 1],
            c=y_pred,
            cmap="tab10",
            s=50,
            edgecolors="black",
            linewidths=0.5,
            alpha=0.7,
        )
        ax.set_title("Military Text Classification (PCA 2D)")
        ax.set_xlabel("PCA Component 1")
        ax.set_ylabel("PCA Component 2")
        ax.grid(True)
        plt.colorbar(scatter, ax=ax, label="Predicted Category")
        canvas.draw()

        # 控制台输出报告
        target_names = self.label_encoder.inverse_transform(
            sorted(set(y) | set(y_pred))
        )
        print("\n📊 全部数据分类报告：\n")
        print(classification_report(y, y_pred, target_names=target_names))
