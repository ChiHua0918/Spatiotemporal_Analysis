# 照片分成 4 個象限，filter 按照象限順序乘以 filter
import csv
import numpy as np
import sys

# filter x 照片區塊
# img:GEI filters:直橫斜 size: filter 大小
def multiplyFilter(img,filter,size):
    width = int(len(img)**0.5) # GEI照片寬度
    resultScore = [] # 和 filter 相乘的分數
    r = 0
    c = 0
    img = np.reshape(img,(10,10))
    # 圖片抓取範圍
    relativePosR = []
    relativePosC = []
    for i in range(size):
        relativePosR += [i for times in range(size)]
        relativePosC += [j for j in range(size)]
    while r <= width-size:
        score = 0
        for pos in range(len(relativePosR)):
            score += img[r+relativePosR[pos]][c+relativePosC[pos]]*filter[pos]
        # 計算區塊對每一個filter的分數
        resultScore.append(score)
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
    # 同一個象限的分數放在一起
    scoreWidth = width//2-size+1
    resultScore = np.reshape(resultScore,(len(resultScore)//scoreWidth,scoreWidth))
    odd = []
    even = []
    for i in range(len(resultScore)):
        if i % 2 != 0:
            odd.append(resultScore[i])
        else:
            even.append(resultScore[i])
    # print(*odd)
    # print(even)
    return np.reshape(even+odd,(1,len(even+odd)*scoreWidth))[0]
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
        result.append(score)
    # 資料輸出
    index = inputData.find("_regular")
    # 4 種 filter 計算出的分數分成 4 個 csv
    filter_name = ["row","col","rightDown","leftDown"]
    for i in range(len(filter_name)):
        outputData = "./data/quadrant/"+inputData[:index]+f"_bow_{size}_{filter_name[i]}.csv"
        with open(outputData, 'w', newline='') as _file:
                writer = csv.writer(_file)
                for key,value in result[i].items():
                    writer.writerow([key,*value])
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
    # main()