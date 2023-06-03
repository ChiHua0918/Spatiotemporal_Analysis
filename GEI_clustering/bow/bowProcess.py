import os
import sys

def createFile(path):
    if os.path.isdir(path) == False:
        os.system("mkdir "+ path)
# 分群
def cluster(size,folderList,cutType,year):
    source = [f"GEI_origin_{size}",f"GEI_level_{size}"]
    for folder in folderList:
        createFile(f"./clustering/{year}/{cutType}/bow/{folder}")
        for file in source:
            print(f"python3 ./bow/code/cluster.py {file} {folder} {cutType} {year}")
            os.system(f"python3 ./bow/code/cluster.py {file} {folder} {cutType} {year}")
# BOW — raster scan (filter 分數的累加)
def AccumulateScore(source,size,cutType,year):
    createFile(f"./bow/data/{year}/{cutType}/accumulate")
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./bow/code/bowAccumulateScore.py {file} {size} {cutType} {year}")
        os.system(f"python3 ./bow/code/bowAccumulateScore.py {file} {size} {cutType} {year}")
    return "accumulate"
# BOW — 四個象限 (filter 分數的累加)
def bowQuadrantAccumulate(source,size,cutType,year):
    createFile(f"./bow/data/{year}/{cutType}/quadrantAccumulate")
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./bow/code/bowQuadrantAccumulate.py {file} {size} {cutType} {year}")
        os.system(f"python3 ./bow/code/bowQuadrantAccumulate.py {file} {size} {cutType} {year}")
    return "quadrantAccumulate"
# BOW — 分四個象限（象限分數）
def bowQuadrantScore(source,size,cutType,year):
    createFile(f"./bow/data/{year}/{cutType}/quadrantScore")
    for file in source:
        # path = "../make_GEI/data/GEI_regular/"
        print(f"python3 ./bow/code/bowQuadrantScore.py {file} {size} {cutType} {year}")
        os.system(f"python3 ./bow/code/bowQuadrantScore.py {file} {size} {cutType} {year}")
    return "quadrantScore"
# 階層式分析
def hierarchical(source,folderList,size,cutType,year):
    createFile(f"./clustering/{cutType}/bow/quadrantScoreDecideNum")
    for folder in folderList:
        for data in source:
            print(f"python3 ./bow/code/Hierarchical.py {folder} {data} {size} {cutType} {year}")
            os.system(f"python3 ./bow/code/Hierarchical.py {folder} {data} {size} {cutType} {year}")
            print(f"python3 ./bow/code/decideClusterNum.py {folder} {data} {size} {cutType} {year}")
            os.system(f"python3 ./bow/code/decideClusterNum.py {folder} {data} {size} {cutType} {year}")

def main(cutType,year):
    source = ["GEI_origin","GEI_level"]
    size = input("請輸入 filter 大小(輸入數字為整數):")
    folderList = []
    # folderList.append(AccumulateScore(source,size,cutType,year))
    folderList.append(bowQuadrantAccumulate(source,size,cutType,year))
    folderList.append(bowQuadrantScore(source,size,cutType,year))
    cluster(size,folderList,cutType,year)
    # hierarchical(source,folderList,size,cutType,year)
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])