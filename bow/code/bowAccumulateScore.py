# filter 相乘相加
import csv
import numpy as np
import sys

# 計算區域對每一個filter的分數
def countScores(filters,img,pos,size):
    # 抓取區域的相對位置
    # relativePos = [0,1,2,10,11,12,19,20,21]
    relativePos = np.array([i for i in range(size)])
    copyPos = relativePos.copy()
    width = len(img)**0.5 # 照片寬度
    for i in range(1,size):
        relativePos = np.append(relativePos,copyPos+width*i)
    # 抓取的範圍
    capture = np.array([])
    for j in relativePos:
        capture = np.append(capture,img[pos+int(j)])
    # 存放這個區塊乘上filter的分數
    score = np.zeros(len(filters))
    # 該區塊*filter的分數
    for j in range(len(filters)):
        multiply = capture.dot(filters[j])
        score[j] = multiply
    # print("socres",scores)
    return score
# GEI 分成 4 個象限，每一個象限做 filter
# img:GEI filters:直橫斜 size: filter 大小
def bowAccumulateScore(img,filters,size):
    # 區塊符合filter的個數
    # bag = np.zeros(len(filters))
    # GEI照片寬度
    width = len(img)**0.5
    # GEI 各 filter 的分數
    scores = np.zeros(len(filters))
    for i in range(len(img)):
        # 高超出範圍
        if i//10 == width-size:
            break
        # 寬超出範圍
        elif i%10 == width-size:
            continue
        # 計算區塊對每一個filter的分數
        scores += countScores(filters,img,i,size)
        # 加到對應的filter個數
        # maxNum = max(scores)
        # filter_index = np.where(scores == maxNum)
        # for pos in filter_index:
        #     bag[pos] += 1
    return scores
# =================================
# 採用 ?*? 的 filter
# size: filter 的大小
def choiceFilter(size):
    match size:
        case 2:
            return np.array([[1,1,-1,-1]
                            ,[1,-1,1,-1]
                            ,[1,-1,-1,1]
                            ,[-1,1,1,-1]])
        case 3:
            return np.array([[-1,-1,-1,1,1,1,-1,-1,-1]
                            ,[-1,1,-1,-1,1,-1,-1,1,-1]
                            ,[1,-1,-1,-1,1,-1,-1,-1,1]
                            ,[-1,-1,1,-1,1,-1,1,-1,-1]])
        case _:
            print("目前沒有設定此大小的 filter")
            print("請再輸入一次 filter 大小:",end = " ")
            size = int(input())
            choiceFilter(size)
def main(argv,size):
    # 輸入 filter 大小
    size = int(size)
    filters = choiceFilter(size)
    # 讀取 GEI 資料
    name,readData = [],[] # GEI 名字，GEI 10*10 資料
    inputData = argv
    inputFile = "../make_GEI/data/GEI_regular/"+inputData
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append(list(map(int,row[1:])))
                name.append(row[0])
            except:
                pass
    result = []
    # 計算圖片在每一個 filter 占比多少
    for i in range(len(readData)):
        # 計算每個 GEI filter 的分數
        feature = bowAccumulateScore(readData[i],filters,size)
        # 轉型態，因為 slice 必須同型態，所以先轉為 string
        feature = np.array(feature,dtype="str")
        feature = np.insert(feature,0,name[i])
        result.append(feature)
        print(name[i])
    # 資料輸出
    index = inputData.find("_regular")
    # 4 種 filter 個別累加 -> 產出 4 種 csv
    filter_name = ["row","col","rightDown","leftDown"]
    for i in range(len(filter_name)):
        outputData = "./data/quadrant/"+inputData[:index]+f"_bow_{size}_{filter_name[i]}.csv"
        with open(outputData, 'w', newline='') as _file:
                writer = csv.writer(_file)
                for key,value in result[i].items():
                    writer.writerow([key,*value])
    # 4 種 filter 累加分數
    # outputData = "./data/"+inputData[:index]+f"_bow_{size}.csv"
    # with open(outputData, 'w', newline='') as _file:
    #         writer = csv.writer(_file)
    #         writer.writerows(result)
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
    # main()