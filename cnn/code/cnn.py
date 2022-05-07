# rom keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np
import csv
import tensorflow as tf
import os
import sys
# 模型及權重載入程式
# include_top=True，表示會載入完整的 VGG16 模型，包括加在最後(頂部)3層完全連接層 <- 後進先出
# include_top=False，表示會載入 VGG16 的模型，不包括加在最後(頂部)的3層完全連接層，通常是取得 Features
# imagenet:使用預先訓練的資料
# model = VGG16(weights='imagenet', include_top=True)
# model = VGG16(weights="imagenet", include_top=False)
# model = VGG19( weights= "imagenet" , include_top= True ,input_tensor=Input( shape= ( 100 , 100 , 1 )))

def writeCSV(result,folder,source):
    # with open("./flask/static/cnn/GEI_origin_average_cnn.csv","w",newline="") as csvfile:
    outputFile = source+"_cnn.csv"
    with open(f"./data/{folder}/{outputFile}","w",newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result)
# 每一張GEI該類別的關係程度，如果此 GEI 沒有該類別，則該類別關係程度 = 0
def dot(classification,every_GEI_extent):
    GEI_dot = []
    for name,item in every_GEI_extent.items():
        extend = []
        for category in classification:
            if category in item:
                extend.append(item[category])
            else:
                extend.append(0)
        name = name[:-4]
        extend.insert(0,name)
        GEI_dot.append(extend)
        print("===== name ===== ",name)
    print("===== GEI_dot ====== ",GEI_dot)
    return GEI_dot
# 取前 20 名
def take(classNum):
    order = sorted(classNum.values(),reverse=True)
    threshold = order[20]
    classification = []
    for key,value in classNum.items():
        if value >= threshold:
            classification.append(key)
    return classification
# 套用模板
def vgg16(model,path):
    # path = "./flask/static/image/GEI~3/GEI_origin_average/"
    picture = os.listdir(path)
    # 最後所分類的結果
    classNum= dict()
    # # 1000類別的關係程度
    # relation = []
    # 所有 GEI 的關係程度
    every_GEI_extent = dict()
    # 儲存每一張GEI和1000個類別中的關係程度
    for pic in picture:
    # Input：要辨識的影像
        img_path = path+pic
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # 預測，取得feature map，維度為 (1,3,3,512)
        features = model.predict(x)
        predicted = decode_predictions(features, top=20)[0]
        print("===== predicted =====",predicted)
        # relation.append(predicted)
        # 每一個GEI的對應類別的關係程度
        extend = dict()
        for item in predicted:
            extend[item[1]] = item[2]
        every_GEI_extent[pic] = extend

        # 計算每一類的個數
        for i in range(len(predicted)):
            item = predicted[i][1] # 類別
            # 字典還沒有新增此類別
            if classNum.get(item) == None:
                classNum[item] = 1
            else:
                classNum[item] += 1

    return classNum,every_GEI_extent


def main(source,outputFolder):
    # model
    model = tf.keras.applications.VGG16(
        include_top=True,
        weights="imagenet", # "imagenet"、"mnist"
        input_tensor=None,
        input_shape=None,
        pooling=None,
        classes=1000,
        classifier_activation="softmax",
        # classifier_activation=None,
    )
    # GEI 圖片路徑
    inputData = source
    inputFile = "../make_GEI/picture/"+inputData+"/"
    classNum, every_GEI_extent = vgg16(model,inputFile) # cnn
    classification = take(classNum)
    # random.shuffle(classification) # 把順序打亂
    GEI_dot = dot(classification, every_GEI_extent)
    writeCSV(GEI_dot,outputFolder,source)
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])

    # # 取得資料
    # inputData = argv
    # inputFile = "../make_GEI/picture/"+inputData
    # readData = []
    # with open(inputFile, newline= '') as csvfile :
    #     rows = csv.reader(csvfile, delimiter = ',')
    #     for row in rows :
    #         try:
    #             readData.append([row[0]]+list(map(float,row[1:])))
    #         except:
    #             pass