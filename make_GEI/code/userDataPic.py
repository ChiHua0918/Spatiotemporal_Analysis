import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
# import pandas as pd
import csv
import sys
# from collections import defaultdict
# import matplotlib.colors
# import sys
# import time

def segment(data):
    replaceNum = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    data = int(float(data))
    # 16進位
    num = replaceNum[data//16]+replaceNum[data%16]
    color = "#"+num+num+num
    return color
    # if data == -1:
    #     return 'white'
    # elif data < 7.5:
    #     return 'lightgreen'
    # elif data > 7.4 and data < 15.5:
    #     return 'LightSeaGreen'
    # elif data > 15.4 and data < 25.5:
    #     return 'lightyellow'
    # elif data > 25.4 and data < 35.5:
    #     return 'yellow'
    # elif data > 35.4 and data < 45.5:
    #     return 'orange'
    # elif data > 45.4 and data < 54.5:
    #     return 'darkorange'
    # elif data > 54.4 and data < 102.5:
    #     return 'IndianRed'
    # elif data > 102.4 and data < 150.5:
    #     return 'red'
    # elif data > 150.4 and data < 250.5:
    #     return 'purple'
    # else:
    #     return 'brown'

def drawColor(GEI,cutType,folder,year):
    ax = plt.subplot(111)
    name = GEI[0] #name
    name = name.replace("/","-")
    name = name.replace(":","-")
    name = name.replace(" ","-")
    data = GEI[3:] #data
    tmp = data
    for j in range(len(tmp)):
        if tmp[j] > 255:
            tmp[j] = 255
        x = np.linspace(10 * int((j%10)), 10 * int((j%10)) + 10, 10)
        ax.fill_between(x,90 - 10 * int((j/10)), 100 - 10 * int((j/10)), facecolor = segment(tmp[j]))
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    ax.xaxis.set_major_locator(MultipleLocator(10)) # 數字間隔 10
    ax.yaxis.set_major_locator(MultipleLocator(10)) # 設定 y 數字間隔 10
    ax.xaxis.grid(False,which='major') # major,color='black'
    ax.yaxis.grid(False,which='major') # major,color='black'
    ax.xaxis.set_ticks([]) # 去掉外標線
    ax.yaxis.set_ticks([])
    plt.axis('off')
    # now = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
    # now = time.strftime("%Y-%m-%d-%H-%M", time.localtime())
    # date = date.replace('/','-').replace(' ','-').replace(':','-')
    # plt.savefig(f"./picture/{folder}/{name}.png", bbox_inches='tight',pad_inches = 0)
    plt.savefig(f"./picture/{year}/{cutType}/{folder}/{name}.png", bbox_inches='tight',pad_inches = 0)
    plt.cla()
    plt.clf()
    return name

def main(inputData,cutFile,year):
    cutType = cutFile[:cutFile.find(".csv")]
    path = f"./data/GEI_regular/{year}/{cutType}/{inputData}"
    readData = []
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        next(rows)
        for row in rows :
            readData.append(row[:3]+list(map(float,row[3:])))
    index = inputData.find('.csv')
    folder = inputData[:index]
    # folder = "PM2.5數據灰階圖"
    for GEI in readData:
        print(drawColor(GEI,cutType,folder,year))
    print("======= userDataPic.py 完成 =======")
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3])
    # main("../2018micro.csv")