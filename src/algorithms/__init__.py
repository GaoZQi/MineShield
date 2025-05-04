import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from algorithms.dataMining.Dimensionality_Reduction import (
    cluster_titles_from_csv as DimensionalityReduction,
)
from algorithms.dataMining.Linear_Regression import (
    predict_content_length_from_csv as LinearRegression,
)
from algorithms.dataMining.K_means import KMeansTextClustering as Kemeans
from algorithms.dataMining.Random_forest import (
    RandomForestPredictor as RandomForest,
)
from algorithms.dataMining.Isolation_Forest import (
    run_isolation_forest as IsolationForest,
)
from algorithms.dataMining.Apriori import run as Apriori
from algorithms.dataMining.PCA import plot_pca_scatter as PCA


from algorithms.dataMining.GMM import (
    GMMClustering as GMM,
)

from algorithms.dataMining.Agglomerative_Clustering import (
    AgglomerativeClusteringPredict as AgglomerativeClustering,
)

from algorithms.dataMining.Bayes import naive_bayes_classifier as Bayes

from algorithms.dataMining.Decision_Tree import (
    decision_tree_classifier_chinese as DecisionTree,
)
