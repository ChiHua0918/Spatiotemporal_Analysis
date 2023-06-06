import os

def createFile(path):
    if os.path.isdir(path) == False:
        os.system("mkdir "+ path)
# 切 cut 流程
def cut(file,year):
    # 計算原始 10*10 空汙圖中，10 種等級佔比多少
    # 輸出: 每小時空汙直方圖
    createFile("./data/countLevelNum")
    createFile(f"./data/countLevelNum/{year}")
    print(f"python3 ./code/countLevelNum.py {file} None begin {year}")
    os.system(f"python3 ./code/countLevelNum.py {file} None begin {year}")
    # K-Means 分群
    createFile(f"./data/clustering")
    createFile(f"./data/clustering/{year}")
    print(f"python3 ./code/cluster.py {file} None begin  {year}")
    os.system(f"python3 ./code/cluster.py {file} None begin  {year}")
    # 切 cut
    print(f"python3 ./code/cut.py {file} {year}")
    os.system(f"python3 ./code/cut.py {file} {year}")
# GEI 製作流程
def GEI(sourceData,outputData,cutFile,year):
    # 數據疊成GEI
    cutType = cutFile[:cutFile.index('.csv')]
    createFile(f"./data/GEI_data/")
    createFile(f"./data/GEI_data/{year}")
    createFile(f"./data/GEI_data/{year}/{cutType}")
    createFile(f"./data/GEI_regular")
    createFile(f"./data/GEI_regular/{year}")
    createFile(f"./data/GEI_regular/{year}/{cutType}")
    createFile(f"./picture/{year}")
    createFile(f"./picture/{year}/{cutType}")
    for i in range(len(sourceData)):
        print(f"python3 ./code/GEI.py {sourceData[i]} {cutFile} {outputData[i]} {year}")
        os.system(f"python3 ./code/GEI.py {sourceData[i]} {cutFile} {outputData[i]} {year}")
        # GEI正規化
        print(f"python3 ./code/regular.py {outputData[i]} {cutFile} {year}")
        os.system(f"python3 ./code/regular.py {outputData[i]} {cutFile} {year}")
        # 劃出GEI圖
        createFile(f"./picture/{year}/{cutType}/{outputData[i][:outputData[i].index('.csv')]}")
        print(f"python3 ./code/userDataPic.py {outputData[i]} {cutFile} {year}")
        os.system(f"python3 ./code/userDataPic.py {outputData[i]} {cutFile} {year}")

# 將原始 PM2.5 數據轉為等級
def microToLevel(source,year):
    print(f"python3 ./code/covertToLevel.py {source} {year}")
    os.system(f"python3 ./code/covertToLevel.py {source} {year}")

def main():
    source = "2018micro.csv"
    year = source[:source.index("micro")]
    microToLevel(source,year)
    createFile("./data")
    createFile("./picture")
    # K-Means 切割出 shot
    cut(source,year)
    # 資料 --- 1. 原始數據 2. 等級數據
    sourceData = ["2018micro.csv","2018level.csv"]
    outputData = ["GEI_origin.csv","GEI_level.csv"]
    cutFile = input("(KMenas.csv、HCED1.csv、RasterScan4.csv)\ncut file = ") #cut.csv、HCED1.csv、RasterScan4.csv
    # 疊加成 GEI
    GEI(sourceData,outputData,cutFile,year)
if __name__ == '__main__':
    main()