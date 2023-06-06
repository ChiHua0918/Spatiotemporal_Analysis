import csv
import sys

# 數據轉為 0~9 級
def convert(data,inpuFile,startIndex) :
    result = []
    # 各計數的上界
    if inpuFile == "GEI_origin":
        levelList = [25,50,75,100,125,150,175,200,225,250]
    else:
        levelList = [7.5,15.5,25.5,35.5,45.5,54.5,102.5,150.5,250.5]
    for r in range(len(data)):
        HisData = [0 for i in range(len(levelList)+1)]
        for c in range(startIndex, len(data[0])) :
            for i in range(len(levelList)) :
                # 超過 250.5 = 9 級
                if data[r][c] > 250.5:
                    HisData[len(levelList)] += 1
                    break
                elif (levelList[i] >= data[r][c]) :
                    HisData[i] += 1
                    break
        HisData.insert(0,data[r][0])
        result.append(HisData)
    return result
def main(inputData,cutFile,form,year):
    cutType = cutFile[:cutFile.find(".csv")]
    startIndex = 0
    if form == "begin": # 2018micro.csv
        path = "./"+inputData
        startIndex = 1
        outputFile = f"./data/countLevelNum/{year}/{inputData}"
    elif form == "regular": # 已正規化數據
        path = f"../make_GEI/data/GEI_regular/{year}/{cutType}/{inputData}"
        outputFile = f"./histogram/data/countLevelNum/{year}/{cutType}/{inputData}"
        startIndex = 3
    readData = []
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        next(rows) # 跳過標題
        for row in rows :
            readData.append(row[:startIndex]+list(map(float,row[startIndex:])))
    # 轉換等級
    result = convert(readData,inputData,startIndex)

    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","data"])
        writer.writerows(result)
    print("======= countLevelNum.py 完成 =======")

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])