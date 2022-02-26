import os

from numpy import source
# 將原始 PM2.5 數據轉為等級
def cnn():
    # source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    # source = ["GEI_origin","GEI_Level"]
    # outputFolder = ["imagenet","mnist"]
    source = ["GEI_origin","GEI_Level"]
    outputFolder = ["imagenet","mnist"]
    # for i in range(len(outputFolder)):
    #     for j in range(len(source)):
    #         print(f"python cnn.py {source[j]} {outputFolder[i]}")
    #         os.system(f"python cnn.py {source[j]} {outputFolder[i]}")
    os.system(f"python cnn.py GEI_origin mnist")

def main():
    cnn()
if __name__ == '__main__':
    main()