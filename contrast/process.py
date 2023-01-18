import os
# GEI 分群
def singleContrast():
    # GEI 正規化後(0~255)的數據
    # data = ["GEI_origin.csv","GEI_level.csv"]
    # for file in data:
    #     print(f"python3 ./code/regular.py {file}")
    #     os.system(f"python3 ./code/regular.py {file}")
    # drawData = ["GEI_origin_singleRegular.csv","GEI_level_singleRegular.csv"]
    # for file in drawData:
    #     print(f"python3 ./code/userDataPic.py {file}")
    #     os.system(f"python3 ./code/userDataPic.py {file}")
    # 給采禎的每小時 PM2.5 加強對比圖
    # file = "2018micro.csv"
    # os.system(f"python3 ./code/regular.py {file}")
    file = "2018micro_singleRegular.csv"
    os.system(f"python3 ./code/userDataPic.py {file}")
singleContrast()