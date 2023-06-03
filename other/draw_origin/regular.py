import csv
import sys
def regular(readData,minValue,maxValue):
    # 正規化
    for r in range(len(readData)):
        for c in range(1,len(readData[r])):
            # 灰階圖 rgb 0~255
            readData[r][c] = round((readData[r][c]-minValue)/(maxValue-minValue)*255)
# 原始數據才要開根號
def squareRoot(readData):
    for r in range(len(readData)):
        for c in range(1,len(readData[r])):
            readData[r][c] = readData[r][c]**0.5
def main(inputData):
    path = "../make_GEI/"+inputData
    readData = []
    maxValue = 0
    minValue = sys.maxsize
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                data = list(map(float,row[1:]))
                readData.append([row[0]]+data)
                maxValue = max(maxValue,max(data))
                minValue = min(minValue,min(data))
            except:
                pass
    squareRoot(readData)
    maxValue = maxValue**0.5
    minValue = minValue**0.5
    print("最大值",maxValue)
    print("最小值",minValue)
    regular(readData,minValue,maxValue)
    index = inputData.find('.csv')
    outputFile = inputData[:index]+"_regular"+inputData[index:]
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","data"])
        writer.writerows(readData)
    print("======= regular.py 完成 =======")
if __name__ == "__main__":
    main("2018micro.csv")