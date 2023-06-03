import os

def createFile(path):
    if os.path.isdir(path) == False:
        os.system("mkdir "+ path)
# 將原始 PM2.5 數據轉為等級
def microToLevel():
    source = "2018micro.csv"
    print(f"python3 ./code/covertToLevel.py {source}")
    os.system(f"python3 ./code/covertToLevel.py {source}")
# 切 cut 流程
def cut(file,year):
    # 計算原始 10*10 空汙圖中，10 種等級佔比多少
    # 輸出: 每小時空汙直方圖
    '''
    createFile(f"./data/countLevelNum")
    print(f"python3 ./code/countLevelNum.py {file} None begin {year}")
    os.system(f"python3 ./code/countLevelNum.py {file} None begin {year}")
    '''
    # K-Means 分群
    createFile(f"./data/{year}/clustering")
    print(f"python3 ./code/cluster.py {file} None begin  {year}")
    os.system(f"python3 ./code/cluster.py {file} None begin  {year}")
    # 切 cut
    print(f"python3 ./code/cut.py {file} {year}")
    os.system(f"python3 ./code/cut.py {file} {year}")
# GEI 製作流程
def GEI(sourceData,outputData,cutFile,year):
    # 數據疊成GEI
    for i in range(len(sourceData)):
        cutType = cutFile[:cutFile.index('.csv')]
        createFile(f"./data/{year}/GEI_data")
        createFile(f"./data/{year}/GEI_data/{cutType}")
        print(f"python3 ./code/GEI.py {sourceData[i]} {cutFile} {outputData[i]} {year}")
        os.system(f"python3 ./code/GEI.py {sourceData[i]} {cutFile} {outputData[i]} {year}")
        # GEI正規化
        createFile(f"./data/{year}/GEI_regular")
        createFile(f"./data/{year}/GEI_regular/{cutType}")
        print(f"python3 ./code/regular.py {outputData[i]} {cutFile} {year}")
        os.system(f"python3 ./code/regular.py {outputData[i]} {cutFile} {year}")
        # 劃出GEI圖
        createFile(f"./picture/{year}/{cutType}")
        createFile(f"./picture/{year}/{cutType}/{outputData[i][:outputData[i].index('.csv')]}")
        print(f"python3 ./code/userDataPic.py {outputData[i]} {cutFile} {year}")
        os.system(f"python3 ./code/userDataPic.py {outputData[i]} {cutFile} {year}")


def main():
    microToLevel()
    source = "2018micro.csv"
    year = source[:source.index("micro")]
    createFile("./data")
    createFile("./data/"+year)
    createFile("./picture")
    createFile("./picture/"+year)
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