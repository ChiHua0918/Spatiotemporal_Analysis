# 切 cut 流程
# GEI 製作流程
import os

from numpy import source
def cut():
    # 計算原始 10*10 彩色空汙圖中，各 Level 佔多少
    # 輸出: 每一張彩色空汙圖各 Level 數量
    # file = "2018micro.csv"
    # print(f"python ./code/countLevelNum.py {file}")
    # os.system(f"python ./code/countLevelNum.py {file}")
    # K-means 分群
    file = "2018micro_countNum.csv"
    print(f"python ./code/cluster.py {file}")
    os.system(f"python ./code/cluster.py {file}")
    # 切 cut
    file = "2018micro_cluster.csv"
    print(f"python ./code/cut.py {file}")
    os.system(f"python ./code/cut.py {file}")

def GEI():
    sourceData = ["2018micro.csv","2018level.csv"]
    outputData = ["GEI_origin.csv","GEI_Level.csv"]
    # 數據疊成GEI
    # for i in range(len(sourceData)):
    #     print(f"python ./code/GEI.py {sourceData[i]} {outputData[i]}")
    #     os.system(f"python ./code/GEI.py {sourceData[i]} {outputData[i]}")
    # GEI正規化
    for file in outputData:
        print(f"python ./code/regular.py {file}")
        os.system(f"python ./code/regular.py {file}")
    # 劃出GEI圖
    drawData = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    for file in drawData:
        print(f"python ./code/userDataPic.py {file}")
        os.system(f"python ./code/userDataPic.py {file}")

# 將原始 PM2.5 數據轉為等級
def microToLevel():
    file = "2018micro.csv"
    print(f"python ./code/covertToLevel.py {file}")
    os.system(f"python ./code/covertToLevel.py {file}")

def main():
    # cut()
    # 資料 --- 1. 原始數據 2. 等級數據
    # microToLevel()
    GEI()
if __name__ == '__main__':
    main()