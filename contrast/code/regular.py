# 單張 GEI 正規化
import csv
import sys
def regular(readData):
    # 正規化
    for r in range(len(readData)):
        minValue = min(readData[r][GEI_index:])
        maxValue = max(readData[r][GEI_index:])
        for c in range(1,len(readData[r])):
            # 灰階圖 rgb 0~255
            try:
                readData[r][c] = round((readData[r][c]-minValue)/(maxValue-minValue)*255)
            except: # 如果最大最小值相同 -> 全黑的圖
                readData[r][c] = 0
def main(argv,cutType):
    # gei 數據從哪裡開始
    global GEI_index
    GEI_index = 3
    inputData = argv+".csv"
    inputFile = f"../make_GEI/data/GEI_data/{cutType}/{inputData}"
    readData = []
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        next(rows) # 跳過標題
        for row in rows :
            readData.append(row[:GEI_index]+list(map(float,row[GEI_index:])))
    regular(readData)
    outputFile = f"./{argv}_{cutType}.csv"
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","data"])
        writer.writerows(readData)
    print("regular.py 完成")
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])