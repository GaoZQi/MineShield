import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def cluster_titles_from_csv(csv_path, ax, canvas, n_clusters=4, encoding="utf-8"):
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans

    df = pd.read_csv(csv_path, encoding=encoding)
    titles = df["title"].dropna().astype(str).tolist()

    vectorizer = TfidfVectorizer()
    title_vectors = vectorizer.fit_transform(titles)

    pca = PCA(n_components=2)
    title_vectors_2d = pca.fit_transform(title_vectors.toarray())

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(title_vectors_2d)

    result_df = pd.DataFrame(title_vectors_2d, columns=["PC1", "PC2"])
    result_df.insert(0, "title", titles)
    result_df["cluster"] = labels

    # 清空之前的图
    ax.clear()
    # 画新图
    scatter = ax.scatter(
        result_df["PC1"],
        result_df["PC2"],
        c=result_df["cluster"],
        cmap="viridis",
        alpha=0.7,
        edgecolors="black",
        linewidths=0.5,
    )
    ax.set_title("Title Dimensionality Reduction + Clustering Result (PCA + KMeans)")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.grid(True)
    # 刷新画布
    canvas.draw()


if __name__ == "__main__":
    # 示例：使用示例CSV文件进行聚类
    result_df = cluster_titles_from_csv(
        "../../res/data/Dimensionality_Reduction/result.csv",
        n_clusters=4,
        encoding="utf-8",
    )
    print(result_df.head())
