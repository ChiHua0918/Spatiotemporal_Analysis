import os

# 將原始 PM2.5 數據轉為等級
def bow():
    source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python ./code/covertToLevel.py {file}")
        os.system(f"python ./code/covertToLevel.py {file}")

def main():
    bow()
if __name__ == '__main__':
    main()