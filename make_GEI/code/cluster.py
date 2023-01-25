from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
import csv
import sys
import matplotlib.pyplot as plt #畫圖
# 畫圖
def draw(k,scores):
    # 母畫布
    fig = plt.figure()
    # 輪廓係數
    plt.title('Silhouette scores',fontsize=10)
    plt.plot(range(2,11),scores)
    plt.plot(k+2,scores[k],"go")
    plt.show()
def k_means(data):
    scores = []      # 輪廓係數分數 (silhouette score)
    results = []     # 分群結果
    for k in range(2,11):
        # n_clusters: 分為 k 群 n_init: 運行 k-menas 多少次(每一次的初始群心皆不同) max_iter: 最多迭代幾次
        # .fit 計算 k-means 的分群
        kmeans = KMeans(n_clusters=k,n_init=10,max_iter=50).fit(data)
        results.append(kmeans)
        scores.append(silhouette_score(data, kmeans.predict(data)))
    # 取結果分數最好的
    k = scores.index(max(scores))
    cluster = results[k].predict(data)
    print("群心",KMeans(n_clusters=k+2,n_init=10,max_iter=50).fit(data).cluster_centers_)
    print(f"分 {k+2} 類")
    print("score of silhouette score is",scores[k])
    # draw(k,scores)
    return cluster

def main(argv,cutFile):
    cutType = cutFile[:cutFile.find(".csv")]
    # 數據
    inputData = argv
    path =  f"./data/countLevelNum/{cutType}/{inputData}"
    readData = []
    name = []
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        next(rows) # 跳過標題
        for row in rows :
            readData.append(list(map(float,row[1:])))
            name.append(row[0])
    cluster = k_means(readData)
    for i in range(len(cluster)):
        readData[i].insert(0,name[i])
        readData[i].insert(1,cluster[i])
    # outputData = inputData.split("_countNum")[0]+"_cluster.csv"
    outputFile = f"./data/clustering/{cutType}/{inputData}"
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["time","cluster","LevelNum"])
        writer.writerows(readData)
    print("======= 分群完成 =======")
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
