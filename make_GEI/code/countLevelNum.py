import csv
import matplotlib.pyplot as plt
import sys

# 等級計算個數
def HD(data) :
    HisData = []
    for r in range(len(data)):
        print(data[r][0])
        His = list(plt.hist(data[r][1:], bins=16, range=[0, 16]))
        # print("His",His)
        oneData = list(His[0])
        oneData.insert(0,data[r][0])
        HisData.append(oneData)
    return HisData

# 0~9 級
def part(data) :
    # 各計數的上界
    levelList = [7.5,15.5,25.5,35.5,45.5,54.5,102.5,150.5,250.5]
    for r in range(len(data)):
        for c in range(1, len(data[0])) :
            for i in range(len(levelList)) :
                # 超過 250.5 = 9 級
                if data[r][c] > 250.5:
                    data[r][c] = len(levelList)
                    break
                if (levelList[i] >= data[r][c]) :
                    data[r][c] = i
                    break
def main(argv):
    inputData = argv
    inputFile = inputData
    readData = []
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append([row[0]]+list(map(float,row[1:])))
            except:
                pass
    part(readData)
    print(readData[0])
    HisData = HD(readData)
    index = inputData.find('.csv')
    outputData = inputData[:index]+"_countNum"+inputData[index:]
    outputFile = "./data/countLevelNum/" + outputData
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["number","data"])
        writer.writerows(HisData)
    print("countLevelNum.py 完成")

if __name__ == "__main__":
    main(sys.argv[1])