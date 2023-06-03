import os

def createFile(path):
    if os.path.isdir(path) == False:
        os.system("mkdir "+ path)
# GEI 分群
def singleContrast(mode,cutType,year):
    # GEI 正規化後(0~255)的數據
    if mode == "GEI":
        data = ["GEI_origin","GEI_level"]
        createFile(f"./image/{year}/{cutType}")
        for file in data:
            createFile(f"./image/{year}/{cutType}/{file}")
            print(f"python3 ./code/regular.py {file} {cutType} {year}")
            os.system(f"python3 ./code/regular.py {file} {cutType} {year}")
            print(f"python3 ./code/userDataPic.py {file} {cutType} {year}")
            os.system(f"python3 ./code/userDataPic.py {file} {cutType} {year}")
    # 給采禎的每小時 PM2.5 加強對比圖(ex:2018micro)
    elif mode == "makeEveryHour":
        createFile(f"./image/{year}/{mode}")
        file = cutType# "2018micro"
        os.system(f"python3 ./code/regular.py {file} {mode} {year}")
        os.system(f"python3 ./code/userDataPic.py {file} {mode} {year}")
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
    cutType = cutFile[:cutFile.find(".csv")]
    year = int(input("Please enter the year: "))
    createFile("./image")
    createFile(f"./image/{year}")
    singleContrast(modeList[userSelect],cutType,year)