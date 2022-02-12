# rom keras.applications.vgg16 import VGG16
from numpy.lib.function_base import append
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np
import csv
import tensorflow as tf
import os
import random
# 模型及權重載入程式
# include_top=True，表示會載入完整的 VGG16 模型，包括加在最後(頂部)3層完全連接層 <- 後進先出
# include_top=False，表示會載入 VGG16 的模型，不包括加在最後(頂部)的3層完全連接層，通常是取得 Features
# imagenet:使用預先訓練的資料
# model = VGG16(weights='imagenet', include_top=True)
# model = VGG16(weights="imagenet", include_top=False)
# model = VGG19( weights= "imagenet" , include_top= True ,input_tensor=Input( shape= ( 100 , 100 , 1 )))

def writeCSV(result):
    with open("./flask/static/cnn/GEI_origin_average_cnn.csv","w",newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result)

# 資料放大
def magnifier(GEI_dot):
    for item in GEI_dot:
        for pos in range(1,len(item)):
            item[pos] *= 10000
    return GEI_dot

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
# 取前10名
def take(classNum):
    order = sorted(classNum.values(),reverse=True)
    threshold = order[10] # 過第10名分數的門檻
    classification = []
    for key,value in classNum.items():
        if value >= threshold:
            classification.append(key)
    return classification
# 套用模板
def vgg16(model):
    path = "./flask/static/image/GEI~3/GEI_origin_average/"
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
            if classNum.get(item) == None:
                classNum[item] = 1
            else:
                classNum[item] += 1

    return classNum,every_GEI_extent


def main():
    # model
    model = tf.keras.applications.VGG16(
        include_top=True,
        weights="imagenet",
        input_tensor=None,
        input_shape=None,
        pooling=None,
        classes=1000,
        classifier_activation="softmax",
        # classifier_activation=None,
    )
    classNum, every_GEI_extent = vgg16(model) # cnn
    classification = take(classNum)           # 取前10名的類別
    # random.shuffle(classification) # 把順序打亂
    GEI_dot = dot(classification, every_GEI_extent)
    result = magnifier(GEI_dot)
    writeCSV(result)
if __name__ == "__main__":
    main()