# -*- coding:utf-8 -*-
import cv2
import numpy as np


# embedded
def DFTEmbdWM(oriPath, wmPath, af):
    print("embedding...")
    # read and cvt
    grayimg = cv2.cvtColor(cv2.imread(oriPath), cv2.COLOR_BGR2GRAY)
    wmimg = cv2.cvtColor(cv2.imread(wmPath), cv2.COLOR_BGR2GRAY)

    # fft
    orifft = np.fft.fft2(grayimg)
    orifftshift = np.fft.fftshift(orifft)
    wmfft = np.fft.fft2(wmimg)
    wmfftshift = np.fft.fftshift(wmfft)

    # embedded
    wmHeight, wmWidth = wmimg.shape
    HStart = wmHeight * 1; HEnd = wmHeight * 2
    WStart = wmWidth * 1; WEnd = wmWidth * 2

    orifftshiftcopy = orifftshift.copy()
    orifftshiftcopy[HStart: HEnd, WStart: WEnd] += af * wmimg
    orifftshiftcopy[-HEnd: -HStart, -WEnd: -WStart] += af * cv2.flip(wmimg, -1)

    # db图
    orimag = 20 * np.log(np.abs(orifftshift))
    wmmag = 20 * np.log(np.abs(wmfftshift))
    oricopymag = 20 * np.log(np.abs(orifftshiftcopy))

    # ifft
    ishift = np.fft.ifftshift(orifftshiftcopy)
    recoverImg = np.abs(np.fft.ifft2(ishift))

    print("Done!")
    return grayimg, wmimg, orimag, wmmag, oricopymag, recoverImg


# extract
def DFTExttWM(oriPath, wmPath, embdPath, af):
    print("extracting...")
    # read and cvt
    grayimg = cv2.cvtColor(cv2.imread(oriPath), cv2.COLOR_BGR2GRAY)
    wmimg = cv2.cvtColor(cv2.imread(wmPath), cv2.COLOR_BGR2GRAY)
    embdimg = cv2.cvtColor(cv2.imread(embdPath), cv2.COLOR_BGR2GRAY)

    # fft
    orifft = np.fft.fft2(grayimg)
    orifftshift = np.fft.fftshift(orifft)
    wmfft = np.fft.fft2(wmimg)
    wmfftshift = np.fft.fftshift(wmfft)
    embdfft = np.fft.fft2(embdimg)
    embdfftshift = np.fft.fftshift(embdfft)

    # extract
    wmHeight, wmWidth = wmimg.shape
    HStart = wmHeight * 1; HEnd = wmHeight * 2
    WStart = wmWidth * 1; WEnd = wmWidth * 2

    WMImg = (embdfftshift[HStart: HEnd, WStart: WEnd] -
             orifftshift[HStart: HEnd, WStart: WEnd]) / af
    WMImg = np.abs(WMImg)

    print("Done!")
    return WMImg
