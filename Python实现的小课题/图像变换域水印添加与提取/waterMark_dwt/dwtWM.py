# -*- coding: utf-8 -*-
import numpy as np
import pywt
import cv2


# embedded
def DWTEmbdWM(imgPath, wmPath, af):
    print("embedding...")
    # read and cvt
    grayimg = cv2.cvtColor(cv2.imread(imgPath), cv2.COLOR_BGR2GRAY)
    waterMark = cv2.cvtColor(cv2.imread(wmPath), cv2.COLOR_BGR2GRAY)

    # 1. dwt
    cA, (cH, cV, cD) = pywt.dwt2(grayimg, 'haar')
    cA2, (cH2, cV2, cD2) = pywt.dwt2(cA, 'haar')
    cA3, (cH3, cV3, cD3) = pywt.dwt2(cA2, 'haar')

    # 将各个子图进行拼接，最后得到一张图
    AH3 = np.concatenate([cA3, cH3], axis=1)
    VD3 = np.concatenate([cV3, cD3], axis=1)
    AHVD3 = np.concatenate([AH3, VD3], axis=0)
    AH2 = np.concatenate([AHVD3, cH2], axis=1)
    VD2 = np.concatenate([cV2, cD2], axis=1)
    AHVD2 = np.concatenate([AH2, VD2], axis=0)
    AH = np.concatenate([AHVD2, cH], axis=1)
    VD = np.concatenate([cV, cD], axis=1)
    dwtresult = np.concatenate([AH, VD], axis=0)

    # 3. 嵌入
    cA4 = cA3 + af * waterMark

    # 将各个子图进行拼接，最后得到一张图
    AH3 = np.concatenate([cA4, cH3], axis=1)
    VD3 = np.concatenate([cV3, cD3], axis=1)
    AHVD3 = np.concatenate([AH3, VD3], axis=0)
    AH2 = np.concatenate([AHVD3, cH2], axis=1)
    VD2 = np.concatenate([cV2, cD2], axis=1)
    AHVD2 = np.concatenate([AH2, VD2], axis=0)
    AH = np.concatenate([AHVD2, cH], axis=1)
    VD = np.concatenate([cV, cD], axis=1)
    embddwtresult = np.concatenate([AH, VD], axis=0)

    # 4. idwt
    icA2 = pywt.idwt2((cA4, (cH3, cV3, cD3)), 'haar')
    icA = pywt.idwt2((icA2, (cH2, cV2, cD2)), 'haar')
    embeddedImage = pywt.idwt2((icA, (cH, cV, cD)), 'haar')

    print("Done!")
    return grayimg, waterMark, dwtresult, embddwtresult, embeddedImage


# extract
def DWTExttWM(oriPath, embdPath, af):
    print("extracting...")
    # read and cvt
    oriimg = cv2.cvtColor(cv2.imread(oriPath), cv2.COLOR_BGR2GRAY)
    embdimg = cv2.cvtColor(cv2.imread(embdPath), cv2.COLOR_BGR2GRAY)

    # 1. ori dwt
    cA, (cH, cV, cD) = pywt.dwt2(oriimg, 'haar')
    cA2, (cH2, cV2, cD2) = pywt.dwt2(cA, 'haar')
    cA3, (cH3, cV3, cD3) = pywt.dwt2(cA2, 'haar')

    # 2. embd dwt
    embdcA, (embdcH, embdcV, embdcD) = pywt.dwt2(embdimg, 'haar')
    embdcA2, (embdcH2, embdcV2, embdcD2) = pywt.dwt2(embdcA, 'haar')
    embdcA3, (embdcH3, embdcV3, embdcD3) = pywt.dwt2(embdcA2, 'haar')

    # 3. extract WM
    extractWaterMark = (embdcA3 - cA3) / af
    for i in range(extractWaterMark.shape[0]):
        for j in range(extractWaterMark.shape[1]):
            if extractWaterMark[i][j] > 255:
                extractWaterMark[i][j] = 255
            elif extractWaterMark[i][j] < 0:
                extractWaterMark[i][j] = 0

    print("Done!")
    return extractWaterMark
