import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import networkx as nx
import matplotlib.pyplot as plt


def draw_rule_graph(rules, ax, canva, top_n=20):
    G = nx.DiGraph()
    for i, row in rules.head(top_n).iterrows():
        rule_node = f"R{i}"
        G.add_node(rule_node, color="yellow")
        for a in row["antecedents"]:
            G.add_node(a, color="lightgreen")
            G.add_edge(a, rule_node)
        for c in row["consequents"]:
            G.add_node(c, color="lightgreen")
            G.add_edge(rule_node, c)

    colors = [data["color"] for _, data in G.nodes(data=True)]
    pos = nx.spring_layout(G, k=0.5, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=500, arrowsize=12)
    ax.set_title(f"Association Rules Graph (top {top_n})")
    canva.draw()


def draw_bubble_chart(rules, ax, canva):
    # rules 是 association_rules() 返回的 DataFrame
    x = rules["support"]
    y = rules["confidence"]
    sizes = rules["lift"] * 20  # 根据 lift 放大气泡
    colors = rules["lift"]  # 也可映射颜色
    scatter = ax.scatter(x, y, s=sizes, c=colors, alpha=0.6)
    ax.set_xlabel("Support")
    ax.set_ylabel("Confidence")
    ax.set_title("Support vs Confidence (bubble size/color ~ Lift)")
    cbar = plt.colorbar(scatter)
    cbar.set_label("Lift")
    canva.draw()
    # plt.grid(True)
    # plt.show()


def run(file_path, ax, canva):
    # 读取卖菜交易数据集
    df = pd.read_csv(file_path)

    # 使用Apriori算法生成频繁项集，设定最小支持度为0.5
    frequent_itemsets = apriori(
        df.drop(columns="Transaction ID"), min_support=0.5, use_colnames=True
    )

    # 生成关联规则，设定最小提升度为1
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

    # 查看频繁项集和关联规则
    print("频繁项集:")
    print(frequent_itemsets)

    print("\n关联规则:")
    print(rules)

    # 可视化关联规则图
    draw_rule_graph(rules, ax, canva, top_n=20)
    # draw_bubble_chart(rules, ax, canva)


if __name__ == "__main__":
    # 读取卖菜交易数据集
    df = pd.read_csv("../../res/data/Apriori/vegetable_transactions.csv")

    # 使用Apriori算法生成频繁项集，设定最小支持度为0.5
    frequent_itemsets = apriori(
        df.drop(columns="Transaction ID"), min_support=0.5, use_colnames=True
    )

    # 生成关联规则，设定最小提升度为1
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

    # 查看频繁项集和关联规则
    print("频繁项集:")
    print(frequent_itemsets)

    print("\n关联规则:")
    print(rules)

    # 可视化关联规则图
    fig, ax = plt.subplots(figsize=(10, 6))
    draw_rule_graph(rules, ax, plt, top_n=20)
    plt.show()
