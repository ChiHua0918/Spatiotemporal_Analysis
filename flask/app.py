from flask import Flask, render_template, request, send_from_directory
import os
import csv
import imageio
import numpy as np
from make_clusterUI.userDataPic import drawColor

app = Flask(__name__)

#通過python3裝飾器的方法定義路由地址
@app.route("/")
#定義方法 用jinjia2引擎來渲染頁面，并回傳一個index.html頁面
def root():
    return render_template("show.html",title="Browse By Cluster")
@app.route("/bbg")
def bbg():
    return render_template("bbg.html",title="Browse By GEI")
@app.route("/bbc")
def bbc():
    return render_template("bbc.html",title="Browse By Cluster")
@app.route("/qbgResult",methods = ["GET","POST"])
def qbgResult():
    if request.method == 'POST':
        selectName = request.form.get("selectName")
        GEIfolder = request.form.get("GEIfolder")
        dataYear = request.form.get("dataYear")
        cutType = request.form.get("cutType")
        print("method:POST")
    else:
        selectName = "NO.0"
        GEIfolder = "GEI_origin"
        dataYear = 2018
        cutType = "KMeans"
        print("method:GET")
    print("selectName:",selectName)
    print("GEIfolder:",GEIfolder)
    print("cutType:",cutType)
    rankResult = directQBG(selectName,GEIfolder,cutType)
    # 排名結果的第一名一定是使用者選擇的 GEI
    # GEIRankData = rankResult[1:]
    GEIRankData = dict()
    for i in range(len(rankResult)):
        GEIRankData[i] = rankResult[i].replace(",","").replace("'","").replace(":00","H").split()
    print("=======================\nGEIRankData")
    start = GEIRankData[0][2]+" "+GEIRankData[0][3]
    end = GEIRankData[0][4]+" "+GEIRankData[0][5]
    return render_template("qbgResult.html",sourceImageName = selectName+".png",\
                                            sourceDataset = GEIfolder,\
                                            GEIRankData = GEIRankData,\
                                            dataYear = dataYear,\
                                            cutType = cutType,\
                                            start = start,\
                                            end = end)
# =========== 婷誼的部份 =============
@app.route("/shot")
def home():
    return render_template("index.html")
# 讀取csv獲取每一張 GEI 所屬的群
@app.route("/readFile",methods = ["POST"])
def readFile():
    # 從前端拿到的資料
    path = request.form.get("path")
    cut_shot = [] # 0: shot, 1:cut
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        next(rows)
        for row in rows :
            cut_shot.append(int(row[0]))
    return {"data":cut_shot}
# 計算 GEI 的排名
# @app.route("/directQBG",methods = ["GET"])
def directQBG(selectName,GEIfolder,cutType):
    print(cutType)
    command = "python3 rasterScan_D_GEI.py " + selectName +" "+cutType
    print(GEIfolder)
    print(command)
    # 建立 process，將執行結果用 readlines 讀取
    rankResult = os.popen(command).readlines()
    return rankResult
# ================================
# 現在GEI的數量
@app.route("/GEINum",methods=["GET"])
def GEINum():
    cutType = request.args.get("cutType")
    dataYear = request.args.get("dataYear")
    path = f"./static/image/GEI/{dataYear}/{cutType}/GEI_origin"
    GEIName = os.listdir(path)
    return {"num":len(GEIName)}
    # return {"num":2}

# 讀取csv獲取每一張 GEI 所屬的群
@app.route("/cluster",methods = ["GET"])
def cluster():
    # 從前端拿到的資料
    dataYear = request.args.get("dataYear")
    cutType = request.args.get("cutType")
    sourceDataset = request.args.get("sourceDataset")
    clusterFile = request.args.get("clusterFile")
    filterSize = request.args.get("filterSize")
    print(f"sourceDataset:{sourceDataset} clusterFile:{clusterFile} filterSize:{filterSize}")
    if clusterFile == "histogram":
        path = f"./static/data/clustering/{dataYear}/{cutType}/histogram/{sourceDataset}.csv"
    elif clusterFile.split('_')[0] == "bow":
        folder = clusterFile.split('_')[1]
        path = f"./static/data/clustering/{dataYear}/{cutType}/bow/{folder}/{sourceDataset}_{filterSize}.csv"
    elif clusterFile.split('_')[0] == "cnn":
        folder = folder = clusterFile.split('_')[1] # imagenet
        path = f"./static/data/clustering/{dataYear}/{cutType}/cnn/{folder}/{sourceDataset}_imagenet.csv"
    cluster = [] # GEI 所屬群
    GEIName = [] # GEI 名字
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try: # 防止加到標題
                cluster.append(int(row[1])) # GEI 所屬群，如果是標題就會是字串
                GEIName.append(row[0])
            except:
                pass
    k = max(cluster)
    tmp = cluster.copy()
    clusterUI(tmp,sourceDataset,cutType,dataYear)
    return {"cluster":cluster,"GEIName":GEIName,"maxCluster":k}
