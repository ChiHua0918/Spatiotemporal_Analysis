import os

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
    for data in source:
        # os.system(f"python cnn.py {data} imagenet")
        file = data+"_cnn.csv"
        print(f"python ./code/cluster.py {file} imagenat")
        os.system(f"python ./code/cluster.py {file} imagenet")

def main():
    cnn()
if __name__ == '__main__':
    main()