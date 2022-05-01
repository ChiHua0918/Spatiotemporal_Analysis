from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
import csv
import sys
from matplotlib import pyplot as plt

# 畫圖
def draw(fileName,X,scores,distortions):
    fig = plt.figure()
    # 輪廓係數
    fig.add_subplot(211)
    fig.suptitle(fileName)
    # plt.figure(figsize=(15,10),dpi=100,linewidth = 2)
    plt.plot(X,scores,'s-',color = 'r')
    plt.title("Silhouette Coefficient")
    plt.xlabel("k") # labelpad代表與圖片的距離
    plt.ylabel("score")
    # SSE
    fig.add_subplot(212)
    plt.plot(X,distortions,'s-',color = 'r')
    plt.title("SSE (Elbow method)") # 每群 "點到群心的平方和" 總距離
    plt.xlabel("k") # labelpad代表與圖片的距離
    plt.ylabel("distance")
    fig.tight_layout()
# 選最好的分群數 k
def selectK(distortions):
    diff = []
    for i in range(1,len(distortions)):
        diff.append(distortions[i] - distortions[i-1])
    # average
    average = abs((diff[0]+diff[len(diff)-1])/len(diff))
    print("average",average)
    # select k
    for i in range(len(diff)):
        if abs(diff[i]) < average:
            k = i
            break
    return k
# k-means分類
def k_means(fileName,data):
    scores = []      # 輪廓係數分數
    distortions = [] # SSE
    results = []     # 分群結果
    least = 2        # 至少要分多少群
    most = 16        # 最多酚多少群
    # 找出最好的分群數
    for k in range(least,most):
        # n_clusters: 分為 k 群 n_init: 運行 k-menas 多少次(每一次的初始群心皆不同) max_iter: 最多迭代幾次
        # .fit 計算 k-means 的分群
        kmeans = KMeans(n_clusters=k,n_init=10,max_iter=300).fit(data)
        # 分群結果
        results.append(kmeans)
        # 輪廓係數
        scores.append(silhouette_score(data, kmeans.predict(data)))
        # SSE
        distortions.append(kmeans.inertia_) 
    # 取結果分數最好的
    # k = scores.index(max(scores))+least
    k = selectK(distortions)+least
    cluster = KMeans(n_clusters=k,n_init=10,max_iter=300).fit(data).predict(data)
    print("群心",KMeans(n_clusters=k,n_init=10,max_iter=300).fit(data).cluster_centers_)
    print(f"分 {k} 類")
    draw(fileName,[i for i in range(least,most)],scores,distortions)
    return cluster

def main(argv,folder):
    # 數據
    inputData = argv
    inputFile =  f"./data/{folder}/"+inputData
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
    cluster = k_means(inputData,readData)
    for i in range(len(cluster)):
        readData[i].insert(0,name[i])
        readData[i].insert(1,cluster[i])
    # index = inputData.find("_bow")
    # outputData = inputData[:index]+"_cluster.csv"
    outputFile = f"./data/clustering/{folder}/"+ inputData
    print("outpuFilte:",outputFile)
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","cluster","LevelNum"])
        writer.writerows(readData)
    plt.show()
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
