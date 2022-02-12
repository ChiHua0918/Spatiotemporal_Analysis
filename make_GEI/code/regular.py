import csv
import sys
def regular(readData,minValue,maxValue):
    # 正規化
    for r in range(len(readData)):
        for c in range(1,len(readData[r])):
            readData[r][c] = round((readData[r][c]-minValue)/(maxValue-minValue))
# 原始數據才要開根號
def squareRoot(readData):
    for r in range(len(readData)):
        for c in range(1,len(readData[r])):
            readData[r][c] = readData[r][c]**0.5
def main(argv):
    inputData = argv
    inputFile = "./data/GEI_data/"+inputData
    readData = []
    maxValue = 0
    minValue = sys.maxsize
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                data = list(map(float,row[1:]))
                readData.append([row[0]]+data)
                # 最大
                if maxValue < max(data):
                    maxValue = max(data)
                # 最小
                if minValue > min(data):
                    minValue = min(data)
            except:
                pass
    index = inputData.find('.csv')
    mode = inputData[:index]
    if mode == "GEI_origin":
        squareRoot(readData)
    regular(readData,minValue,maxValue)
    outputData = inputData[:index]+"_regular"+inputData[index:]
    outputFile = "./data/GEI_regular/"+ outputData
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","data"])
        writer.writerows(readData)
    print("regular.py 完成")
if __name__ == "__main__":
    main(sys.argv[1])