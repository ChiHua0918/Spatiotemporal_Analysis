import csv
import sys
def regular(readData,minValue,maxValue):
    # 正規化
    for r in range(len(readData)):
        for c in range(3,len(readData[r])):
            # 灰階圖 rgb 0~255
            readData[r][c] = round((readData[r][c]-minValue)/(maxValue-minValue)*255)
# 原始數據才要開根號
def squareRoot(readData):
    for r in range(len(readData)):
        for c in range(3,len(readData[r])):
            readData[r][c] = readData[r][c]**0.5
def main(argv):
    inputData = argv
    path = "./data/GEI_data/"+inputData
    readData = []
    maxValue = 0
    minValue = sys.maxsize
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        next(rows) # 跳過標題
        for row in rows :
            data = list(map(float,row[3:]))
            readData.append(row[:3]+data)
            maxValue = max(maxValue,max(data))
            minValue = min(minValue,min(data))
    index = inputData.find('.csv')
    mode = inputData[:index]
    if mode == "GEI_origin":
        squareRoot(readData)
        maxValue = maxValue**0.5
        minValue = minValue**0.5
    print("最大值",maxValue)
    print("最小值",minValue)
    regular(readData,minValue,maxValue)
    # outputData = inputData[:index]+"_regular"+inputData[index:]
    outputFile = "./data/GEI_regular/"+ inputData
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","start","end","data"])
        writer.writerows(readData)
    print("======= regular.py 完成 =======")
if __name__ == "__main__":
    main(sys.argv[1])