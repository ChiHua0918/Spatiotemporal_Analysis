# filter 相乘相加
import csv
import numpy as np
import sys

# 累計象限分數，width: 象限寬度
def accumulate(allScore,scoreWidth):
    allScore = np.reshape(allScore,(len(allScore)//scoreWidth,scoreWidth))
    # 4 個象限分數
    result = [0 for i in range(4)]
    pos = 0 # 加到哪一個象限
    for i in range(len(allScore)):
        if i >= scoreWidth*2:
            pos = 2 # 從左下角的象限開始加
        result[pos+i%2] += sum(allScore[i])
    return result
# GEI 分成 4 個象限，每一個象限做 filter
# img:GEI filters:直橫斜 size: filter 大小
def calculateScore(img,filter,size):
    width = int(len(img)**0.5) # GEI照片寬度
    allScore = [] # GEI 區塊 和 filter 相乘的所有分數
    r = 0
    c = 0
    img = np.reshape(img,(width,width))
    # 圖片抓取範圍
    relativePosR = []
    relativePosC = []
    for i in range(size):
        relativePosR += [i for times in range(size)]
        relativePosC += [j for j in range(size)]
    while r <= width-size:
        score = 0
        # GEI 區塊 X filter
        for pos in range(len(relativePosR)):
            score += img[r+relativePosR[pos]][c+relativePosC[pos]]*filter[pos]
        allScore.append(score)
        c += 1
        # 寬超出範圍，下一行
        if c%width > width-size:
            r += 1
            c = 0
            # 換下面的象限
            if r%width == width//2-size+1:
                r += size-1
        # 換右邊的象限
        elif c%10 == width//2-size+1:
            c += size-1
    # 累計 4 個象限分數
    result = accumulate(allScore,width//2-size+1)
    return result
# =================================
# 採用 ?*? 的 filter
# size: filter 的大小
def choiceFilter(size):
    while True:
        if size == '2':
            return np.array([[1,1,-1,-1]
                            ,[1,-1,1,-1]
                            ,[1,-1,-1,1]
                            ,[-1,1,1,-1]])
        elif size == '3':
            return np.array([[-1,-1,-1,2,2,2,-1,-1,-1]
                            ,[-1,2,-1,-1,2,-1,-1,2,-1]
                            ,[2,-1,-1,-1,2,-1,-1,-1,2]
                            ,[-1,-1,2,-1,2,-1,2,-1,-1]])
        print("目前沒有設定此大小的 filter")
        print("請再輸入一次 filter 大小:",end = " ")
        size = int(input())
        choiceFilter(size)
def main(inputData,size,cutType,year):
    # 輸入 filter 大小
    filters = choiceFilter(size)
    size = int(size)
    # 讀取 GEI 資料
    name,readData = [],[] # GEI 名字，GEI 10*10 資料
    inputFile = f"../make_GEI/data/{year}/GEI_regular/{cutType}/{inputData}.csv"
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append(list(map(int,row[3:])))
                name.append(row[0])
            except:
                pass

    result = []
    for i in range(len(readData)):
        score = [name[i]]
        for filter in filters:
            # 計算每個 GEI filter 的分數
            feature = calculateScore(readData[i],filter,size)
            # 轉型態，因為 slice 必須同型態，所以先轉為 string
            # feature = np.array(feature,dtype="str")
            # feature = np.insert(feature,0,name[i])
            score += feature
            # score[name[i]] = feature
        result.append(score)
    # 資料輸出
    outputData = f"./bow/data/{year}/{cutType}/quadrantAccumulate/{inputData}_{size}.csv"
    with open(outputData, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerows(result)
    # 資料輸出
    # index = inputData.find("_regular")
    # # 4 種 filter 個別累加 -> 產出 4 種 csv
    # filter_name = ["row","col","rightDown","leftDown"]
    # for i in range(len(filter_name)):
    #     outputData = "./data/accumulate/"+inputData[:index]+f"_bow_{size}_{filter_name[i]}.csv"
    #     with open(outputData, 'w', newline='') as _file:
    #             writer = csv.writer(_file)
    #             for key,value in result[i].items():
    #                 writer.writerow([key,*value])
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    # main()