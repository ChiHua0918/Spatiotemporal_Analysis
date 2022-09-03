# filter 相乘相加
import csv
import numpy as np
import sys

# 計算區域對每一個filter的分數
def countScores(img,pos,size):
    # 抓取區域的相對位置
    # relativePos = [0,1,2,10,11,12,19,20,21]
    relativePos = np.array([i for i in range(size)]*size)
    width = len(img)**0.5 # 照片寬度
    for row in range(size):
        for col in range(size):
            relativePos[row*size+col] = width*row+col
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
    return score
# GEI 分成 4 個象限，每一個象限做 filter
# img:GEI filters:直橫斜 size: filter 大小
def bowAccumulateScore(img,size):
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
        scores += countScores(img,i,size)
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
        case '2':
            return np.array([[1,1,-1,-1]
                            ,[1,-1,1,-1]
                            ,[1,-1,-1,1]
                            ,[-1,1,1,-1]])
        case '3':
            return np.array([[-1,-1,-1,2,2,2,-1,-1,-1]
                            ,[-1,2,-1,-1,2,-1,-1,2,-1]
                            ,[2,-1,-1,-1,2,-1,-1,-1,2]
                            ,[-1,-1,2,-1,2,-1,2,-1,-1]])
        case _:
            size = input("目前沒有設定此大小的 filter,請再輸入一次 filter 大小:")
            choiceFilter(size)
def main(argv,size):
    global filters
    filters = choiceFilter(size)
    # 讀取 GEI 資料
    name,readData = [],[] # GEI 名字，GEI 10*10 資料
    inputData = argv
    inputFile = f"../make_GEI/data/GEI_regular/{inputData}.csv"
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append(list(map(int,row[1:])))
                name.append(row[0])
            except:
                pass
    result = dict()
    # 計算圖片在每一個 filter 占比多少
    for i in range(len(readData)):
        # 計算每個 GEI filter 的分數
        feature = bowAccumulateScore(readData[i],int(size))
        result[name[i]] = feature
    # 資料輸出
    outputData = f"./data/accumulate/{inputData}_{size}.csv"
    with open(outputData, 'w', newline='') as _file:
            writer = csv.writer(_file)
            for key, value in result.items():
                writer.writerow([key,*value])
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
    # main()