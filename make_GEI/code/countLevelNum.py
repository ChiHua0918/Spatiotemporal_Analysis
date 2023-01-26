import csv
import matplotlib.pyplot as plt
import sys

# 等級計算個數
def HD(data) :
    HisData = []
    for r in range(len(data)):
        His = list(plt.hist(data[r][3:], bins=16, range=[0, 16]))
        oneData = list(His[0])
        # 插入名字 (2018/1/1 00:00)
        oneData.insert(0,data[r][0])
        HisData.append(oneData)
    return HisData

# 數據轉為 0~9 級
def convert(data) :
    # 各計數的上界
    levelList = [7.5,15.5,25.5,35.5,45.5,54.5,102.5,150.5,250.5]
    for r in range(len(data)):
        for c in range(3, len(data[0])) :
            for i in range(len(levelList)) :
                # 超過 250.5 = 9 級
                if data[r][c] > 250.5:
                    data[r][c] = len(levelList)
                    break
                if (levelList[i] >= data[r][c]) :
                    data[r][c] = i
                    break
    return data
def main(argv,cutFile,form):
    inputData = argv
    cutType = cutFile[:cutFile.find(".csv")]
    if form == "begin": # 2018micro.csv
        path = "./"+inputData
    elif form == "regular": # 已正規化數據
        path = f"./data/GEI_regular/{cutType}/{inputData}"

    readData = []
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        next(rows) # 跳過標題
        for row in rows :
            readData.append(row[:3]+list(map(float,row[3:])))
    # 轉換等級
    readData = convert(readData)
    HisData = HD(readData)
    # index = inputData.find('.csv')
    # outputData = inputData[:index]+"_countNum"+inputData[index:]
    outputFile = f"./data/countLevelNum/{cutType}/{inputData}"
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","data"])
        writer.writerows(HisData)
    print("======= countLevelNum.py 完成 =======")

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])