import csv
import sys
# 0~9 級
def covertToLevel(data):
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
    return data
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
    data = covertToLevel(readData)
    with open("2018level.csv", 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerows(data)
    print("======= covertToLevel.py 完成 =======")
if __name__ == "__main__":
    main(sys.argv[1])