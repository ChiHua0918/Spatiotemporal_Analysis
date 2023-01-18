import csv
import sys
def regular(readData):
    # 正規化
    for r in range(len(readData)):
        maxValue = max(readData[r][1:])
        minValue = min(readData[r][1:])
        print("最大值",maxValue)
        print("最小值",minValue)
        for c in range(1,len(readData[r])):
            # 灰階圖 rgb 0~255
            readData[r][c] = round((readData[r][c]-minValue)/(maxValue-minValue)*255)
def main(argv):
    inputData = argv
    inputFile = "./static/data/"+inputData
    readData = []
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                data = list(map(float,row[1:]))
                readData.append([row[0]]+data)
            except:
                pass
    regular(readData)
    index = inputData.find('.csv')
    outputData = inputData[:index]+"_regular"+inputData[index:]
    outputFile = "./static/data/GEI_regular/"+ outputData
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","data"])
        writer.writerows(readData)
    print("regular.py 完成")
if __name__ == "__main__":
    main(sys.argv[1])