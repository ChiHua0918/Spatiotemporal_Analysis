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
    # 給采禎的每小時 PM2.5 加強對比圖
    elif mode == "makeEveryHour":
        file = "2018micro.csv"
        os.system(f"python3 ./code/regular.py {file}")
        file = "2018micro_singleRegular.csv"
        os.system(f"python3 ./code/userDataPic.py {file}")
if __name__ == __name__:
    modeList = {
        1:"GEI",
        2:"makeEveryHour"
    }
    print("========== Mode List ==========")
    print(*[f"\t{i[0]}:{i[1]}\n" for i in modeList.items()])
    userSelect = int(input("Please enter the number to select the mode:"))
    cutFile = input("cutFile = ")
    singleContrast(modeList[userSelect],cutFile)