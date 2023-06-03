import os
# GEI 分群
def singleContrast(mode,cutFile):
    # GEI 正規化後(0~255)的數據
    if mode == "GEI":
        data = ["GEI_origin","GEI_level"]
        cutType = cutFile[:cutFile.find(".csv")]
        for file in data:
            print(f"python3 ./code/regular.py {file} {cutType}")
            os.system(f"python3 ./code/regular.py {file} {cutType}")
            print(f"python3 ./code/userDataPic.py {file} {cutType}")
            os.system(f"python3 ./code/userDataPic.py {file} {cutType}")
    # 給采禎的每小時 PM2.5 加強對比圖(ex:2018micro)
    elif mode == "makeEveryHour":
        file = cutFile[:cutFile.find(".csv")] # "2018micro"
        os.system(f"python3 ./code/regular.py {file} {mode}")
        os.system(f"python3 ./code/userDataPic.py {file} {mode}")
if __name__ == __name__:
    modeList = {
        1:"GEI",
        2:"makeEveryHour"
    }
    print("========== Mode List ==========")
    print(*[f"\t{i[0]}:{i[1]}\n" for i in modeList.items()])
    userSelect = int(input("Please enter the number to select the mode:"))
    # 2018micro.csv 是補值後的一年空污資料，因為要給采禎在 QBE 呈現，所以增加此項
    cutFile = input("(2018micro.csv、KMenas.csv、HCED1.csv、RasterScan4.csv)\ncut file = ")
    singleContrast(modeList[userSelect],cutFile)