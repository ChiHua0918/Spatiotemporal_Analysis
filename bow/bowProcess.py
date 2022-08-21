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
# BOW — raster scan (filter 分數的累加)
def AccumulateScore(size):
    # source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    source = ["GEI_origin","GEI_level"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/bowAccumulateScore.py {file} {size}")
        os.system(f"python3 ./code/bowAccumulateScore.py {file} {size}")
    return "accumulate"
# BOW — 四個象限 (filter 分數的累加)
def bowQuadrantAccumulate(size):
    # source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    source = ["GEI_origin","GEI_level"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/bowQuadrantAccumulate.py {file} {size}")
        os.system(f"python3 ./code/bowQuadrantAccumulate.py {file} {size}")
    return "quadrantAccumulate"
# BOW — 分四個象限（象限分數）
def bowQuadrantScore(size):
    # source = ["GEI_origin_regular.csv","GEI_Level_regular.csv"]
    source = ["GEI_origin","GEI_level"]
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/bowQuadrantScore.py {file} {size}")
        os.system(f"python3 ./code/bowQuadrantScore.py {file} {size}")
    return "quadrantScore"
# 階層式分析
def hierarchical(folder,size):
    source = ["GEI_origin","GEI_level"]
    for data in source:
        print(f"python3 ./code/Hierarchical.py {folder} {data} {size}")
        os.system(f"python3 ./code/Hierarchical.py {folder} {data} {size}")
        print(f"python3 ./code/decideClusterNum.py {folder} {data} {size}")
        os.system(f"python3 ./code/decideClusterNum.py {folder} {data} {size}")

# 階層式分析 --- 決定要分多少群
# def decideHierarchical(folder,size):
#     source = ["GEI_origin_bow","GEI_Level_bow"]
#     filterType = ["_col","_row","_leftDown","_rightDown"]
#     for dataType in filterType:
#         for data in source:
#             fileName = f"{data+'_'+str(size)+dataType}"+".csv"
#             path = f"./data/{folder}/{fileName}"
#             print(f"python3 ./code/decideClusterNum.py {path} {fileName}")
#             os.system(f"python3 ./code/decideClusterNum.py {path} {fileName}")
def main():
    size = input("請輸入 filter 大小(輸入數字為整數):")
    # folder = AccumulateScore(size)
    # folder = bowQuadrantAccumulate(size)
    folder = bowQuadrantScore(size)
    # cluster(size,folder)
    hierarchical(folder,size)
    # decideHierarchical(folder,size)
if __name__ == '__main__':
    main()