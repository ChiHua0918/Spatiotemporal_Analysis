import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
import csv
import sys


def segment(data):
    replaceNum = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    data = int(float(data))
    # 16進位
    num = replaceNum[data//16]+replaceNum[data%16]
    color = "#"+num+num+num
    return color
# GEI：GEI 數據, folder: 存放圖片的位置
def drawColor(GEI,folder):
    ax = plt.subplot(111)
    name = GEI[0] #name
    data = GEI[1:] #data
    tmp = data
    for j in range(len(tmp)):
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
    plt.savefig(f"./static/image/{folder}/{name}.png", bbox_inches='tight',pad_inches = 0)
    plt.cla()
    plt.clf()
    return name
    # plt.show()

# def main(inputData):
#     # print(len(argv))
#     global plt
#     inputFile =  "./static/data/"+inputData
#     # inputFile =  "./static/data/GEI_regular/"+inputData
#     readData = []
#     with open(inputFile, newline= '') as csvfile :
#         rows = csv.reader(csvfile, delimiter = ',')
#         for row in rows :
#             try:
#                 readData.append([row[0]]+list(map(float,row[1:])))
#             except:
#                 pass
#     # index = inputData.find('_regular')
#     index = inputData.find('.csv')
#     folder = inputData[:index]
#     for GEI in readData:
#         print(drawColor(GEI,folder))

# if __name__ == '__main__':
#     # main(sys.argv[1:])
#     main(sys.argv[1])