from sklearn.datasets import load_sample_image
from sklearn.feature_extraction import image
# rom keras.applications.vgg16 import VGG16
from numpy.lib.function_base import append
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np
import csv
import tensorflow as tf
def takeFeature():
    # Use the array data from the first image in this dataset:
    one_image = load_sample_image("./make_GEI/picture/level/NO.0.jpg")
    print('Image shape: {}'.format(one_image.shape))
    patches = image.extract_patches_2d(one_image, (2, 2))
    print('Patches shape: {}'.format(patches.shape))
# 套用模板
def vgg16(model,readData):
    # 儲存每一張GEI和1000個類別中的關係程度
    for data in readData:
        data = np.reshape(data,(len(data),1))
        # 灰階圖 rgb 三個數值會相同
        data = data.repeat(3)
        data = np.reshape(data,(10,10,3))
        data = np.expand_dims(data, axis=0)
        x = preprocess_input(data)
        # print(x)
        print(x)
        # print("preprocess_input",x)
        # 預測，取得feature map，維度為 (1,3,3,512)
        features = model.predict(x)
        print(features)
        return
def readCSV():
    inputData = "GEI_origin_regular.csv"
    inputFile =  "./make_GEI/data/GEI_regular/"+inputData
    readData = []
    with open(inputFile, newline= '') as csvfile :
        rows = csv.reader(csvfile, delimiter = ',')
        for row in rows :
            try:
                readData.append(list(map(float,row[1:])))
            except:
                pass
    return readData
# 利用捲基層提取特徵
def main():
    # model = tf.keras.applications.VGG16(
    #     include_top=False,
    #     weights="imagenet",
    #     input_tensor=None,
    #     input_shape=None,
    #     pooling=None,
    #     classes=1000,
    #     classifier_activation="softmax",
    #     # classifier_activation=None,
    # )
    # 顯示模型結構
    # print(model.summary())
    # data = readCSV()
    # vgg16(model,data)
    takeFeature()
    return
    classNum, every_GEI_extent = vgg16(model) # cnn
    classification = take(classNum)           # 取前10名的類別
    # random.shuffle(classification) # 把順序打亂
    GEI_dot = dot(classification, every_GEI_extent)
    result = magnifier(GEI_dot)
    writeCSV(result)
if __name__ == "__main__":
    main()