import cv2
import numpy as np


def BTWSHighPass(sourceimage):
    """巴特沃斯高通滤波器，处理单通道图像"""
    height = sourceimage.shape[0]
    width = sourceimage.shape[1]

    # 频谱
    fftres = np.fft.fftshift(np.fft.fft2(sourceimage))

    # 巴特沃斯截止频率与阶数
    wc = 90
    N = 4
    # 巴特沃斯滤波器
    BTWSFilter = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            d = ((i - height // 2) ** 2 + (j - width // 2) ** 2) ** 0.5
            # 巴特沃斯高通
            if d == 0:
                BTWSFilter[i][j] = 0
            else:
                BTWSFilter[i][j] = (1 / (1 + (wc / d) ** (2 * N))) ** 0.5

    filterres = fftres * BTWSFilter

    # 滤波结果图像
    return (np.abs(np.fft.ifft2(np.fft.ifftshift(filterres)))).astype(np.uint8)


def ImageProcessing(btwsimage):
    """对巴特沃斯滤波结果进行一定的后处理，使边缘更清晰"""
    # 二值化阈值
    k = 9
    for i in range(btwsimage.shape[0]):
        for j in range(btwsimage.shape[1]):
            if btwsimage[i][j] <= k:
                btwsimage[i][j] = 0
            else:
                btwsimage[i][j] = 255

    # 对图像做形态学运算
    # 先闭运算使破碎对象连接起来
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closedimage = cv2.morphologyEx(btwsimage, cv2.MORPH_CLOSE, kernel)
    # 再开运算消除噪点
    openedimage = cv2.morphologyEx(closedimage, cv2.MORPH_OPEN, kernel)

    return btwsimage, openedimage


def ColorImageBorder(path, color=True):
    """彩色图像边缘检测，拆分三个通道分别处理"""
    colorimage = cv2.imread(path)
    # 判断处理彩色图像还是灰度图像
    if color:
        colorimage = cv2.cvtColor(colorimage, cv2.COLOR_BGR2RGB)
    else:
        colorimage = cv2.cvtColor(colorimage, cv2.COLOR_BGR2GRAY)

    btimage = colorimage.copy()
    tni = colorimage.copy()
    xtxi = colorimage.copy()
    # 分通道处理
    if color:
        for d in range(3):
            btimage[:, :, d] = BTWSHighPass(colorimage[:, :, d])
            btcopy = btimage[:, :, d].copy()
            tni[:, :, d], xtxi[:, :, d] = ImageProcessing(btcopy)
    else:
        btimage = BTWSHighPass(colorimage)
        btcopy = btimage.copy()
        tni, xtxi = ImageProcessing(btcopy)
    return colorimage, btimage, tni, xtxi
