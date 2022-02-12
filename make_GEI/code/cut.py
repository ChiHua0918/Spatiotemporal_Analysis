import sys
import csv
# cut 和 cut 之間沒有達到目標數量 -> 全變為 cut
def cut(readData,shotNum):
    cut_shot = [] # 放 cut 、 shot
    shot = 0 # 多少張 shot
    precluster = readData[0][1] # 前一張的所屬分群
    tmp = []
    for img in readData:
        # shot
        shot += 1
        cut_shot.append([img[0],0])
        # shot 不足 3 張 -> 變為 cut
        if shot < shotNum and img[1] != precluster:
            # 所有變成 cut
            start = len(cut_shot)-shot
            end = len(cut_shot)
            for i in range(start,end):
                cut_shot[i][1] = 1
            shot = 0
            precluster = img[1]
            tmp.clear()
            # print("cut",img[0])
            continue
        # cut:和前一張的分群不同，"此張"變 cut
        elif img[1] != precluster:
            precluster = img[1]
            cut_shot[len(cut_shot)-1][1] = 1
            shot = 0
            tmp.clear()
            # print("single cut",img[0])
            continue

    return cut_shot
def main(argv):
    inputData = argv
    inputFile = "./data/clustering/"+inputData
    readData = []
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append([row[0],float(row[1])])
            except:
                pass
    print("shot 數量至少為(請填入整數):",end = " ")
    cut_shot = cut(readData,int(input()))
    print("來源數據長度:",len(readData))
    print("輸出數據長度:",len(cut_shot))
    with open("cut~3.csv", 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","cut_shot"])
        writer.writerows(cut_shot)
    print("cut.py 完成")
if __name__ == "__main__":
    main(sys.argv[1])