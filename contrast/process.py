import os
# GEI 分群
def singleContrast():
    # GEI 正規化後(0~255)的數據
    data = ["GEI_origin.csv","GEI_Level.csv"]
    for file in data:
        print(f"python ./code/regular.py {file}")
        os.system(f"python ./code/regular.py {file}")
    drawData = ["GEI_origin_singleRegular.csv","GEI_Level_singleRegular.csv"]
    for file in drawData:
        print(f"python ./code/userDataPic.py {file}")
        os.system(f"python ./code/userDataPic.py {file}")

singleContrast()