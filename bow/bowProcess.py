import os
# 分群
def cluster(size,folderList):
    source = [f"GEI_origin_{size}",f"GEI_level_{size}"]
    for folder in folderList:
        for file in source:
            # path = "../make_GEI/data/GEI_regular/"
            print(f"python3 ./code/cluster.py {file} {folder}")
            os.system(f"python3 ./code/cluster.py {file} {folder}")
# BOW — raster scan (filter 分數的累加)
def AccumulateScore(source,size):
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/bowAccumulateScore.py {file} {size}")
        os.system(f"python3 ./code/bowAccumulateScore.py {file} {size}")
    return "accumulate"
# BOW — 四個象限 (filter 分數的累加)
def bowQuadrantAccumulate(source,size):
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/bowQuadrantAccumulate.py {file} {size}")
        os.system(f"python3 ./code/bowQuadrantAccumulate.py {file} {size}")
    return "quadrantAccumulate"
# BOW — 分四個象限（象限分數）
def bowQuadrantScore(source,size):
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./code/bowQuadrantScore.py {file} {size}")
        os.system(f"python3 ./code/bowQuadrantScore.py {file} {size}")
    return "quadrantScore"
# 階層式分析
def hierarchical(source,folder,size):
    for data in source:
        print(f"python3 ./code/Hierarchical.py {folder} {data} {size}")
        os.system(f"python3 ./code/Hierarchical.py {folder} {data} {size}")
        print(f"python3 ./code/decideClusterNum.py {folder} {data} {size}")
        os.system(f"python3 ./code/decideClusterNum.py {folder} {data} {size}")

# 階層式分析 --- 決定要分多少群
# def decideHierarchical(source,folder,size):
#     filterType = ["_col","_row","_leftDown","_rightDown"]
#     for dataType in filterType:
#         for data in source:
#             fileName = f"{data+'_'+str(size)+dataType}"+".csv"
#             path = f"./data/{folder}/{fileName}"
#             print(f"python3 ./code/decideClusterNum.py {path} {fileName}")
#             os.system(f"python3 ./code/decideClusterNum.py {path} {fileName}")
def main():
    source = ["GEI_origin","GEI_level"]
    size = input("請輸入 filter 大小(輸入數字為整數):")
    folderList = []
    folderList.append(AccumulateScore(source,size))
    folderList.append(bowQuadrantAccumulate(source,size))
    folderList.append(bowQuadrantScore(source,size))
    cluster(size,folderList)
    # hierarchical(source,folder,size)
    # ===== 未整理 =====
    # decideHierarchical(source,folder,size)
if __name__ == '__main__':
    main()