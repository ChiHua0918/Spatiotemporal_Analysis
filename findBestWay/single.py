import csv
# 單目標
def single_object(header,data):
    allOrderList = []
    # 各個指標排序
    for indexName in header:
        order = []
        for fileName in data.keys():
            # [方法名, 該方法的指標分數]
            order.append([fileName,data[fileName][indexName]])
        # 依照兩個元素的第二個元素（index=1）遞減排序
        order.sort(key=lambda x:x[1],reverse = True)
        allOrderList.append(order)
    # allOrderList [ [[fileName,第 0 個指標數值],...], [第 1 個指標同左...], [第三個指標同左...] ]
    # 排名相加 --- 相加排名越小，名次越前面
    result = dict()
    for i in range(len(header)):
        for j in range(len(allOrderList[i])):
            fileName = allOrderList[i][j][0]
            if fileName not in result.keys():
                result[fileName] = 0
            result[fileName] += j
    return result
# read file
def readFile(path):
    '''
    資料格式
    {
        k:{
            fileName:{
                'Silhouette_Coefficient':,
                'Calinski_Harabaz_Index':,
                'Davies_Bouldin_Index':
            }
        }
    }
    '''
    readData = dict()
    for k in range(2,10):
        readData[k] = dict()
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        # 標題
        header = next(rows)
        # 資料
        for row in rows :
            tmp = dict()
            # tmp['k'] = int(row[0])
            # tmp['file'] = row[1]
            tmp['Silhouette_Coefficient'] = float(row[2])
            tmp['Calinski_Harabaz_Index'] = float(row[3])
            tmp['Davies_Bouldin_Index'] = float(row[4])
            readData[int(row[0])][row[1]] = tmp
    return header, readData
def main():
    # BOW
    path = "./assessment_bow/"
    source = ["bow_GEI_origin.csv","bow_GEI_level.csv"]
    # three way（histogram, BOW, CNN）
    # path = "./threeWay/"
    # source = ["GEI_origin.csv","GEI_level.csv"]
    for file in source:
        print(f"============== {file} =============")
        print("|k|NO.1|NO.2|NO.3|NO.4|NO.5|NO.6|")
        print("|:-:|:-:|:-:|:-:|:-:|:-:|:-:|")
        # print("|k|NO.1|NO.2|NO.3|")
        # print("|:-:|:-:|:-:|:-:|")
        tmpPath = path+file
        header, readData = readFile(tmpPath)
        # 依照分群數分群比較
        for k in range(2,10):
            uncategorizedWay = readData[k]
            # 單目標
            result = single_object(header[2:],uncategorizedWay)
            # 印下名次
            print("|",k,end="")
            for fileName,value in result.items():
                print(f"| {fileName}({value}) ",end="")
            print("|")
if __name__ == "__main__":
    main()