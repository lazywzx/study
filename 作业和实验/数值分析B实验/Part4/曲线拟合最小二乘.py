import numpy as np
import pylab
from matplotlib import pyplot as plt

# 解决画图显示中文问题
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']

x = np.array([3, 4, 5, 6, 7, 8, 9])
f = np.array([2.01, 2.98, 3.5, 5.02, 5.47, 6.02, 7.05])


def phi(x, k):
    """最小二乘逼近基函数"""
    return x ** k


def min2multi(x, f, m):
    """曲线拟合最小二乘"""
    # 求Hn
    H = np.zeros((m, m))
    for c in range(0, m):
        for r in range(0, m):
            pp_sum = 0
            for i in range(0, x.size):
                pp_sum += phi(x[i], c) * phi(x[i], r)

            H[c][r] = pp_sum

    # 求b
    b = np.zeros((1, m)).T
    for j in range(0, m):
        pf_sum = 0
        for i in range(0, x.size):
            pf_sum += phi(x[i], j) * f[i]

        b[j] = pf_sum

    # 解法方程
    return np.linalg.solve(H, b)


def y(x, a, m):
    """定义拟合多项式函数y = sum(ax^j)"""
    y_sum = 0
    for i in range(0, m):
        y_sum += a[i][0] * x ** i

    return y_sum


def main(x, f, m):
    """用最小二乘法拟合数据并可视化"""
    a = min2multi(x, f, m)

    # 输出拟合多项式
    y_str = "y = "
    for i in range(0, m):
        y_str += str(a[i][0]) + "x^" + str(i)
        if i < m - 1:
            y_str += " + "

    print("拟合多项式为：", y_str)

    # 画出原始数据和拟合多项式曲线
    t = np.arange(min(x) - 1, max(x) + 1, 0.1)
    yt = y(t, a, m)
    plt.plot(t, yt, label="拟合多项式y(x)", linewidth=2)
    plt.plot(x, f, 'm.-.', label="原始数据f(x)", linewidth=2)
    plt.legend()
    plt.title("最小二乘曲线拟合结果与原始数据对比")
    plt.xlabel("x")
    plt.ylabel("y(x)、f(x)")
    plt.show()


main(x, f, 5)
