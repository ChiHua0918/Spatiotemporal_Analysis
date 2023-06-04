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

def main(folder,inputData,size,cutType,year):
    # 數據
    readData = []
    name = []
    inputFile = f"./bow/data/{year}/{cutType}/{folder}/{inputData}_{size}.csv"
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append(list(map(float,row[1:])))
                name.append(row[0])
            except:
                pass
    k = int(input("要分多少群: "))
    cluster = k_means(readData,k)
    for i in range(len(cluster)):
        readData[i].insert(0,name[i])
        readData[i].insert(1,cluster[i])
    outputFile = f"./clustering/{year}/{cutType}/bow/quadrantScoreDecideNum/{inputData}_quadrantScoreDecideNum_{size}.csv"
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["time","cluster","data"])
        writer.writerows(readData)

if __name__ == '__main__':
    # main()
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
