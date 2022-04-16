# filter 相乘相加
import csv
import numpy as np
import sys

# 計算區域對每一個filter的分數
def countScores(filter,img,pos,size):
    relativePos = np.array([i for i in range(size)])
    copyPos = relativePos.copy()
    width = len(img)**0.5 # 照片寬度
    # 區域的相對位置
    for i in range(1,size):
        relativePos = np.append(relativePos,copyPos+width*i)
    # 抓取的範圍
    capture = np.array([])
    for j in relativePos:
        capture = np.append(capture,img[pos+int(j)])
    # 對應位置相乘之和
    score = capture.dot(filter) 
    return score
# 計算 GEI 經過 filter 後的圖片分數(7*7 or  8*8)
# img:GEI filters:直橫斜 size: filter 大小
def multiplyFilter(img,filter,size):
    # GEI照片寬度
    width = len(img)**0.5
    # GEI 各 filter 的分數
    score = []
    for i in range(len(img)):
        # 高超出範圍
        if i//10 == width-size:
            break
        # 寬超出範圍
        elif i%10 == width-size:
            continue
        # 計算區塊對每一個filter的分數
        score.append(countScores(filter,img,i,size))
    return score
# 採用 ?*? 的 filter
# size: filter 的大小
def choiceFilter(size):
    match size:
        case 2:
            return np.array([[1,1,-1,-1] # 上橫 row
                            ,[1,-1,1,-1] # 左豎 col
                            ,[1,-1,-1,1] # 右下斜 rightdowm
                            ,[-1,1,1,-1]]) # 左下斜 leftdown
        case 3:
            return np.array([[-1,-1,-1,1,1,1,-1,-1,-1] # 橫
                            ,[-1,1,-1,-1,1,-1,-1,1,-1] # 豎
                            ,[1,-1,-1,-1,1,-1,-1,-1,1]
                            ,[-1,-1,1,-1,1,-1,1,-1,-1]])
        case _:
            print("目前沒有設定此大小的 filter")
            print("請再輸入一次 filter 大小:",end = " ")
            size = int(input())
            choiceFilter(size)
def main(argv,size):
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
    for  filter in filters: # 計算 4 種 filter 的分數
        score = dict()
        for i in range(len(readData)):
            # 計算每個 GEI filter 的分數
            feature = multiplyFilter(readData[i],filter,size)
            # 轉型態，因為 slice 必須同型態，所以先轉為 string
            # feature = np.array(feature,dtype="str")
            # feature = np.insert(feature,0,name[i])
            score[name[i]] = feature
            # print(name[i])
        result.append(score)
    # 資料輸出
    index = inputData.find("_regular")
    # 4 種 filter 計算出的分數分成 4 個 csv
    filter_name = ["row","col","rightDown","leftDown"]
    for i in range(len(filter_name)):
        outputData = "./data/strengthenEdge/"+inputData[:index]+f"_bow_{size}_{filter_name[i]}.csv"
        with open(outputData, 'w', newline='') as _file:
                writer = csv.writer(_file)
                for key,value in result[i].items():
                    writer.writerow([key,*value])
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
    # main()