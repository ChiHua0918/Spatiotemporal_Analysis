# import imageio.v3 as iio
import imageio
import csv
import os

# 找要疊加的圖片
def findPictureName(id):
    # 要疊加的照片
    statckList = []
    order = 0
    print("GEI ID:",id)
    for data in cut_shot:
        # cut
        if data[1] == 1 and statckList != []:
            if order == id:
                break
            order += 1
            statckList.clear()
        # shot
        elif data[1] == 0:
            # data[0]: 彩色 PM2.5 圖片名字
            statckList.append(data[0])
    return statckList
def makeGif(cutType,id,speed,year):
    # 要疊成 gif 的圖片
    stackList = findPictureName(id)
    path = f"./image/{year}/{cutType}/{id}.gif"
    images = []
    for filename in stackList:
        filename = filename.replace("/","-")
        filename = filename.replace(" ","-")
        filename = filename.replace(":","-")
        filename += ".png"
        images.append(imageio.imread("../../sis/"+filename))
    imageio.mimsave(path,images,duration=speed)
    '''
    with imageio.get_writer(path, mode='I',fps=speed) as writer:
        for filename in stackList:
            filename = filename.replace("/","-")
            filename = filename.replace(" ","-")
            filename = filename.replace(":","-")
            filename += ".png"
            image = imageio.imread("../../sis/"+filename)
            writer.append_data(image)
    '''

def main(cutType,file,sourceCut,year):
    global cut_shot
    # cut and shot
    cut_shot = []
    with open("../../make_GEI/"+sourceCut, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                cut_shot.append([row[0]]+list(map(int,row[1:])))
            except:
                pass
    # GEI 數量
    with open(f"../../make_GEI/data/{year}/GEI_data/{cutType}/{file}.csv", newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        GEINum = len(list(rows))-1 # -1: 去掉標題

    for id in range(GEINum):
        makeGif(cutType,id,1,year)
def createFile(path):
    if os.path.isdir(path) == False:
        os.system("mkdir "+ path)
if __name__ == "__main__":
    # gif 存放在哪一個資料夾
    file = "GEI_origin"
    sourceCut = input("(KMenas.csv、HCED1.csv、RasterScan4.csv)\ncut file = ")# "KMeans.csv"
    cutType = sourceCut[:sourceCut.find(".csv")]
    year = int(input("Please enter the year: "))
    createFile("./image")
    createFile(f"./image/{year}")
    createFile(f"./image/{year}/{cutType}")
    main(cutType,file,sourceCut,year)