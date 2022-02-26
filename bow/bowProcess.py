import os

# 分群
def cluster(size):
    source = [f"GEI_origin_bow_{size}.csv",f"GEI_Level_bow_{size}.csv"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python ./code/cluster.py {file}")
        os.system(f"python ./code/cluster.py {file}")
# 將原始 PM2.5 數據轉為等級
def bow(size):
    source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python ./code/bow.py {file} {size}")
        os.system(f"python ./code/bow.py {file} {size}")
def main():
    print("請輸入 filter 大小(輸入數字為整數):",end = " ")
    size = int(input())
    bow(size)
    cluster(size)
if __name__ == '__main__':
    main()