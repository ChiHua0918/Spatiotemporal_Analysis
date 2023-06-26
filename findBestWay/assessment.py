'''
三種指標分數
1. 從實驗結果可得 accumulate 的分群結果較佳，所以 BOW 取 accumulate 作為代表
2. 三大方法中 (histogram, bow, cnn)算出各指標分數
'''
import os
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import davies_bouldin_score
from sklearn.cluster import KMeans
import csv
import pandas as pd

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
def writeInFile(data,outputPath):
    with open(outputPath, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["k","file","Silhouette_Coefficient","Calinski_Harabaz_Index","Davies_Bouldin_Index"])
        writer.writerows(data)
# read file
def readFile(path):
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        readData = [] # 數據
        for row in rows :
            try:
                readData.append(list(map(float,row[1:])))
            except:
                pass
    return readData
def main():
    global kmeans
    year = int(input("year="))
    cutFile = input("(KMenas、HCED1、RasterScan4)\ncut file = ")
    folderList = [f"../GEI_clustering/clustering/{year}/{cutFile}/cnn/imagenet",f"../GEI_clustering/clustering/{year}/{cutFile}/bow/accumulate",f"../GEI_clustering/clustering/{year}/{cutFile}/histogram"]
    data = ["GEI_origin","GEI_level"]
    # 數據
    for file in data:
        result = []
        for folder in folderList:
            if "histogram" in folder:
                path = f"{folder}/{file}.csv"
                fileName = f"histogram_{file}"
            elif "bow" in folder:
                # 由 9/27 實驗結果可知，BOW 最佳為 accumulate，目前 CNN 的 filter = 3，所以 BOW filter 取 3 作為 input
                path = f"{folder}/{file}_3.csv"
                fileName = f"bow_{file}"
            elif "cnn" in folder:
                path = f"{folder}/{file}_imagenet.csv"
                fileName = f"cnn_{file}"
            # 分群數
            readData = readFile(path)
            for k in range(2,10):
                kmeans = KMeans(n_clusters=k).fit(readData)
                # 評估指標 :分群數,Silhouette_Coefficient,Calinski_Harabaz_Index,Davies_Bouldin_Index
                # Davies_Bouldin_Index 因為只有 DBI 的指標越小代表分群越合理，所以將倒數
                result.append([k,fileName,SC(readData),CHIndex(readData),1/DBIndex(readData)])
        outputPath = f"./threeWay/{file}.csv"
        writeInFile(result,outputPath)
        print(f"============== {file} ==============")
        result = pd.DataFrame(result,columns=["k","file","Silhouette_Coefficient","Calinski_Harabaz_Index","Davies_Bouldin_Index"])
        print(result)
if __name__ == "__main__":
    if os.path.isdir("./assessment_bow") == False:
        os.system("mkdir ./assessment_bow")
    main()