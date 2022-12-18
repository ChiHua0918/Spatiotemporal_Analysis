# 用多目標客觀排名不同方法的 BOW
# ----------------------------
import csv
# read file
def readFile(path):
    # 資料格式
    # {
    #     k:{
    #         fileName:{
    #             'Silhouette_Coefficient':,
    #             'Calinski_Harabaz_Index':,
    #             'Davies_Bouldin_Index':
    #         }
    #     }
    # }
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
# 絕對支配 indexName: 各個指標名字
def dominate(header,data):
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
    # 計算分群結果的分數指標有多少個
    indexNum = len(allOrderList)
    # 絕對支配的方法
    dominateWays = []
    # 找出有絕對優勢的檔案 (三個指標都第一名, 接下來看有沒有三個指標第二名,...) 
    for i in range(len(data.keys())): # 幾種方法
        num = 0
        fileName = allOrderList[i][0]
        for j in range(indexNum):
            if allOrderList[j][i] != fileName:
                break
            num += 1
        if num == indexNum:
            dominateWays.append(fileName)
        else:
            break
    return dominateWays
    # # 每一個指標的最高分的檔名
    # bestScore = []
    # for indexName in header:
    #     score = 0 # 最高分
    #     highestName = "" # 最高分的檔名
    #     for fileName in data.keys():
    #         if data[fileName][indexName] > score:
    #             score = data[fileName][indexName]
    #             highestName = fileName
    #     bestScore.append(highestName)
    # # 有絕對支配
    # if bestScore.count(bestScore[0]) == len(bestScore):
    #     return [bestScore[0]]
    # return []
# constrained: 超過平均
def constrained(header,data):
    passWay = dict()
    lowerBound = dict()
    # 每一個指標的平均
    for indexName in header:
        avgScore = 0
        for fileName in data.keys():
            avgScore += data[fileName][indexName]
        lowerBound[indexName] = avgScore/len(data.keys())
    for fileName in data.keys():
        isPass = True
        for indexName in header:
            if data[fileName][indexName] < lowerBound[indexName]:
                isPass = False
        if isPass:
            passWay[fileName] = data[fileName]
    return passWay
# 多目標 - compromise 作用：因為 constrain 篩選後有可能會有多個第二名，所以採用 compromise 將多個第二名再排序
# readData: 一開始讀取的資料 orderData: 已經排名的資料
def compromise(header,data,orderData):
    tmp = []
    # 歐基理得距離
    for fileName in orderData:
        # 目標 [1,1,1]
        dis = 0
        dis += (1-data[fileName]['Silhouette_Coefficient'])**2
        dis += (1-data[fileName]['Calinski_Harabaz_Index'])**2
        dis += (1-data[fileName]['Davies_Bouldin_Index'])**2
        tmp.append([fileName, dis**0.5])
    # 距離越長，排名越後面 => 遞增排序
    tmp.sort(key=lambda x:x[1])
    return [i[0] for i in tmp]
# 正規化
def regular(header,data):
    tmp = [[] for i in range(len(header))]
    # 找各指標最大最小
    for fileName in data.keys():
        for j in range(len(header)):
            tmp[j].append(data[fileName][header[j]])
    minNum = [min(i) for i in tmp]
    maxNum = [max(i) for i in tmp]
    # 最大最小正規化
    for fileName in data.keys():
        for i in range(len(header)):
            data[fileName][i] = (data[fileName][header[i]]-minNum[i])/(maxNum[i]-minNum[i])
    return data
# data: 目前還沒排名的方法們 removeData: 已給予排名
def removeWay(data,removeData):
    for fileName in removeData:
        data.pop(fileName)
    return data
def printTable(k,result):
    print(f"|{k}|",end="")
    for i in result:
        print(f"{i}|",end="")
    print()
def main():
    path = "./test/"
    source = ["GEI_origin.csv","GEI_level.csv"]
    for file in source:
        print(f"============== {file} =============")
        print("|k|NO.1|NO.2|NO.3|NO.4|NO.5|NO.6|")
        print("|:-:|:-:|:-:|:-:|:-:|:-:|:-:|")
        tmpPath = path+file
        header, readData = readFile(tmpPath)
        indexNames = header[2:]
        # 依照分群數分群比較
        for k in range(2,10):
            uncategorizedWay = readData[k].copy()
            # 多目標 - 絕對支配
            first = dominate(indexNames,uncategorizedWay)
            uncategorizedWay = removeWay(uncategorizedWay,first)
            result = [i for i in first]
            # 多目標 - constrain
            second = constrained(indexNames,uncategorizedWay)
            uncategorizedWay = removeWay(uncategorizedWay,second)
            readData[k] = regular(indexNames,readData[k])
            tmpOrder = compromise(indexNames,readData[k],second)
            result += [i for i in tmpOrder]
            # 剩餘還未排名的方法進行排名
            tmpOrder = compromise(indexNames,readData[k],uncategorizedWay)
            result += [i for i in tmpOrder]
            # 印結果表格 （採用 hackmd 表格）
            printTable(k,result)
if __name__ == "__main__":
    main()