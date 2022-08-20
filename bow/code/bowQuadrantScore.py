# filter 相乘相加
# word: 象限內的個別分數，假設 filter 3x3 ＝> 9（一個象限產生的數據）x 4(個象限) ＝ 36 個數據
import csv
import numpy as np
import sys

# # 計算區域對每一個filter的分數
# def countScores(filter,img,pos,size):
#     # relativePos = np.array([i for i in range(size)])
#     # copyPos = relativePos.copy()
#     # width = len(img)**0.5 # 照片寬度
#     # # 區域的相對位置
#     # for i in range(1,size):
#     #     relativePos = np.append(relativePos,copyPos+width*i)
#     for i in range(len(relativePos)):

#     # # 抓取的範圍
#     # capture = np.array([])
#     # for j in range(len(relativePos)):
#     #     capture = np.append(capture,img[pos+int(j)])
#     # # 對應位置相乘之和
#     # score = capture.dot(filter) 
#     return score
# 調整 word 順序, feature:GEI x filter 後的結果 scoreWidth: 象限的數據寬度
def adjust(feature,scoreWidth):
    return np.reshape(feature,(len(feature)//scoreWidth,scoreWidth))
# img:GEI filters:直橫斜 size: filter 大小
def multiplyFilter(img,size,relativePos,score):
    r = 0
    c = 0
    for filter in filters:
        pos = 0
        while r <= width-size:
            # GEI 區塊
            block = np.array([img[(r*width+c)+i] for i in relativePos])
            # GEI 區塊 X filter
            score[pos] += sum(filter*block)
            pos += 1
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
            return np.array([[-1,-1,-1,1,1,1,-1,-1,-1]
                            ,[-1,1,-1,-1,1,-1,-1,1,-1]
                            ,[1,-1,-1,-1,1,-1,-1,-1,1]
                            ,[-1,-1,1,-1,1,-1,1,-1,-1]])
        case _:
            size = int(input("目前沒有設定此大小的 filter,請再輸入一次 filter 大小:"))
            choiceFilter(size)
def main(argv,size):
    global filters,width
    size = int(size)
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
    # GEI照片寬度
    width = int(len(readData[1])**0.5)
    # 圖片抓取範圍
    relativePos = []
    for r in range(size):
        for c in range(size):
            relativePos.append(r*width+c)
    # 計算圖片在每一個 filter 占比多少
    result = dict()
    for i in range(len(readData)):
        # GEI 各 filter 的分數, 一個象限數據：(width//2-size)的平方, 4 個象限
        dataLength = (width//2-size+1) **2 *4
        # 計分
        score = np.zeros(dataLength)
        # 計算每個 GEI filter 的分數
        feature = multiplyFilter(readData[i],size,relativePos,score)
        # 調整順序＝> word 為 4 個象限數據，每一個數據有 3* 3 個（假設 filter = 3*3）
        feature = adjust(feature,width//2-size+1)
        result[name[i]] = np.reshape(feature,dataLength)
    # 資料輸出
    outputData = f"./data/quadrantScore/{inputData}_{size}.csv"
    with open(outputData, 'w', newline='') as _file:
        writer = csv.writer(_file)
        for key,value in result.items():
            writer.writerow([key,*value])
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
    # main()