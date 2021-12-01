import numpy as np
from osgeo import gdal
from matplotlib import pyplot as plt

# 解决plt显示中文问题
plt.rcParams['font.sans-serif'] = ['SimHei']


def band_equilibrium(src_img):
    """对单个通道均衡化"""
    # 统计直方图
    height = src_img.shape[0]
    width = src_img.shape[1]
    histogram = np.zeros((256, 1), dtype=float)
    for i in range(height):
        for j in range(width):
            histogram[src_img[i, j]] = histogram[src_img[i, j]] + 1

    # 均衡直方图
    NormalizedHistogram = histogram / (height * width)  # 归一化直方图
    CumulativeHistogram = np.zeros((256, 1), dtype=float)  # 累计直方图
    CumulativeHistogram[0] = NormalizedHistogram[0]
    for i in range(1, 256):
        CumulativeHistogram[i] = CumulativeHistogram[i - 1] + NormalizedHistogram[i]

    EquilibriumHistogram = (CumulativeHistogram * 255).astype(np.uint8)

    # 映射到新图像
    EquilibriumImage = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            EquilibriumImage[i, j] = EquilibriumHistogram[src_img[i, j]]

    # 返回处理后的图层
    return EquilibriumImage


def img_equilibrium(image):
    """对图像每个波段分别做直方图均衡化处理"""
    bands = image.shape[0]
    equ_img = np.zeros(image.shape, dtype=np.uint8)
    for band in range(bands):
        equ_img[band] = band_equilibrium(image[band])

    return equ_img


def enhance(img_path):
    """直方图均衡化图像增强与显示"""
    # 读入数据
    data = gdal.Open(img_path)
    img = data.ReadAsArray()
    # 显示原始数据的六个波段和直方图
    plt.figure('原始数据各波段图像')
    for i in range(6):
        plt.subplot(231 + i)
        plt.imshow(img[i], cmap='gray')
        plt.title('Band' + str(1 + i))

    plt.figure('原始数据各波段直方图')
    for i in range(6):
        plt.subplot(231 + i)
        plt.hist(img[i].flatten(), bins=128)
        plt.title('Band' + str(1 + i) + '直方图')
        plt.xlim(0, 255)

    # 图像增强
    enhanced_img = img_equilibrium(img)
    # 显示直方图均衡化后的六个波段和直方图
    plt.figure('直方图均衡化后各波段图像')
    for i in range(6):
        plt.subplot(231 + i)
        plt.imshow(enhanced_img[i], cmap='gray')
        plt.title('enh_Band' + str(1 + i))

    plt.figure('直方图均衡化后各波段直方图')
    for i in range(6):
        plt.subplot(231 + i)
        plt.hist(enhanced_img[i].flatten(), bins=128)
        plt.title('enh_Band' + str(1 + i) + '直方图')
        plt.xlim(0, 255)

    # 增强前后彩色合成效果对比
    bands, height, width = img.shape
    tmp_img = np.zeros((height, width, 3), dtype=np.uint8)
    plt.figure('增强前后彩色合成效果对比')
    plt.subplot(221)
    tmp_img[:, :, 0] = img[2]; tmp_img[:, :, 1] = img[1]; tmp_img[:, :, 2] = img[0]; plt.imshow(tmp_img)
    plt.title('原数据可见光波段321合成')

    plt.subplot(222)
    tmp_img[:, :, 0] = img[3]; tmp_img[:, :, 1] = img[2]; tmp_img[:, :, 2] = img[1]; plt.imshow(tmp_img)
    plt.title('原数据标准假彩色波段432合成')

    plt.subplot(223)
    tmp_img[:, :, 0] = enhanced_img[2]; tmp_img[:, :, 1] = enhanced_img[1]; tmp_img[:, :, 2] = enhanced_img[0]
    plt.imshow(tmp_img)
    plt.title('增强后可见光波段321合成')

    plt.subplot(224)
    tmp_img[:, :, 0] = enhanced_img[3]; tmp_img[:, :, 1] = enhanced_img[2]; tmp_img[:, :, 2] = enhanced_img[1]
    plt.imshow(tmp_img)
    plt.title('增强后标准假彩色波段432合成')

    plt.show()


# 函数调用
enhance('./Exp2_TM.tif')
