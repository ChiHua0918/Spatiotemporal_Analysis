import os

# 將原始 PM2.5 數據轉為等級
def cnn():
    # source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    source = ["GEI_origin","GEI_level"]
    # outputFolder = ["imagenet","mnist"]
    # for i in range(len(outputFolder)):
    #     for j in range(len(source)):
    #         print(f"python cnn.py {source[j]} {outputFolder[i]}")
    #         os.system(f"python cnn.py {source[j]} {outputFolder[i]}")
    for file in source:
        print(f"python3 ./code/cnn.py {file} imagenet")
        os.system(f"python3 ./code/cnn.py {file} imagenet")
        print(f"python3 ./code/cluster.py {file} imagenet")
        os.system(f"python3 ./code/cluster.py {file} imagenet")

def main():
    cnn()
if __name__ == '__main__':
    main()