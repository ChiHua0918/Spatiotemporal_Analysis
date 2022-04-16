from sklearn.cluster import KMeans
import csv
import sys
# k-means分類
def k_means(data,k):
    kmeans = KMeans(n_clusters=k,n_init=10,max_iter=300).fit(data)
    # 輪廓係數
    print("群心",KMeans(n_clusters=k,n_init=10,max_iter=300).fit(data).cluster_centers_)
    print(f"分 {k} 類")
    return kmeans.predict(data)

def main(argv,fileName):
    # 數據
    inputData = fileName
    inputFile =  argv
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
    print("要分多少群",end=" ")
    k = int(input())
    cluster = k_means(readData,k)
    for i in range(len(cluster)):
        readData[i].insert(0,name[i])
        readData[i].insert(1,cluster[i])
    # index = inputData.find("_bow")
    # outputData = inputData[:index]+"_decideClusterNum.csv"
    outputData = inputData
    outputFile = "./data/clustering/quadrantDecideNum/"+ outputData
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","cluster","LevelNum"])
        writer.writerows(readData)

if __name__ == '__main__':
    # main()
    main(sys.argv[1],sys.argv[2])
