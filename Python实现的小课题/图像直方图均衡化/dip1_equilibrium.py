import cv2
import numpy


def equilibrium(SourceImage):
    """对单个通道均衡化"""
    # 统计直方图
    height = SourceImage.shape[0]
    width = SourceImage.shape[1]
    histogram = [0] * 256
    for i in range(height):
        for j in range(width):
            histogram[SourceImage[i, j]] = histogram[SourceImage[i, j]] + 1

    # 均衡直方图
    NormalizedHistogram = [i / (height * width) for i in histogram]  # 归一化直方图
    CumulativeHistogram = [0] * 256  # 累计直方图
    CumulativeHistogram[0] = NormalizedHistogram[0]
    for i in range(1, 256):
        CumulativeHistogram[i] = CumulativeHistogram[i - 1] + NormalizedHistogram[i]

    EquilibriumHistogram = [int(255 * i) for i in CumulativeHistogram]

    # 映射到新图像
    EquilibriumImage = numpy.zeros((height, width), dtype=numpy.uint8)
    for i in range(height):
        for j in range(width):
            EquilibriumImage[i, j] = EquilibriumHistogram[SourceImage[i, j]]

    # 返回处理后的图层
    return EquilibriumImage


def colorimageequilibrium(Image):
    """对彩色图片三个通道分别均衡化处理
        最后再合成彩色图片"""
    # 拆分三个通道分别处理
    RImage, GImage, BImage = cv2.split(Image)
    REquilibrium = equilibrium(RImage)
    GEquilibrium = equilibrium(GImage)
    BEquilibrium = equilibrium(BImage)

    # 合成图片
    EquilibriumColorImage = cv2.merge([REquilibrium, GEquilibrium, BEquilibrium])

    return EquilibriumColorImage
