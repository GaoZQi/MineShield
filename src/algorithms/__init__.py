import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from Dimensionality_Reduction import cluster_titles_from_csv as DimensionalityReduction
from Linear_Regression import predict_content_length_from_csv as LinearRegression
from K_means import KMeansTextClustering as Kemeans
from Random_forest import RandomForestPredictor as RandomForest


# def RandomForest(): ...
def IsolationForest(filepath, ax, canva): ...


from Apriori import run as Apriori
from PCA import plot_pca_scatter as PCA


# def PCA(filepath, ax, canva): ...
def GMM(filepath, ax, canva): ...
def AgglomerativeClustering(filepath, ax, canva): ...


from Bayes import naive_bayes_classifier as Bayes

from Decision_Tree import decision_tree_classifier_chinese as DecisionTree
