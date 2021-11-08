import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示乱码问题

# 读入图片并转换为灰度图
img_bgr = cv2.imread('wall_TIB15thWall_13d20h.JPG')
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# 二维数据转化为一维数据
data = np.array(img_gray).flatten()

# 计算均值和方差
mean = np.mean(data)
var = np.var(data)

# 画出统计直方图
plt.figure(figsize=(10, 5))
nums, bins, patches = plt.hist(data, bins=(max(data) - min(data)), edgecolor='k', rwidth=0.6)
plt.title("灰度值统计直方图")
# plt.show()


# 估计分布类型及其参数
# 1. 高斯分布
def gauss(x, mean, var):
    """输入x, 均值和方差，返回高斯分布函数值"""
    return 1 / (2 * math.pi * var) ** 0.5 * math.exp(-(x - mean) ** 2 / 2 / var)


# 2. 瑞利分布
def riley(x, mean, var):
    """输入x, 均值和方差，返回瑞利分布函数值"""
    a = mean / (math.pi * 4) ** 0.5
    b = 4 * var / (4 - math.pi)

    if x >= a:
        return 2 / b * (x - a) * math.exp(-(x -a) ** 2 / b)
    else:
        return 0


# 3. 指数分布
def expo(x, mean, var):
    """输入x, 均值，返回指数分布函数值"""
    a = 1 / mean
    return a * math.exp(-a * x)


# 4. 均匀分布
def unif(x , mean, var):
    """均匀分布"""
    return 127.5


# 计算KL散度，取散度最小的分布
kl = 0
prob = nums / data.size
for i in range(bins.size - 1):
    a = unif(bins[i], mean, var)

    if a == 0:  # 避免非法运算值
        continue
    b = prob[i] / a
    if b == 0:
        continue
    kl += prob[i] * math.log(b)

print("KL散度值为：", kl)
