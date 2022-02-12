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
    path = "./static/image/GEI~3/GEI_origin"
    GEIName = os.listdir(path)
    return {"num":len(GEIName)}

# 讀取csv獲取每一張 GEI 所屬的群
@app.route("/cluster",methods = ["GET"])
def cluster():
    memory = request.args.get("memory")
    pattern = request.args.get("pattern")
    if pattern == "level":
        path = "./static/classifyData/classify_rgb_3/"+memory+"_regular_classify.csv"
    elif pattern == "space":
        path = "./static/classifyData/classify_bow/"+memory+"_classify.csv"
    elif pattern == "cnn":
        path = "./static/classifyData/classify_cnn/"+memory+"_classify.csv"
    cluster = []
    GEIName = []
    with open(path, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            if row[1].isdigit():
                cluster.append(int(row[1]))
                GEIName.append(row[0])
    return {"cluster":cluster,"GEIName":GEIName}

#app的路由地址"/submit"即為ajax中定義的url地址，采用POST、GET方法均可提交
@app.route("/gif",methods=["GET"])
# 顯示連續彩色PM2.5空汙圖
def gif():
    path = "./static/image/sis~3"
    allPicture = os.listdir(path) # 所有 PM2.5 彩色圖片
    stackList = [] # 要疊成 gif 的圖片
    # 從前端拿到 id
    id = request.args.get("id")
    speed = request.args.get("speed")
    for img in allPicture:
        imgID = img.split("-")[0]
        if imgID == id:
            stackList.append(img)
        elif stackList != []:
            putPlace = "./static/image/gif/"# gif要存取的地方
            path = putPlace+id+".gif"
            with imageio.get_writer(path, mode='I',fps=speed) as writer:
                for filename in stackList:
                    image = imageio.imread("./static/image/sis~3/"+filename)
                    writer.append_data(image)
            break
    return {"gif":path}

app.run(port=8000)