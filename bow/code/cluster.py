from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
import csv
import sys
# k-means分類
def k_means(data):
    scores = []      # 輪廓係數分數
    results = []     # 分群結果
    # 找出最好的分群數
    for k in range(2,11):
        # n_clusters: 分為 k 群 n_init: 運行 k-menas 多少次(每一次的初始群心皆不同) max_iter: 最多迭代幾次
        # .fit 計算 k-means 的分群
        kmeans = KMeans(n_clusters=k,n_init=10,max_iter=300).fit(data)
        # 分群結果
        results.append(kmeans)
        # 輪廓係數
        scores.append(silhouette_score(data, kmeans.predict(data)))
    # 取結果分數最好的
    k = scores.index(max(scores))+2
    cluster = results[k].predict(data)
    print("群心",KMeans(n_clusters=k,n_init=10,max_iter=300).fit(data).cluster_centers_)
    print(f"分 {k} 類")
    return cluster

def main(argv):
    # 數據
    inputData = argv
    inputFile =  "./data/"+inputData
    readData = []
    name = []
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append(list(map(float,row[1:])))
                name.append(row[0])
            except:
                pass
    cluster = k_means(readData)
    for i in range(len(cluster)):
        readData[i].insert(0,name[i])
        readData[i].insert(1,cluster[i])
    index = inputData.find("_bow")
    outputData = inputData[:index]+"_cluster.csv"
    outputFile = "./data/clustering/"+ outputData
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","cluster","LevelNum"])
        writer.writerows(readData)

if __name__ == '__main__':
    main(sys.argv[1])
