import os
def main():
    print("GEI_origin_regular.csv、GEI_origin_average_regular.csv、GEI_Level_regular.csv、GEI_Level_average_regular.csv")
    # 計算格子數
    os.system("python ./code/CountLevelNum.py")
    # 分類
    os.system("python ./code/classify.py")
if __name__ == '__main__':
    main()