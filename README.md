# MineShield

一款展示常见数据挖掘算法和攻击检测方法的可视化工具，旨在帮助用户理解数据挖掘算法的工作原理和应用场景。该工具提供了多种数据挖掘算法的实现，包括分类、聚类、关联规则挖掘等，并通过可视化界面展示算法的运行过程和结果。同时，MineShield 还集成了一些常见的攻击检测方法，帮助用户识别和防范潜在的安全威胁。

## 环境要求

Python 版本要求为 3.10，推荐使用虚拟环境（如 venv 或 conda）来管理依赖。

运行下面指令安装依赖：

```
pip install -r requirements.txt
```

## 使用方法

### 数据挖掘

点击算法信息右侧图标切换数据挖掘算法。

![step1](assets/image-11.png)

点击选择数据集，选择本地数据集。

![step2](assets/image-12.png)

选择数据集后，点击“开始”按钮，开始运行数据挖掘算法。

![step3](assets/image-13.png)

### 攻击检测

点击左侧功能列表选择攻击检测方法。

![step1](assets/image-14.png)

点击选择文件，上传本地文件。

![step2](assets/image-15.png)

点击开始检测按钮，开始运行攻击检测方法。

![step3](assets/image-16.png)

部分功能支持才输入框输入数据，点击左侧按钮进行检测。

![step4](assets/image-19.png)

## 界面展示

### 数据挖掘算法

-   Dimensionalit Reduction
    ![Dimensionalit Reduction](assets/image.png)
-   Linear Regression
    ![Linear Regression](assets/image-1.png)
-   K-Means
    ![K-Means](assets/image-2.png)
-   Random Forest
    ![Random Forest](assets/image-3.png)
-   Isolation Forest
    ![Isolation Forest](assets/image-4.png)
-   Apriori
    ![Apriori](assets/image-5.png)
-   PCA
    ![PCA](assets/image-6.png)
-   GMM
    ![GMM](assets/image-7.png)
-   Agglomerative Clustering
    ![Agglomerative Clustering](assets/image-8.png)
-   Bayes
    ![Bayest](assets/image-9.png)
-   Decision Tree
    ![Decision Tree](assets/image-10.png)

### 攻击检测方法

-   日志检测自动化 SQL 注入
    ![XGBoost](assets/image-17.png)
-   恶意 URL 请求检测
    ![Logistics Regression](assets/image-25.png)
-   恶意邮件检测
    ![SVM](assets/image-18.png)
-   恶意扫描数据包检测
    ![KNN](assets/image-20.png)
-   DDoS 攻击检测
    ![梯度提升树](assets/image-21.png)
-   IDS 入侵检测
    ![One-Class SVM](assets/image-22.png)
-   恶意数据包检测
    ![MLP](assets/image-23.png)
-   端口扫描攻击检测
    ![Isolation Forest](assets/image-24.png)
-   SQL 注入攻击检测
    ![SVM](assets/image-26.png)
-   XSS 攻击检测
    ![LSTM](assets/image-27.png)
