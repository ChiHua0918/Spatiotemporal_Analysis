from keras.models import Sequential
from keras.layers.core import Activation
from keras.layers.convolutional import Conv2D, MaxPooling2D
import numpy as np
from matplotlib import pyplot as plt
def makeModel(picture):
    model = Sequential()
    model.add(Conv2D(3, 
                    (15,15), 
                    padding="same", 
                    data_format="channels_last", 
                    input_shape=picture.shape))
    model.add(Activation("relu"))
    print(model.summary())
def takeFeature():
    data = np.reshape(data,(len(data),1))
    # 灰階圖 rgb 三個數值會相同
    data = data.repeat(3)
    data = np.reshape(data,(10,10,3))
    data = np.expand_dims(data, axis=0)
    x = preprocess_input(data)
def show_img(model, img):
    plt.figure(figsize=(8, 8))
    img_batch = np.expand_dims(img, axis=0)
    conv_img = model.predict(img_batch)
    conv_img = np.squeeze(conv_img, axis=0)
    print(conv_img.shape)
    conv_img = conv_img.reshape(conv_img.shape[:2])
    plt.imshow(conv_img)