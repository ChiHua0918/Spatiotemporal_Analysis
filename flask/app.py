from flask import Flask, render_template, request, send_from_directory,url_for,redirect
import os
import csv
import imageio
import numpy as np
from make_clusterUI.userDataPic import drawColor
#創建Flask物件app并初始化
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
@app.route("/qbgResult",methods = ["POST"])
def qbgResult():
    # selectName = request.args.get("selectName") # NO.1
    selectName = request.form.get("selectName") # NO.1
    GEIfolder = request.form.get("GEIfolder")
    print("selectName:",selectName)
    print("GEIfolder:",GEIfolder)
    rankResult = directQBG(selectName,GEIfolder)
    # GEIRankData = rankResult[1:]
    GEIRankData = dict()
    for i in range(len(rankResult[1:])):
        GEIRankData[i] = rankResult[i+1].replace(",","").replace("'","").split()
    return render_template("qbgResult.html",sourceImageName = selectName+".png",\
                                            sourceDataset = GEIfolder,\
                                            GEIRankData = GEIRankData)
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
        for row in rows :
            cut_shot.append(int(row[0]))
    return {"data":cut_shot}
# 計算 GEI 的排名
# @app.route("/directQBG",methods = ["GET"])
def directQBG(selectName,GEIfolder):
    command = "python3 rasterScan_D_GEI.py " + selectName
    print(GEIfolder)
    print(command)
    # 建立 process，將執行結果用 readlines 讀取
    rankResult = os.popen(command).readlines()
    return rankResult
# ================================
# 現在GEI的數量
@app.route("/GEINum",methods=["GET"])
def GEINum():
    path = "./static/image/GEI/GEI_origin"
    GEIName = os.listdir(path)
    # return {"num":len(GEIName)}
    return {"num":2}

# 讀取csv獲取每一張 GEI 所屬的群
@app.route("/cluster",methods = ["GET"])
def cluster():
    # 從前端拿到的資料
    memory = request.args.get("memory")
    clusterFile = request.args.get("clusterFile")
    filterSize = request.args.get("filterSize")
    print(f"memory:{memory} clusterFile:{clusterFile} filterSize:{filterSize}")
    if clusterFile.split('_')[0] == "histogram":
        folder = clusterFile
        path = f"./static/data/clusterData/{folder}/{memory}.csv"
    elif clusterFile.split('_')[0] == "bow":
        folder = clusterFile.split('_')[1]
        path = f"./static/data/clusterData/bow/{folder}/{memory}_{filterSize}.csv"
    elif clusterFile.split('_')[0] == "cnn":
        path = f"./static/data/clusterData/cnn/imagenet/{memory}_imagenet.csv"
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
    clusterUI(tmp,memory)
    return {"cluster":cluster,"GEIName":GEIName,"maxCluster":k}
# 製作每一群的代表 GEI
def clusterUI(cluster,memory):
    # 每一群所有 GEI 堆疊成一個代表的 GEI
    print("make clusterUI")
    readData = []
    with open(f"./static/data/GEI_regular/{memory}.csv", newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append(list(map(float,row[1:])))
            except:
                pass
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
    id = request.args.get("id") # GEI id
    speed = request.args.get("speed") # gif 速度
    # 要疊成 gif 的圖片
    stackList = findPictureName(id)
    print(stackList)
    path = f"./static/image/gif/{id}.gif"
    with imageio.get_writer(path, mode='I',fps=speed) as writer:
        for filename in stackList:
            filename = filename.replace("/","-")
            filename = filename.replace(" ","-")
            filename = filename.replace(":","-")
            filename += ".png"
            image = imageio.imread("./static/image/sis/"+filename)
            writer.append_data(image)
    return {"gif":path}
# 找要疊加的圖片
def findPictureName(id):
    readData = []
    with open("./static/data/cut.csv", newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append([row[0]]+list(map(int,row[1:])))
            except:
                pass
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
    app.run(port=8085)