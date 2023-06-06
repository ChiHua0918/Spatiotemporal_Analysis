import sys
import csv
# cut 和 cut 之間沒有達到目標數量 -> 全變為 cut
def cut(readData,least):
    cut_shot = [] # 放 cut 、 shot
    precluster = readData[0][1] # 前一張的所屬分群
    shotNum = 0 # 目前所檢查的片段， shot 有多少張 
    for img in readData:
        cut_shot.append([img[0],0]) # [image name,cut or shot] (0: shot, 1:cut)
        shotNum += 1
        # shot 不足 3 張 -> 變為 cut
        if img[1] != precluster and shotNum <= least:
            # 所有變成 cut
            start = len(cut_shot)-shotNum
            end = len(cut_shot)
            for i in range(start,end):
                cut_shot[i][1] = 1
            precluster = img[1]
            shotNum = 0
        # cut:和前一張的分群不同，"此張"變 cut
        elif img[1] != precluster:
            precluster = img[1]
            cut_shot[len(cut_shot)-1][1] = 1
            shotNum = 0
    return cut_shot
def main(inputData,year):
    inputFile = f"./data/clustering/{year}/{inputData}"
    readData = []
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append([row[0],float(row[1])])
            except:
                pass
    print("shot 數量至少為(請填入整數):",end = " ")
    least = int(input())
    cut_shot = cut(readData,least)
    print("number of source:",len(readData))
    print("number of output:",len(cut_shot))
    # with open(f"cut~{least}.csv", 'w', newline='') as _file:
    with open(f"KMeans.csv", 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","cut_shot"])
        writer.writerows(cut_shot)
    print("======= cut.py 完成 =======")
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])