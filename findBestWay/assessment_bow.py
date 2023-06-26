'''
三種指標分數
算出 BOW 三種方法的各指標分數
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
    folder = f"../GEI_clustering/clustering/{year}/{cutFile}/bow"
    bow_way = ["accumulate", "quadrantAccumulate", "quadrantScore"]
    # folderList = [f"../GEI_clustering/clustering/{year}/{cutFile}/cnn/imagenet",f"../GEI_clustering/clustering/{year}/{cutFile}/bow/accumulate",f"../GEI_clustering/clustering/{year}/{cutFile}/histogram"]
    data = ["GEI_origin","GEI_level"]
    filterSize = [2,3]
    # 數據
    for file in data:
        result = []
        for way in bow_way:
            for size in filterSize:
                path = f"{folder}/{way}/{file}_{size}.csv"
                # 分群數
                readData = readFile(path)
                fileName = f"{way}_{file}_{size}"
                for k in range(2,10):
                    kmeans = KMeans(n_clusters=k).fit(readData)
                    # 評估指標 :分群數,Silhouette_Coefficient,Calinski_Harabaz_Index,Davies_Bouldin_Index
                    # Davies_Bouldin_Index 因為只有 DBI 的指標越小代表分群越合理，所以將倒數
                    result.append([k,fileName,SC(readData),CHIndex(readData),1/DBIndex(readData)])
        outputPath = f"./assessment_bow/bow_{file}.csv"
        writeInFile(result,outputPath)
        print(f"============== {file} ==============")
        result = pd.DataFrame(result,columns=["k","file","Silhouette_Coefficient","Calinski_Harabaz_Index","Davies_Bouldin_Index"])
        print(result)
if __name__ == "__main__":
    if os.path.isdir("./threeWay") == False:
        os.system("mkdir ./threeWay")
    main()