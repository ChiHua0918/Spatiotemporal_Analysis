from fileinput import filename
import os
# 分群
def cluster(size,folder):
    # source = [f"GEI_origin_bow_{size}.csv",f"GEI_Level_bow_{size}.csv"]
    source = [f"GEI_origin_bow_{size}_col.csv",f"GEI_Level_bow_{size}_col.csv"
             ,f"GEI_origin_bow_{size}_row.csv",f"GEI_Level_bow_{size}_row.csv"
             ,f"GEI_origin_bow_{size}_leftDown.csv",f"GEI_Level_bow_{size}_leftDown.csv"
             ,f"GEI_origin_bow_{size}_rightDown.csv",f"GEI_Level_bow_{size}_rightDown.csv"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python ./code/cluster.py {file} {folder}")
        os.system(f"python ./code/cluster.py {file} {folder}")
# 累加 filter 分數
def AccumulateScore(size):
    source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python ./code/bowAccumulateScore.py {file} {size}")
        os.system(f"python ./code/bowAccumulateScore.py {file} {size}")
    return "accumulate"
# filter 經過圖片後
def strengthenEdge(size):
    source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python ./code/bowStrengthenEdge.py {file} {size}")
        os.system(f"python ./code/bowStrengthenEdge.py {file} {size}")
    return "strengthenEdge"
def bowFilterScore(size):
    source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python ./code/bowFilterScore.py {file} {size}")
        os.system(f"python ./code/bowFilterScore.py {file} {size}")
# 4 個象限計算各 filter 分數
def bowFilterScore_quadrant(size):
    source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python ./code/bowFilterScore_quadrant.py {file} {size}")
        os.system(f"python ./code/bowFilterScore_quadrant.py {file} {size}")
    return "quadrant"
# 階層式分析
def hierarchical(folder,size):
    source = ["GEI_origin_bow","GEI_Level_bow"]
    filterType = ["_col","_row","_leftDown","_rightDown"]
    for dataType in filterType:
        for data in source:
            file = f"./data/{folder}/{data+'_'+str(size)+dataType}"+".csv"
            print(f"python ./code/Hierarchical.py {file}")
            os.system(f"python ./code/Hierarchical.py {file}")
# 階層式分析 --- 決定要分多少群
def decideHierarchical(folder,size):
    source = ["GEI_origin_bow","GEI_Level_bow"]
    filterType = ["_col","_row","_leftDown","_rightDown"]
    for dataType in filterType:
        for data in source:
            fileName = f"{data+'_'+str(size)+dataType}"+".csv"
            path = f"./data/{folder}/{fileName}"
            print(f"python ./code/decideClusterNum.py {path} {fileName}")
            os.system(f"python ./code/decideClusterNum.py {path} {fileName}")
def main():
    print("請輸入 filter 大小(輸入數字為整數):",end = " ")
    size = int(input())
    # folder = AccumulateScore(size)
    # folder = strengthenEdge(size) # 每一個 filter 分數分開
    # folder = bowFilterScore(size)
    # folder = bowFilterScore_quadrant(size)
    # cluster(size,folder)
    folder = "quadrant"
    # hierarchical(folder,size)
    decideHierarchical(folder,size)
if __name__ == '__main__':
    main()