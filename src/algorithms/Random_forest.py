import pandas as pd
import joblib
import os
import chardet
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
)
import umap.umap_ as umap
import warnings

# 静音 UMAP 警告
warnings.filterwarnings("ignore", category=UserWarning)


class RandomForestPredictor:
    def __init__(self, file_path, ax, canvas, model_dir="../res/model/Random_forest"):
        self.model_dir = model_dir
        self.model = joblib.load(os.path.join(model_dir, "Random_Forest_model.pkl"))
        self.vectorizer = joblib.load(
            os.path.join(model_dir, "Random_Forest_Tfidf_Vectorizer.pkl")
        )
        self.label_encoder = joblib.load(
            os.path.join(model_dir, "Random_Forest_Label_Encoder.pkl")
        )
        self.run(file_path, ax, canvas)

    def read_csv_safely(self, path):
        with open(path, "rb") as f:
            result = chardet.detect(f.read(5000))
        encoding = result["encoding"]
        print(f"File encoding detected: {encoding}")
        return pd.read_csv(path, encoding=encoding).dropna()

    def plot_confusion_matrix(self, y_true, y_pred, ax, canvas):
        cm = confusion_matrix(
            y_true, y_pred, labels=range(len(self.label_encoder.classes_))
        )
        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=[str(c) for c in self.label_encoder.classes_],
        )
        disp.plot(cmap="Blues", ax=ax, colorbar=True)
        ax.set_title("Confusion Matrix: True vs Predicted")
        plt.tight_layout()
        canvas.draw()

    def plot_umap_scatter(self, X, y_pred, ax, canvas):
        reducer = umap.UMAP(n_components=2)  # 不设置 random_state
        X_umap = reducer.fit_transform(X.toarray())
        df_umap = pd.DataFrame(X_umap, columns=["UMAP1", "UMAP2"])
        df_umap["Label"] = self.label_encoder.inverse_transform(y_pred)

        sns.scatterplot(
            data=df_umap, x="UMAP1", y="UMAP2", hue="Label", palette="tab10", s=30
        )
        ax.set_title("UMAP Scatter Plot (Colored by Predicted Label)")
        plt.tight_layout()
        canvas.show()

    def predict_and_visualize(self, test_csv_path, ax, canvas):
        df = self.read_csv_safely(test_csv_path)
        df["text"] = df["Title"] + " " + df["Description"]
        X_test = self.vectorizer.transform(df["text"])
        y_pred = self.model.predict(X_test)

        # 分类报告 + 可视化
        # if "Class Index" in df.columns:
        #     y_true = self.label_encoder.transform(df["Class Index"])
        #     class_names = [str(c) for c in self.label_encoder.classes_]
        #     report = classification_report(
        #         y_true, y_pred, target_names=class_names, digits=4
        #     )
        #     print("Classification Report:\n")
        #     print(report)
        #     self.plot_confusion_matrix(y_true, y_pred, ax, canvas)
        # else:
        #     print(
        #         "No 'Class Index' column found. Skipping classification report and confusion matrix."
        #     )

        print("📡 Generating UMAP scatter plot... Please wait.")
        self.plot_umap_scatter(X_test, y_pred, ax, canvas)

    def run(self, file_path, ax, canvas):
        # 运行预测和可视化
        self.predict_and_visualize(file_path, ax, canvas)


if __name__ == "__main__":

    model_dir = "../../res/model/Random_forest"

    # === 预测部分 ===
    print(
        "\n请输入测试集 CSV 文件路径（例如 train/data/Random_forest_data/Random_forest_test.csv）："
    )
    test_path = input("测试文件路径: ").strip()

    predictor = RandomForestPredictor(model_dir)
    predictor.predict_and_visualize(test_path)
