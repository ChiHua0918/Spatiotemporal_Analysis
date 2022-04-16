import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import AgglomerativeClustering # top - button
import scipy.cluster.hierarchy as sch
import csv
def hierarchical(data):
    # affinity: 距離的計算方式”euclidean”,”l1″,”l2″,”manhattan”,”cosine”…
    # linkage: 群與群之間的距離，”ward”,”complete”,”average”,”single”
    # ml=AgglomerativeClustering(n_clusters=k,affinity='euclidean',linkage='single')
    # ml.fit_predict(data)
    # 進行分群
    dis=sch.linkage(data,metric='euclidean',method='single')
    print(max(dis[0]))
    # sch.dendrogram(dis,color_threshold=20)
    # plt.title('Hierarchical Clustering')
    # plt.show()
def main():
    # 要分多少群
    data = [[-39,32],[-22,38],[-40,23],[-33,37],[-28,37],[-5,-1],[12,1],[9,-11],[26,31],[28,25],[35,30],[37,23],[29,29],[0,0]]

    hierarchical(data)
if __name__ == "__main__":
    main()