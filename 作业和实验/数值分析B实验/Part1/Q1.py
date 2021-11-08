import math


def fx(x):
    """定义函数fx = sin(x) - x^2 / 2"""
    return math.sin(x) - x ** 2 / 2


def dichotomy(a, b, e):
    """二分法计算方程fx"""
    dcount = 0   # 迭代次数
    while True:
        dcount += 1
        c = (a + b) / 2

        if fx(c) == 0:
            return c, a, b, dcount
        elif fx(a) * fx(c) > 0:
            a = c
        else:
            b = c

        if b - a <= e:
            return (a + b) / 2, a, b, dcount


c, a, b, count = dichotomy(1, 2, 5 * 10 ** (-6))

print("近似值为：" + str(c) + "\n" + "区间：[" + str(a) + ", " + str(b) + "]\n" + "迭代次数：" + str(count))
