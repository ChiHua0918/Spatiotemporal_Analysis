from flask import Flask, render_template, request
import os
import csv
import imageio
import numpy as np
#創建Flask物件app并初始化
app = Flask(__name__)

#通過python裝飾器的方法定義路由地址
@app.route("/")
#定義方法 用jinjia2引擎來渲染頁面，并回傳一個index.html頁面
def root():
    return render_template("show.html")

# 現在GEI的數量
@app.route("/GEINum",methods=["GET"])
def GEINum():
    path = "./static/image/GEI/GEI_origin"
    GEIName = os.listdir(path)
    return {"num":len(GEIName)}

# 讀取csv獲取每一張 GEI 所屬的群
@app.route("/cluster",methods = ["GET"])
def cluster():
    memory = request.args.get("memory")
    pattern = request.args.get("pattern")
    if pattern == "level":
        path = "./static/data/clusterData/KMeans/"+memory+"_regular_cluster.csv"
    elif pattern == "space":
        path = "./static/data/clusterData/bow/"+memory+"_cluster.csv"
    elif pattern == "cnn":
        path = "./static/data/clusterData/cnn/"+memory+"_cluster.csv"
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
    with open(f"./static/data/GEI_data/{memory}.csv", newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append(list(map(float,row[1:])))
            except:
                pass
    print("cluster length",len(cluster))
    print("readData length",len(readData))
    clusterData = []
    for k in range(max(cluster)+1):
        # 堆疊的 GEI 數據
        stackData = np.array([float(0) for i in range(len(readData[0]))])
        # 堆疊的張數
        n = 0
        while k in cluster:
            n += 1
            pos = cluster.index(k) # 找對應群的 GEI
            stackData += readData[pos]
            cluster.remove(k) # 把剛剛已經加到 stackList 的 GEI 移除
        # 名字
        stackData = stackData / n
        stackData = stackData.tolist()
        stackData.insert(0,k)
        print(k)
        print(stackData)
        clusterData.append(stackData)
    file = "clusterUI.csv"
    with open("./static/data/"+file, 'w', newline='') as _file:
        writer = csv.writer(_file)
        writer.writerow(["name","data"])
        writer.writerows(clusterData)
    # 正規化
    # os.system(f"python ./make_clusterUI/regular.py {file}")
    # 畫圖
    file = "clusterUI.csv"
    # file = "clusterUI_regular.csv"
    os.system(f"python ./make_clusterUI/userDataPic.py {file}")
#app的路由地址"/submit"即為ajax中定義的url地址，采用POST、GET方法均可提交
@app.route("/gif",methods=["GET"])
# 顯示連續彩色PM2.5空汙圖
def gif():
    id = request.args.get("id") # GEI id
    speed = request.args.get("speed") # gif 速度
    # 要疊成 gif 的圖片
    stackList = findPictureName(id)
    print(stackList)
    putPlace = "./static/image/gif/"# gif要存取的地方
    path = putPlace+id+".gif"
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
    with open("./static/data/cut~3.csv", newline= '') as csvfile :
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
        #     if order > 930:
        #         print("order",order)
        #         print("stackList",statckList)
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
app.run(port=8000)