# 製作每一群的代表 GEI
def clusterUI(cluster,sourceDataset,cutType,dataYear):
    # 每一群所有 GEI 堆疊成一個代表的 GEI
    print("make clusterUI")
    readData = []
    with open(f"./static/data/GEI_regular/{dataYear}/{cutType}/{sourceDataset}.csv", newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        next(rows) # 跳過標題
        for row in rows :
            readData.append(list(map(float,row[3:])))
    # print("cluster length",len(cluster))
    # print("readData length",len(readData))
    clusterData = []
    # print("num",max(cluster))
    # print("cluster",cluster)
    for k in range(max(cluster)+1):
        # 堆疊的 GEI 數據
        stackData = np.zeros(len(readData[0]))
        # 堆疊的張數
        n = 0
        while k in cluster:
            n += 1
            # 找對應群的 GEI
            pos = cluster.index(k)
            stackData += readData[pos]
            # 把剛剛已經加到 stackList 的 GEI 移除
            cluster.pop(pos)
            readData.pop(pos)
        # 名字
        stackData = stackData / n
        stackData = stackData.tolist()
        stackData.insert(0,k)
        # print("k",k)
        # print("n",n)
        # print("stackData",stackData)
        clusterData.append(stackData)
        print(drawColor(stackData,"clusterUI"))
    print("cluster UI 繪製完成")
# 動態圖片
@app.route("/dynamicImage",methods=["GEI"])
def dynamicImage():
    directory = request.args.get("directory")
    path = request.args.get("path")
    return send_from_directory(directory, path)
#app的路由地址"/submit"即為ajax中定義的url地址，采用POST、GET方法均可提交
@app.route("/gif",methods=["GET"])
# 顯示連續彩色PM2.5空汙圖
def gif():
    cutType = request.args.get("cutType") # GEI id
    id = request.args.get("id") # GEI id
    speed = request.args.get("speed") # gif 速度
    # 要疊成 gif 的圖片
    stackList = findPictureName(id,cutType)
    images = []
    path = f"./static/image/gif/{id}.gif"
    for filename in stackList:
        filename = filename.replace("/","-")
        filename = filename.replace(" ","-")
        filename = filename.replace(":","-")
        filename += ".png"
        images.append(imageio.imread("./static/image/sis/"+filename))
    imageio.mimsave(path,images,duration=speed)
    '''
    with imageio.get_writer(path, mode='I',fps=speed) as writer:
        for filename in stackList:
            filename = filename.replace("/","-")
            filename = filename.replace(" ","-")
            filename = filename.replace(":","-")
            filename += ".png"
            image = imageio.imread("./static/image/sis/"+filename)
            writer.append_data(image)
    '''
    return {"gif":path}
# 找要疊加的圖片
def findPictureName(id,cutType):
    readData = []
    with open(f"./static/data/{cutType}.csv", newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        next(rows) # 跳過標題
        for row in rows :
            readData.append([row[0]]+list(map(int,row[1:])))
    # 要疊加的照片
    statckList = []
    order = 0
    print("GEI ID:",id)
    for data in readData:
        # cut
        if data[1] == 1 and statckList != []:
            # 確認是疊加的原始圖片
            if order == int(id):
                return statckList
            order += 1
            statckList.clear()
        # shot
        elif data[1] == 0:
            # data[0]: 彩色 PM2.5 圖片名字
            statckList.append(data[0])
    return statckList
if __name__ == "__main__":
    # from gevent import pywsgi
    # server = pywsgi.WSGIServer(("localhost", 8085), app)
    # server.serve_forever()
    if os.path.isdir("./static/image/clusterUI") == False:
        os.system("mkdir ./static/image/clusterUI")
    app.run(port=8085,debug=True)