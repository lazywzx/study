import numpy as np


def fx(x):
    """定义函数fx = x * e^x - 1"""
    return x * np.exp(x) - 1


def cutting_line(x0, x1, e1, e2, n):
    """
    割线法求解fx近似值
    :param x0: 初始值1
    :param x1: 初始值2
    :param e1: 小于则抛出奇异标志
    :param e2: |x1 - x0|小于则迭代成功
    :param n: 最大迭代次数
    :return: 迭代结果和次数
    """
    k = 1
    while True:
        if abs(fx(x0)) < e1 or abs(fx(x1)) < e1:
            return "奇异标志", None, k

        x2 = x1 - fx(x1) * (x1 - x0) / (fx(x1) - fx(x0))
        if abs(x2 - x1) < e2:
            return "迭代成功", x2, k

        if k == n:
            return "迭代失败", x2, k

        x0 = x1
        x1 = x2
        k += 1


flag, x, k = cutting_line(0.4, 0.6, 1e-20, 5e-6, 20)

print("迭代结果：" + flag + "\n" + "近似值：" + str(x) + "\n迭代次数：" + str(k))
