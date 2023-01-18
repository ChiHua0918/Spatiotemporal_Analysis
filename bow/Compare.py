# 計算每一種方法的分群結果好壞，進行比較
# ---------------------------------
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import davies_bouldin_score
from sklearn.cluster import KMeans
import csv
import pandas as pd
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# 折線圖
def draw(scoreData,pos,fileName):
    # width = int(len(scoreData)**0.5)
    subCanvas = canvas.add_subplot(3,2,pos)
    subCanvas.set_title(fileName)
    plt.xlabel('k')
    plt.ylabel('score')
    xData = [k for k in scoreData.keys()]
    data = [i for i in scoreData.values()]
    # 折線圖
    yData = [i['Silhouette_Coefficient'] for i in data]
    subCanvas.plot(xData, yData, marker='o', linestyle='-', color='r', label='Silhouette_Coefficient') 
    yData = [i['Calinski_Harabaz_Index'] for i in data]
    subCanvas.plot(xData, yData, marker='o', linestyle='-', color='b', label='Calinski_Harabaz_Index') 
    yData = [i['Davies_Bouldin_Index'] for i in data]
    subCanvas.plot(xData, yData, marker='o', linestyle='-', color='g', label='Davies_Bouldin_Index') 
# Davies-Bouldin Index(戴維森堡丁指數)(分類適確性指標)(DB)(DBI)
def DBIndex(data):
    labels = kmeans.labels_
    return davies_bouldin_score(data,labels)
# Calinski-Harabaz Index
def CHIndex(data):
    labels = kmeans.labels_
    return calinski_harabasz_score(data, labels)  
# 輪廓係數  Silhouette Coefficient
def SC(data):
    return silhouette_score(data, kmeans.predict(data))
def writeInFile(data,file,size):
    with open(f"../findBestWay/bowScores_{file}_{size}.csv", 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["k","file","Silhouette_Coefficient","Calinski_Harabaz_Index","Davies_Bouldin_Index"])
        writer.writerows(data)
# read file
def readFile(folder,file,size):
    with open(f"./data/{folder}/{file}_{size}.csv", newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        readData = [] # 數據
        for row in rows :
            try:
                readData.append(list(map(float,row[1:])))
            except:
                pass
    return readData
# write in file
# def writeInFile(data):
#     data.to_csv
def main(size):
    global kmeans
    folderList = ["accumulate","quadrantAccumulate","quadrantScore"]
    data = ["GEI_origin","GEI_level"]
    # 畫布
    pos = 1
    global canvas
    canvas = plt.figure()
    plt.subplots_adjust(hspace=1) # 子畫布間距
    canvas.tight_layout()
    # 數據
    for file in data:
        result = []
        for folder in folderList:
            # 分群數
            readData = readFile(folder,file,size)
            # k = max(cluster)+1
            fileName = f"{folder}_{file}_{size}"
            for k in range(2,10):
                kmeans = KMeans(n_clusters=k).fit(readData)
                # 評估指標 :分群數,Silhouette_Coefficient,Calinski_Harabaz_Index,Davies_Bouldin_Index
                # Davies_Bouldin_Index 因為只有 DBI 的指標越小代表分群越合理，所以將倒數
                result.append([k,fileName,SC(readData),CHIndex(readData),1/DBIndex(readData)])
            # draw(result[fileName],pos,fileName)
            pos += 1
        writeInFile(result,file,size)
    # result.index = ["k","Silhouette_Coefficient","Calinski_Harabaz_Index","Davies_Bouldin_Index"]
    # result.to_csv("../findBestWay/bowScores.csv")
    # print(show)
    # plt.legend(loc="upper right", fontsize=10)
    # plt.show()

    # print(result)
if __name__ == "__main__":
    size = int(input('請輸入 filter 大小：'))
    main(size)