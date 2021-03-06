#!/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
"""
利用决策树，根据鸢尾花数据集中的两个特征，实现三分类
"""

def iris_type(s):
    it = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    return it[s]


# 花萼长度、花萼宽度，花瓣长度，花瓣宽度
# iris_feature = 'sepal length', 'sepal width', 'petal length', 'petal width'
iris_feature = u'花萼长度', u'花萼宽度', u'花瓣长度', u'花瓣宽度'

if __name__ == "__main__":
    # 设置图像的中文字体
    mpl.rcParams['font.sans-serif'] = "Times New Roman"
    mpl.rcParams['axes.unicode_minus'] = False

    # 1. 利用pandas加载数据集
    path = 'iris.data'  # 数据文件路径
    data = pd.read_csv(path, names=["sepal-length", "sepal-width",
                                     "petal-length", "petal-width", "label"])
    # 1.1 为了便于处理数据，将label标记为int型数据
    data["label"] = pd.Categorical(data["label"]).codes

    # 1.2 为了可视化，仅使用花萼长度和花瓣长度作为特征
    x = np.array(data[["sepal-length", "petal-width"]])
    y = np.array(data["label"])
    
    # 1.3 划分数据集
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.3, random_state=1)

    # 2. 决策树模型拟合
    # min_samples_split = 10：如果该结点包含的样本数目大于10，则(有可能)对其分支
    # min_samples_leaf = 10：若将某结点分支后，得到的每个子结点样本数目都大于10，则完成分支；否则，不进行分支
    model = Pipeline([
        ('ss', StandardScaler()),
        ('DTC', DecisionTreeClassifier(criterion='entropy', max_depth=3))])
    # clf = DecisionTreeClassifier(criterion='entropy', max_depth=3)
    model = model.fit(x_train, y_train)
    y_test_hat = model.predict(x_test)      # 测试数据

    # 保存决策树结果图
    # dot -Tpng -o 1.png 1.dot
    # f = open('.\\iris_tree.dot', 'w')
    # tree.export_graphviz(model.get_params('DTC')['DTC'], out_file=f)
    # f.close()
    
    # 3. 决策边界可视化
    N, M = 100, 100  # 横纵各采样多少个值
    x1_min, x1_max = x[:, 0].min(), x[:, 0].max()  # 第0列的范围
    x2_min, x2_max = x[:, 1].min(), x[:, 1].max()  # 第1列的范围
    t1 = np.linspace(x1_min, x1_max, N)
    t2 = np.linspace(x2_min, x2_max, M)
    # x1按行重复M次，x2按列重复N次，x1和x2都是M行N列。
    x1, x2 = np.meshgrid(t1, t2)  # 生成网格采样点
    # 按行展开，然后按列拼在一起，得到10000对数据点
    x_show = np.stack((x1.flat, x2.flat), axis=1)  # 测试点
    print(x_show.shape)

    # 4. 预测
    y_show_hat = model.predict(x_show)  # 预测值
    
    # # 无意义，只是为了凑另外两个维度
    # # 打开该注释前，确保注释掉x = x[:, :2]
    # x3 = np.ones(x1.size) * np.average(x[:, 2])
    # x4 = np.ones(x1.size) * np.average(x[:, 3])
    # x_test = np.stack((x1.flat, x2.flat, x3, x4), axis=1)  # 测试点
    
    # 5. 绘制分类图，因为有三种类别，所以需要三种颜色
    cm_light = mpl.colors.ListedColormap(['#A0FFA0', '#FFA0A0', '#A0A0FF'])
    cm_dark = mpl.colors.ListedColormap(['g', 'r', 'b'])
    
    y_show_hat = y_show_hat.reshape(x1.shape)  # 使之与输入的形状相同

    plt.figure(facecolor='w')
    plt.pcolormesh(x1, x2, y_show_hat, cmap=cm_light)  # 预测值的显示
    # 测试数据点的绘制
    # plt.scatter(x_test[:, 0], x_test[:, 1], c=y_test.ravel(), edgecolors='k', s=100, cmap=cm_dark, marker='o')  # 测试数据散点图，如果只想显示测试样本的图例，请把下行注释掉
    plt.scatter(x[:, 0], x[:, 1], c=y.ravel(), edgecolors='k', s=40, cmap=cm_dark)  # 全部数据的散点图
    plt.xlabel(iris_feature[0], fontsize=15)
    plt.ylabel(iris_feature[2], fontsize=15)
    plt.xlim(x1_min, x1_max)
    plt.ylim(x2_min, x2_max)
    plt.grid(True)
    plt.title('Iris Classification By Decision Tree', fontsize=17)
    plt.show()
    
    # 训练集上的预测结果
    y_test = y_test.reshape(-1)
    print(y_test_hat)
    print(y_test)
    result = (y_test_hat == y_test)   # True则预测正确，False则预测错误
    acc = np.mean(result)
    print('准确度: {:.2f}%'.format(100 * acc))

    # 过拟合：错误率
    depth = np.arange(1, 15)
    err_list = []
    for d in depth:
        clf = DecisionTreeClassifier(criterion='entropy', max_depth=d)
        clf = clf.fit(x_train, y_train)
        y_test_hat = clf.predict(x_test)  # 测试数据
        result = (y_test_hat == y_test)  # True则预测正确，False则预测错误
        err = 1 - np.mean(result)
        err_list.append(err)
        print(d, ' 错误率: %.2f%%' % (100 * err))
    plt.figure(facecolor='w')
    plt.plot(depth, err_list, 'ro-', lw=2)
    plt.xlabel(u'Depth of Decision Tree', fontsize=15)
    plt.ylabel(u'Error Rate', fontsize=15)
    plt.title(u'Depth of the Tree', fontsize=17)
    plt.grid(True)
    plt.show()
    
