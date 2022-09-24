# 計算每一種方法的分群結果好壞，進行比較
# ---------------------------------
from tkinter import Canvas
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
    # 畫布
    pos = 1
    global canvas
    canvas = plt.figure()
    plt.subplots_adjust(hspace=1) # 子畫布間距
    canvas.tight_layout()
    # 數據
    for folder in folderList:
        for file in data:
            # 分群數
            readData = readFile(folder,file,size)
            # k = max(cluster)+1
            fileName = f"{folder}_{file}_{size}"
            result[fileName] = dict()
            for k in range(2,10):
                kmeans = KMeans(n_clusters=k).fit(readData)
                # 評估指標
                fileScore = {
                                # 'k':k,
                                # 'file':f"{folder}_{file}_{size}",
                                'Silhouette_Coefficient':SC(readData),
                                'Calinski_Harabaz_Index':CHIndex(readData)/100,
                                'Davies_Bouldin_Index':DBIndex(readData)
                            }
                # record.append(fileScore)
                result[fileName][k] = fileScore
            # print(result)
            draw(result[fileName],pos,fileName)
            pos += 1
    show = pd.DataFrame(result)
    # .sort_values(by=['k'])
    # show.set_index("k",inplace=True)
    print(show)
    plt.legend(loc="upper right", fontsize=10)
    plt.show()

    # print(result)
if __name__ == "__main__":
    size = int(input('請輸入 filter 大小：'))
    main(size)