# filter 相乘相加
import csv
import numpy as np


# 計算區域對每一個filter的分數
def countScores(filters,img,pos):
    relativePos = [0,1,2,10,11,12,19,20,21]
    # 抓取的範圍
    capture = []
    for j in relativePos:
        capture.append(img[pos+j])
    capture = np.array(capture)
    # print(capture)
    # 存放這個區塊乘上filter的分數
    scores = np.zeros(len(filters))
    # 該區塊*filter的分數
    for j in filters:
        multiply = capture.dot(j)
        scores[j] = multiply
    # print("socres",scores)
    return scores
# 擷取特徵
# 矩陣2*2(4種)(橫、直、右下斜、左下斜)
def bow(img):
    # filters = np.array([[1,1,-1,-1],[-1,-1,1,1],[1,-1,1,-1],[-1,1,-1,1],[1,-1,-1,1],[-1,1,1,-1]])
    filters = np.array([[1,1,1,-1,-1,-1,-1,-1,-1]
                       ,[-1,-1,-1,1,1,1,-1,-1,-1]
                       ,[-1,-1,-1,-1,-1,-1,1,1,1]
                       ,[1,-1,-1,1,-1,-1,1,-1,-1]
                       ,[-1,1,-1,-1,1,-1,-1,1,-1]
                       ,[-1,-1,1,-1,-1,1,-1,-1,1]
                       ,[1,-1,-1,-1,1,-1,-1,-1,1]
                       ,[-1,-1,1,-1,1,-1,1,-1,-1]])
    # 區塊符合filter的個數
    bag = np.zeros(len(filters))
    # GEI照片寬度
    width = len(img)**0.5
    for i in range(len(img)):
        # 高超出範圍
        if i//10 == width-3:
            break
        # 寬超出範圍
        elif i%10 == width-3 :
            # 2*2格子到照片寬的最後，就不要再往右走了
            i += 2
            continue
        # 計算區塊對每一個filter的分數 
        scores = countScores(filters,img,i)
        # 加到對應的filter個數
        maxNum = max(scores)
        filter_index = np.where(scores == maxNum)
        for pos in filter_index:
            bag[pos] += 1
    return bag
# 定義 GEI 灰階圖等級
def level(img):
    # levelList = [32,64,96,128,160,192,224,256]
    levelList = [16,32,46,64,80,96,112,128,144,160,176,192,208,224,240,256]
    img_Level = []
    for pixel in img:
        for level in levelList:
            # 屬於這個等級
            if level > pixel:
                pixel = levelList.index(level)
                img_Level.append(pixel)
                break
    return img_Level
    
# def grid(img):
#     average_grid = [] # 2*2方塊的最大數字
#     Dimension = 10
#     num = []
#     for r in range(0,Dimension,2):
#         for c in range(0,Dimension,2):
#             pos = 10*r+c
#             num.append(pos)

#     relativePos = [0,1,10,11]
#     catch = []
#     for pos in num:
#         for j in relativePos:
#             catch.append(img[pos+j])
#         average_grid.append(max(catch))
#     return average_grid
def readCSV():
    readData=[]
    name=[]
    with open("./flask/static/regularData/GEI_origin_average_regular.csv", newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            # 去掉檔頭
            if row[1].isdigit():
                name.append(row[0])
                readData.append(list(map(int,row[1:])))
    return name,readData
def main():
    name,readData = readCSV()
    scores = []
    # 計算圖片在每一個 filter 占比多少
    for i in range(len(readData)):
        # img_Level = level(readData[i])
        img_Level = readData[i]
        feature = bow(img_Level).astype(str)
        feature = np.insert(feature,0,name[i])
        scores.append(feature)
        # return
    with open("./flask/static/bow/GEI_origin_average_bow.csv", 'w', newline='') as _file:
            writer = csv.writer(_file)
            writer.writerows(scores)
if __name__ == '__main__':
    main()