import os
# 分群
def cluster(size,folder):
    source = [f"GEI_origin_{size}",f"GEI_level_{size}"]
    # source = [f"GEI_origin_bow_{size}_col.csv",f"GEI_Level_bow_{size}_col.csv"
    #          ,f"GEI_origin_bow_{size}_row.csv",f"GEI_Level_bow_{size}_row.csv"
    #          ,f"GEI_origin_bow_{size}_leftDown.csv",f"GEI_Level_bow_{size}_leftDown.csv"
    #          ,f"GEI_origin_bow_{size}_rightDown.csv",f"GEI_Level_bow_{size}_rightDown.csv"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/cluster.py {file} {folder}")
        os.system(f"python3 ./code/cluster.py {file} {folder}")
# V累加 filter 分數，所有的 filter 一起累計
def AccumulateScore(size):
    # source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    source = ["GEI_origin","GEI_level"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/bowAccumulateScore.py {file} {size}")
        os.system(f"python3 ./code/bowAccumulateScore.py {file} {size}")
    return "accumulate"
# filter 經過圖片後
def strengthenEdge(size):
    source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/bowStrengthenEdge.py {file} {size}")
        os.system(f"python3 ./code/bowStrengthenEdge.py {file} {size}")
    return "strengthenEdge"
# =================================
# 分 4 個象限，每一個象限產生一個分數，每一個 filter 以這 4 個象限分數做分群
def bowAccumulate(size):
    # source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    source = ["GEI_origin.csv","GEI_level.csv"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/bowAccumulate.py {file} {size}")
        os.system(f"python3 ./code/bowAccumulate.py {file} {size}")
    return "accumulate"
# V
def bowQuadrantScore(size):
    # source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    source = ["GEI_origin","GEI_level"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/bowQuadrantScore.py {file} {size}")
        os.system(f"python3 ./code/bowQuadrantScore.py {file} {size}")
    return "quadrantScore"
# V4 個象限計算各 filter 分數
def bowQuadrantAccumulate(size):
    # source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    source = ["GEI_origin","GEI_level"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/bowQuadrantAccumulate.py {file} {size}")
        os.system(f"python3 ./code/bowQuadrantAccumulate.py {file} {size}")
    return "quadrantAccumulate"
# 階層式分析
def hierarchical(folder,size):
    source = ["GEI_origin_bow","GEI_Level_bow"]
    filterType = ["_col","_row","_leftDown","_rightDown"]
    for dataType in filterType:
        for data in source:
            file = f"./data/{folder}/{data+'_'+str(size)+dataType}"+".csv"
            print(f"python3 ./code/Hierarchical.py {file}")
            os.system(f"python3 ./code/Hierarchical.py {file}")
# 階層式分析 --- 決定要分多少群
def decideHierarchical(folder,size):
    source = ["GEI_origin_bow","GEI_Level_bow"]
    filterType = ["_col","_row","_leftDown","_rightDown"]
    for dataType in filterType:
        for data in source:
            fileName = f"{data+'_'+str(size)+dataType}"+".csv"
            path = f"./data/{folder}/{fileName}"
            print(f"python3 ./code/decideClusterNum.py {path} {fileName}")
            os.system(f"python3 ./code/decideClusterNum.py {path} {fileName}")
def main():
    size = input("請輸入 filter 大小(輸入數字為整數):")
    # folder = AccumulateScore(size)
    # folder = bowQuadrantAccumulate(size)
    # folder = bowQuadrantScore(size)
    # cluster(size,folder)
    # ====== 以下未整理 ======
    # folder = strengthenEdge(size) # 每一個 filter 分數分開
    # ===========================
    # folder = bowAccumulate(size)
    folder = "accumulate"
    hierarchical(folder,size)
    # decideHierarchical(folder,size)
if __name__ == '__main__':
    main()