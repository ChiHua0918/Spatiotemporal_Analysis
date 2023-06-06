import csv
import sys
# 疊加 GEI
def GEI(data,cut_shot):
    print(f"data 總共有 {len(data)} 筆")
    print(f"cut_shot 總共有 {len(cut_shot)} 筆")
    if len(data) != len(cut_shot):
        print("error! Check the source file.")
    n = 0 # 目前疊加幾張
    puliMapLength = len(data[0])-1 # length of data in puli map
    energy = [0 for i in range(puliMapLength)]
    number = 0 # 第幾張 GEI
    GEIData = []
    for i in range(len(cut_shot)):
        # cut -> 計算 GEI 數據（平均）
        if int(cut_shot[i][1]) == 1 and n != 0:
            energy = [j/n for j in energy]
            name = f"NO.{number}"
            endTime = cut_shot[i-1][0]
            tmp = [name,startTime,endTime]+energy
            GEIData.append(tmp)
            # init setting
            n = 0
            number += 1
            energy = [0 for j in range(puliMapLength)]
        # shot -> 疊加
        elif int(cut_shot[i][1]) == 0:
            # first image in shot
            if n == 0:
                startTime = cut_shot[i][0]
            energy = [energy[j]+data[i][j+1] for j in range(puliMapLength)]
            n += 1
    return GEIData
# read csv file
def readCSV(inputFile):
    readData = []
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        next(rows) # 跳過標題
        for row in rows :
            # row[0]: time
            readData.append([row[0]]+list(map(float,row[1:])))
    return readData
def main(source,cutFile,output,year):
    # 數據
    inputFile = source
    data = readCSV(inputFile)
    # cut
    inputFile = cutFile
    cut_shot = readCSV(cutFile)
    # 疊加 GEI
    GEIData = GEI(data,cut_shot)
    outputFile = f"./data/GEI_data/{year}/{cutFile[:cutFile.find('.csv')]}/{output}"
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["number","start","end","data"])
        writer.writerows(GEIData)
    print("======= GEI.py 完成 =======")
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])