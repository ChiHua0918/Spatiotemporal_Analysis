from flask import Flask, render_template, request, jsonify
import os
import csv
import imageio
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
    elif pattern == "clusterIcon":
        
    cluster = []
    GEIName = []
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                cluster.append(int(row[1]))
                GEIName.append(row[0])
            except:
                pass
    return {"cluster":cluster,"GEIName":GEIName,"maxCluster":max(cluster)}

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
    order = 1
    print("GEI ID:",id)
    for data in readData:
        # cut
        if data[1] == 1 and statckList != []:
            if order > 930:
                print("order",order)
                print("stackList",statckList)
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