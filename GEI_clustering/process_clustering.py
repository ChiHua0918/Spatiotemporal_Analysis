# GEI 分群
# ------------------
import os
def createFile(path):
    if os.path.isdir(path) == False:
        os.system("mkdir "+ path)
def cnn(data,cutType,year):
    createFile("./cnn/data")
    createFile(f"./cnn/data/{year}")
    createFile(f"./cnn/data/{year}/imagenet")
    createFile(f"./cnn/data/{year}/imagenet/{cutType}")
    createFile(f"./clustering/{year}")
    createFile(f"./clustering/{year}/{cutType}")
    createFile(f"./clustering/{year}/{cutType}/cnn")
    createFile(f"./clustering/{year}/{cutType}/cnn/imagenet")
    for file in data:
        file = file[:file.index(".csv")]
        print(f"python3 ./cnn/code/cnn.py {file} imagenet {cutType} {year}")
        os.system(f"python3 ./cnn/code/cnn.py {file} imagenet {cutType} {year}")
        print(f"python3 ./cnn/code/cluster.py {file} imagenet {cutType} {year}")
        os.system(f"python3 ./cnn/code/cluster.py {file} imagenet {cutType} {year}")
def bow(cutType,year):
    createFile(f"./bow/data")
    createFile(f"./bow/data/{year}")
    createFile(f"./bow/data/{year}/{cutType}")
    createFile(f"./clustering/{year}")
    createFile(f"./clustering/{year}/{cutType}")
    createFile(f"./clustering/{year}/{cutType}/bow")
    print(f"python3 ./bow/bowProcess.py {cutType}")
    os.system(f"python3 ./bow/bowProcess.py {cutType} {year}")
def histogram(data,cutFile,cutType,year):
    createFile("./histogram")
    createFile("./histogram/data")
    createFile(f"./histogram/data/countLevelNum")
    createFile(f"./histogram/data/countLevelNum/{year}")
    createFile(f"./histogram/data/countLevelNum/{year}/{cutType}")
    # begin: 2018micro.csv 數據分群（目的為切 cut & shot） regular: 已正規化的數據
    form = "regular"
    # GEI 正規化後(0~255)的數據
    for file in data:
        print(f"python3 ../make_GEI/code/countLevelNum.py {file} {cutFile} {form} {year}")
        os.system(f"python3 ../make_GEI/code/countLevelNum.py {file} {cutFile} {form} {year}")
    # data = ["GEI_origin_regular_countNum.csv","GEI_Level_regular_countNum.csv"]
    createFile(f"./clustering/{year}/{cutType}")
    createFile(f"./clustering/{year}/{cutType}/histogram")
    for file in data:
        print(f"python3 ../make_GEI/code/cluster.py {file} {cutFile} {form} {year}")
        os.system(f"python3 ../make_GEI/code/cluster.py {file} {cutFile} {form} {year}")

def main():
    data = ["GEI_origin.csv","GEI_level.csv"]
    cutFile = input("(KMeans.csv、HCED1.csv、RasterScan4.csv)\ncut file = ") # cut.csv、HCED1.csv、RasterScan4.csv
    cutType = cutFile[:cutFile.find(".csv")]
    year = int(input("Please enter the year: "))
    createFile("./clustering")
    # cluster
    histogram(data,cutFile,cutType,year)
    bow(cutType,year)
    cnn(data,cutType,year)

if __name__ == '__main__':
    if os.path.exists(f"./clustering") == False:
        os.system(f"mkdir ./clustering")
    main()