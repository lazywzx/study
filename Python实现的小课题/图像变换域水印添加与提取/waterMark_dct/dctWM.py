# -*-coding:utf-8 -*-
import cv2
import numpy as np


def DCTEmbdWM(oriPath, wmPath, embdRow, embdCol, af):
    print("embedding...")
    # read and cvt
    grayimg = cv2.cvtColor(cv2.imread(oriPath), cv2.COLOR_BGR2GRAY)
    watermark = cv2.cvtColor(cv2.imread(wmPath), cv2.COLOR_BGR2GRAY)

    # dct
    dctImg = cv2.dct(np.array(grayimg, np.float32))
    oridctImg = dctImg.copy()
    dctwater = cv2.dct(np.array(watermark, np.float32))

    # embd
    waterH, waterW = watermark.shape
    dctImg[waterH * embdRow: waterH * (embdRow + 1), waterW * embdCol: waterW * (embdCol + 1)] += af * dctwater

    # idct
    idctImg = np.array(cv2.idct(dctImg), np.uint8)

    print("Done!")
    return grayimg, watermark, oridctImg, dctwater, dctImg, idctImg


# extract
def DCTExttWM(oriPath, embdImgPath, wmPath, embdRow, embdCol, af):
    print("extracting...")
    # read and cvt
    grayimg = cv2.cvtColor(cv2.imread(oriPath), cv2.COLOR_BGR2GRAY)
    embdimg = cv2.cvtColor(cv2.imread(embdImgPath), cv2.COLOR_BGR2GRAY)
    wmimg = cv2.cvtColor(cv2.imread(wmPath), cv2.COLOR_BGR2GRAY)

    # dct
    oridct = cv2.dct(np.array(grayimg, np.float32))
    embddct = cv2.dct(np.array(embdimg, np.float32))

    # extract
    waterH, waterW = wmimg.shape
    dctwater = (embddct[waterH * embdRow: waterH * (embdRow + 1), waterW * embdCol: waterW * (embdCol + 1)]  -
                oridct[waterH * embdRow: waterH * (embdRow + 1), waterW * embdCol: waterW * (embdCol + 1)]) / af

    # idct
    idctWM = np.array(cv2.idct(dctwater), np.uint8)

    print("Done!")
    return idctWM
