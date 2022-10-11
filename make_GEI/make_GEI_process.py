import os
# 切 cut 流程
def cut():
    # 計算原始 10*10 彩色空汙圖中，各 Level 佔多少
    # 輸出: 每一張彩色空汙圖各 Level 數量
    file = "2018micro.csv"
    print(f"python3 ./code/countLevelNum.py {file} begin")
    os.system(f"python3 ./code/countLevelNum.py {file} begin")
    # K-Means 分群
    # file = "2018micro_countLevelNum.csv"
    print(f"python3 ./code/cluster.py {file}")
    os.system(f"python3 ./code/cluster.py {file}")
    # 切 cut
    # file = "2018micro_cluster.csv"
    print(f"python3 ./code/cut.py {file}")
    os.system(f"python3 ./code/cut.py {file}")

# GEI 製作流程
def GEI():
    cutFile = "cut.csv"
    sourceData = ["2018micro.csv","2018level.csv"]
    outputData = data
    # 數據疊成GEI
    for i in range(len(sourceData)):
        print(f"python3 ./code/GEI.py {sourceData[i]} {cutFile} {outputData[i]}")
        os.system(f"python3 ./code/GEI.py {sourceData[i]} {cutFile} {outputData[i]}")
    # GEI正規化
    for file in outputData:
        print(f"python3 ./code/regular.py {file}")
        os.system(f"python3 ./code/regular.py {file}")
    # 劃出GEI圖
    for file in outputData:
        print(f"python3 ./code/userDataPic.py {file}")
        os.system(f"python3 ./code/userDataPic.py {file}")
# GEI 分群
def GEIcluster():
    # GEI 正規化後(0~255)的數據
    for file in data:
        print(f"python3 ./code/countLevelNum.py {file} regular")
        os.system(f"python3 ./code/countLevelNum.py {file} regular")
    # data = ["GEI_origin_regular_countNum.csv","GEI_Level_regular_countNum.csv"]
    for file in data:
        print(f"python3 ./code/cluster.py {file}")
        os.system(f"python3 ./code/cluster.py {file}")

# 將原始 PM2.5 數據轉為等級
def microToLevel():
    file = "2018micro.csv"
    print(f"python3 ./code/covertToLevel.py {file}")
    os.system(f"python3 ./code/covertToLevel.py {file}")

def main():
    global data
    data = ["GEI_origin.csv","GEI_level.csv"]
    cut()
    # 資料 --- 1. 原始數據 2. 等級數據
    # microToLevel()
    GEI()
    GEIcluster()
if __name__ == '__main__':
    main()