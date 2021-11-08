import cv2
import matplotlib.pyplot as plt
import dip1_equilibrium as de


def showing(r, c, o, image, title, hoi, gray='False'):
    """格式化显示图片和直方图"""
    plt.subplot(r, c, o)
    if hoi:
        plt.hist(image.ravel(), 256)
    elif gray:
        plt.imshow(image, cmap='gray')
        plt.xticks([])
        plt.yticks([])
    else:
        plt.imshow(image)
        plt.xticks([])
        plt.yticks([])

    plt.title(title)
    plt.show()


def grayorcolorimage(path, gray):
    """处理灰度或彩色图像"""
    if gray:
        # 灰度图像
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        eimage = de.equilibrium(image)
    else:
        # 彩色图像
        image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        eimage = de.colorimageequilibrium(image)

    showing(2, 2, 1, image, 'img_ori', False, True)
    showing(2, 2, 2, eimage, 'img_equ', False, True)
    showing(2, 2, 3, image, 'hist_ori', True)
    showing(2, 2, 4, eimage, 'hist_equ', True)


plt.figure(1)
grayorcolorimage('./a.jpg', True)
plt.figure(2)
grayorcolorimage('./d.jpg', True)
plt.figure(3)
grayorcolorimage('./fss.png', False)
