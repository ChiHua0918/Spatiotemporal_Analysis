import csv
import sys
# 疊加 GEI
def GEI(data,cut_shot):
    print(f"data 總共有 {len(data)} 筆")
    print(f"cut_shot 總共有 {len(cut_shot)} 筆")
    if len(data) != len(cut_shot):
        print("error! Check the source file.")
    n = 0 # 目前疊加幾張
    energy = [0 for i in range(len(data[0]))]
    number = 0 # 第幾張 GEI
    GEIData = []
    for i in range(len(cut_shot)):
        # cut -> 結算
        if int(cut_shot[i][0]) == 1 and n != 0:
            energy = [j/n for j in energy]
            name = f"NO.{number}"
            energy.insert(0,name)
            GEIData.append(energy)
            # print(GEIData[0])
            n = 0
            number += 1
            energy = [0 for j in range(len(data[i]))]
        # shot -> 疊加
        elif int(cut_shot[i][0]) == 0:
            energy = [energy[j]+data[i][j] for j in range(len(energy))]
            n += 1
    return GEIData
# read csv file
def readCSV(inputFile):
    readData = []
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append(list(map(float,row[1:])))
            except:
                pass
    return readData
def main(source,cutFile,output):
    # 數據
    inputFile = source
    data = readCSV(inputFile)
    # cut
    inputFile = cutFile
    cut_shot = readCSV(cutFile)
    # 疊加 GEI
    GEIData = GEI(data,cut_shot)
    outputFile = "./data/GEI_data/"+output
    with open(outputFile, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["number","data"])
        writer.writerows(GEIData)
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])