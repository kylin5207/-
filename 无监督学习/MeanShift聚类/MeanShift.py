# !/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import sklearn.datasets as ds
import matplotlib.colors
from sklearn.cluster import MeanShift
from sklearn.metrics import euclidean_distances


if __name__ == "__main__":
    
    #产生聚类数据
    N = 1000
    centers = [[1, 2], [-1, -1], [1, -1], [-1, 1]]
    data, y = ds.make_blobs(N, n_features=2, centers=centers, cluster_std=[0.5, 0.25, 0.7, 0.5], random_state=0)

    matplotlib.rcParams['font.sans-serif'] = [u'SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10, 9), facecolor='w')
    
    #计算各个数据之间的欧几里得距离
    m = euclidean_distances(data, squared=True)
    bw = np.median(m)
    print("欧几里得距离中位数：", bw)
    
    for i, mul in enumerate(np.linspace(0.1, 0.4, 4)):
        band_width = mul * bw #用不同系数去和中位数相乘，将这个结果作为带宽
        model = MeanShift(bin_seeding=True, bandwidth=band_width)
        ms = model.fit(data)
        centers = ms.cluster_centers_ #得到聚类质心
        y_hat = ms.labels_
        n_clusters = np.unique(y_hat).size
        print('带宽：', mul, band_width, '聚类簇的个数为：', n_clusters)

        plt.subplot(2, 2, i+1)
        plt.title(u'带宽：%.2f，聚类簇的个数为：%d' % (band_width, n_clusters))
        clrs = []
        for c in np.linspace(16711680, 255, n_clusters):
            clrs.append('#%06x' % int(c))
        # clrs = plt.cm.Spectral(np.linspace(0, 1, n_clusters))
        print(clrs)
        
        for k, clr in enumerate(clrs):
            cur = (y_hat == k)
            plt.scatter(data[cur, 0], data[cur, 1], c=clr, edgecolors='none')
        #绘制聚类中心
        plt.scatter(centers[:, 0], centers[:, 1], s=150, c=clrs, marker='*', edgecolors='k')
        plt.grid(True)
    plt.tight_layout(2)
    plt.suptitle(u'MeanShift聚类', fontsize=20)
    plt.subplots_adjust(top=0.92)
    plt.show()
