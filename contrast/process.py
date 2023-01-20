import os
# GEI 分群
def singleContrast(mode):
    # GEI 正規化後(0~255)的數據
    if mode == "standard":
        data = ["GEI_origin.csv","GEI_level.csv"]
        for file in data:
            print(f"python3 ./code/regular.py {file}")
            os.system(f"python3 ./code/regular.py {file}")
        drawData = ["GEI_origin_singleRegular.csv","GEI_level_singleRegular.csv"]
        for file in drawData:
            print(f"python3 ./code/userDataPic.py {file}")
            os.system(f"python3 ./code/userDataPic.py {file}")
    # 給采禎的每小時 PM2.5 加強對比圖
    elif mode == "makeEveryHour":
        file = "2018micro.csv"
        os.system(f"python3 ./code/regular.py {file}")
        file = "2018micro_singleRegular.csv"
        os.system(f"python3 ./code/userDataPic.py {file}")
if __name__ == __name__:
    modeList = {
        1:"standard",
        2:"makeEveryHour"
    }
    print("========== Mode List ==========")
    print(*[f"\t{i[0]}:{i[1]}\n" for i in modeList.items()])
    userSelect = int(input("Please enter the number to select the mode:"))
    singleContrast(modeList[userSelect])