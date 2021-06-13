#!/usr/bin/env python3

from augment import *

from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Dropout, UpSampling2D

import random

W = 352
H = 544
BATCH_SIZE = 16 

# makes array from image with the dimensions 
# required for network
def makeArr(path):
    im = Image.open(path)
    im = im.resize((W,H))
    im = ImageOps.grayscale(im)
    return np.array(im)
   
# converts image binary
def toBinary(a):
    a[a<128] = 0.0
    a[a>127] = 1.0
    return a

# converts floating point image to binary
def floatToBinary(a):
    a[a< 0.5] = 0.0
    a[a>=0.5] = 1.0
    return a

# normalizes an image
def norm(a):
    return (a - a.mean()) / a.std()

# shuffles input and output directories identically
def shuffle(xFiles, yFiles):
    tmp = list(zip(xFiles, yFiles))
    random.shuffle(tmp)
    return zip(*tmp)

# generates data for network
def generate(dataset, masks, batchSize):
    # get list of fingerprints and masks
    # sort so the ith print matches the ith mask
    xFiles = sorted(listdir(dataset))
    yFiles = sorted(listdir(masks))

    xFiles,yFiles = shuffle(xFiles, yFiles)

    i = 0
    while True:
        xBatch = []
        yBatch = []
        for j in range(batchSize):
            # shuffle after every epoch
            if i == len(xFiles):
                xFiles,yFiles = shuffle(xFiles, yFiles)
                i = 0

            x = makeArr(dataset + xFiles[i])
            y = makeArr( masks  + yFiles[i])

            x,y = augment(x, y) 

            x = norm(x)
            y = toBinary(y)

            xBatch.append(x[..., None])  
            yBatch.append(y[..., None])

            i += 1

        yield np.array(xBatch), np.array(yBatch)
            
# builds neural network
def buildModel():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(H,W,1), activation='relu', padding='same'))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(Dropout(0.5))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(1, (3, 3), activation='sigmoid', padding='same'))
    return model

# outputs predicted image from the model
def predict(path):
    model = load_model('Model')
    im = Image.open(path)
    w,h = im.size
    im = im.resize((W,H))
    im = ImageOps.grayscale(im)
    fp = np.array(im)
    nm = norm(fp)
    ms = model.predict(nm[None, ..., None])
    ms = ms[0,...,0]
    fp[ms<0.5] = 0
    fp = fp.astype(np.uint8)
    im = Image.fromarray(fp)
    return im.resize((w,h))

# trains network
def train(new):
    if new:
        model = buildModel()
    else:
        model = load_model('Model')
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(
        generate(FINGERPRINTS, MASKS, BATCH_SIZE),
        epochs = 1,
        steps_per_epoch = len(listdir(FINGERPRINTS)) // BATCH_SIZE
    )
    model.save("Model")


if TRAIN:
    train(NEW)
else:
    predict("test.bmp").save("output.jpg")

