from math import sin, cos, tan, atan, pi, radians, degrees, sqrt, exp
from random import random, randint, uniform, seed, choice, shuffle
from PIL import Image, ImageOps
from numpy.random import normal
from os import listdir
import numpy as np
import cv2
import wsq

TRAIN = False               # wether or not "cnn.py' trains the model or predicts a mask
NEW = True                  # wether or not "cnn.py" trains a new model or continues an old one

TEST = "all"                # tell "testAugmentation.py" which step to test

FINGERPRINTS = "MOLF/"      # fingerprint image directory
BACKGROUNDS = "textures/"   # background image directory
MASKS = "masks/"            # mask image directory
FP_BG = 0.1                 # percent change of a fingerprint background instead of a texture
ANGLE_STD = 30              # std for rotaion of fingerprint
NOISE_STD = 10              # std for gaussian noise 
FP_TRANS_STD = 1/6          # std for translation of fingerprint
BG_TRANS_STD = 1/3          # std for translation of background
MEAN_FADE = 0.15            # mean for fading of background
FADE_RATIO = 0.9            # maximum ratio of how dark a background fingerprint can be
R = 2.7                     # multiple of radii of the smudge that can be included
