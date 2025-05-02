import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QStackedWidget,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from QSSLoader import QSSLoader
from dataMining import DataMiningTab
from attackDetection import AttackDetectionTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据挖掘与攻击检测展示系统")
        self.resize(900, 600)

        # 左侧树形导航
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setMaximumWidth(200)

        # 添加顶级节点
        datamine_item = QTreeWidgetItem(self.tree, ["数据挖掘"])
        preprocessing_item = QTreeWidgetItem(datamine_item, ["预处理"])
        feature_item = QTreeWidgetItem(datamine_item, ["特征工程"])
        model_item = QTreeWidgetItem(datamine_item, ["模型训练"])

        attack_item = QTreeWidgetItem(self.tree, ["攻击检测"])

        self.tree.expandItem(datamine_item)

        # 右侧堆栈页面
        self.stack = QStackedWidget()
        self.data_tab = DataMiningTab()
        self.attack_tab = AttackDetectionTab()
        # 可以扩展更多子页面
        self.stack.addWidget(self.data_tab)  # index 0
        self.stack.addWidget(self.attack_tab)  # index 1

        # 整体布局
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.tree)
        main_layout.addWidget(self.stack)
        self.setCentralWidget(central_widget)

        # 连接点击信号
        self.tree.itemClicked.connect(self.on_tree_item_clicked)

    def on_tree_item_clicked(self, item, column):
        text = item.text(column)
        if text == "数据挖掘":
            self.stack.setCurrentIndex(0)
            self.setWindowTitle("数据挖掘与攻击检测展示系统 - 数据挖掘")
        elif text == "攻击检测":
            self.stack.setCurrentIndex(1)
            self.setWindowTitle("数据挖掘与攻击检测展示系统 - 攻击检测")
        elif text in ["预处理", "特征工程", "模型训练"]:
            # 这里可以拓展 DataMiningTab 里的子切换逻辑
            self.stack.setCurrentIndex(0)
            self.data_tab.switch_to(text)  # 需要在 DataMiningTab 里实现这个方法
            self.setWindowTitle(f"数据挖掘与攻击检测展示系统 - {text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 12))
    style_file = "../style/main.qss"
    app.setStyleSheet(QSSLoader.read_qss_file(style_file))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
