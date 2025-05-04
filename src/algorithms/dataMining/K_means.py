import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer


class KMeansTextClustering:
    def __init__(self, file_path, ax, canvas, n_clusters=5, max_features=1000):
        """
        初始化类，自动加载停用词表。
        """
        self.n_clusters = n_clusters
        self.max_features = max_features
        self.vectorizer = TfidfVectorizer(
            stop_words="english", max_features=max_features
        )
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.pca = PCA(n_components=2, random_state=42)
        self.stop_words_set = self._load_stop_words()
        self.run(file_path, ax, canvas)

    def _load_stop_words(self):
        """
        内置英文停用词集合
        """
        return set(
            [
                "the",
                "and",
                "is",
                "in",
                "to",
                "of",
                "that",
                "with",
                "for",
                "on",
                "this",
                "at",
                "by",
                "an",
                "be",
                "are",
                "from",
                "as",
                "or",
                "was",
                "but",
                "not",
                "it",
                "a",
                "has",
                "have",
                "will",
                "can",
                "could",
                "would",
                "should",
                "may",
                "might",
                "about",
                "after",
                "before",
                "more",
                "most",
                "up",
                "out",
                "over",
                "under",
                "while",
                "just",
                "some",
                "one",
                "all",
                "new",
                "us",
                "you",
                "we",
                "they",
                "i",
                "he",
                "she",
                "his",
                "her",
                "their",
                "them",
                "our",
                "your",
                "its",
                "also",
                "like",
                "said",
                "say",
                "says",
                "get",
                "got",
                "make",
                "made",
                "now",
                "still",
                "see",
                "watch",
                "show",
                "video",
                "report",
                "news",
                "take",
                "check",
                "read",
                "click",
                "want",
                "know",
                "find",
                "go",
                "look",
                "come",
                "back",
                "use",
                "give",
                "keep",
                "need",
                "think",
                "let",
                "help",
                "turn",
                "tell",
                "update",
                "view",
                "work",
                "worked",
                "works",
                "what",
                "off",
                "into",
                "onto",
                "upon",
                "across",
                "along",
                "around",
                "through",
                "without",
                "within",
                "than",
                "then",
                "when",
                "where",
                "how",
                "why",
                "who",
                "whom",
                "which",
                "whose",
            ]
        )

    def load_data(self, file_path):
        df = pd.read_csv(file_path)
        if "title" not in df.columns:
            raise ValueError("文件中缺少 'title' 列")
        titles = df["title"].dropna().astype(str).tolist()
        if len(titles) < 5:
            raise ValueError("文本数据不足，至少需要5条以上记录")
        return titles

    def fit(self, texts):
        X = self.vectorizer.fit_transform(texts)
        labels = self.kmeans.fit_predict(X)
        reduced = self.pca.fit_transform(X.toarray())
        return labels, reduced, X.toarray()

    def show_clusters(self, reduced_data, labels, ax, canvas):
        ax.clear()
        scatter = ax.scatter(
            reduced_data[:, 0],
            reduced_data[:, 1],
            c=labels,
            cmap="tab10",
            s=50,
            edgecolors="black",
            linewidths=0.5,
            alpha=0.7,
        )
        ax.set_title("K-Means Clustering")
        ax.set_xlabel("PCA Component 1")
        ax.set_ylabel("PCA Component 2")
        ax.grid(True)
        plt.colorbar(scatter, ax=ax, label="Cluster ID")
        canvas.draw()

    def run(self, file_path, ax, canvas):
        print(f"\nProcessing file: {file_path}")
        texts = self.load_data(file_path)
        labels, reduced, _ = self.fit(texts)
        self.show_clusters(reduced, labels, ax, canvas)
