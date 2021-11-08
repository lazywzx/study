# -*- coding:utf-8 -*-
import numpy as np
import cv2


# 添加椒盐噪声
def addNoise(image, prob):
    """prob: 0~0.5"""
    output = image.copy()
    thres = 1 - prob
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            rdn = np.random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255

    return output


# 旋转
def imgRotate(image, angle):
    """angle: 0~360"""
    height, width = image.shape
    center = (width // 2, height // 2)

    RtMt = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotatedImg = cv2.warpAffine(image, RtMt, (width, height))

    return rotatedImg


# 剪切
def imgCut(image, HStart, HEnd, WStart, WEnd, fill=0):
    """fill: 0~255"""
    cutout = image.copy()
    cutout[HStart: HEnd, WStart: WEnd] = fill
    return cutout
