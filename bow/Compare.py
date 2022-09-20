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
    canvas = plt.figure()
    width = int(len(scoreData)**0.5)
    pos = 1
    for data in scoreData:
        subCanvas = canvas.add_subplot(width,width,pos)
        subCanvas.set_title(fileName)
        # 折線圖
        yData = [k for key,k in data.items()]
        xData = [value for Silhouette_Coefficient,value in data.items()]
        plt.plot(xData, yData, marker='o', linestyle='--', color='r', label='Silhouette_Coefficient') 
        xData = [value for Calinski_Harabaz_Index,value in data.items()]
        plt.plot(xData, yData, marker='o', linestyle='--', color='b', label='Calinski_Harabaz_Index') 
        xData = [value for Davies_Bouldin_Index,value in data.items()]
        plt.plot(xData, yData, marker='o', linestyle='--', color='g', label='Davies_Bouldin_Index') 
        plt.xlabel('k')
        plt.ylabel('score')
    # 相同群數在同一個子畫布
    # pos = 0
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
def main(size):
    global kmeans
    folderList = ["accumulate","quadrantAccumulate","quadrantScore"]
    data = ["GEI_origin","GEI_level"]
    result = dict()
    # scores = [] # 輪廓係數分數
    # chi_value = [] # calinski_harabaz_score 分數
    # print("quadrant、quadrantDecideNum")
    # print("請問要選取哪一個資料夾:",end = " ")
    # folder = input()
    pos = 0
    for folder in folderList:
        for file in data:
            # 分群數
            readData = readFile(folder,file,size)
            # k = max(cluster)+1
            fileName = f"{folder}_{file}_{size}"
            result[fileName] = []
            for k in range(2,10):
                kmeans = KMeans(n_clusters=k).fit(readData)
                # 評估指標
                fileScore = {
                                'k':k,
                                # 'file':f"{folder}_{file}_{size}",
                                'Silhouette_Coefficient':SC(readData),
                                'Calinski_Harabaz_Index':CHIndex(readData),
                                'Davies_Bouldin_Index':DBIndex(readData)
                            }
                # record.append(fileScore)
                result[fileName].append(fileScore)
            draw(result[fileName],pos,fileName)
            pos += 1
    show = pd.DataFrame(result)
            # .sort_values(by=['k'])
    # show.set_index("k",inplace=True)
    print(show)
    plt.legend()
    plt.show()

    # print(result)
if __name__ == "__main__":
    size = int(input('請輸入 filter 大小：'))
    main(size)