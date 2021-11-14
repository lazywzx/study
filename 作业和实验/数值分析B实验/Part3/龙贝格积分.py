import numpy as np


def f(x):
    """定义函数f"""
    # (1) f(x) = x ** 3
    # return x ** 3
    """
    # (2) f(x) = sin(x) / x
    if abs(x) < 1e-6:
        return 1.0
    else:
        return np.sin(x) / x
    """

    # (3) f(x) = sin(x ** 2)
    return np.sin(x ** 2)


def rom_berg(a, b, n, e):
    """龙贝格积分法"""
    T = np.zeros((n, n))
    T[0][0] = (b - a) / 2 * (f(a) + f(b))

    i = 1
    while True:
        # 求f sum
        fsum = 0
        for j in range(1, 2 ** (i - 1) + 1):
            x = a + (2 * j - 1) * (b - a) / 2 ** i
            fsum += f(x)

        T[0][i] = 0.5 * (T[0][i-1] + (b - a) / 2 ** (i - 1) * fsum)

        for m in range(1, i + 1):
            k = i - m
            T[m][k] = (4 ** m * T[m-1][k+1] - T[m-1][k]) / (4 ** m - 1)

        if abs(T[i][0] - T[i-1][0]) <= e:
            print("计算成功\t计算次数：", i, "\t积分结果：", T[i][0], "\tT数表：\n", T)
            break
        elif i == n - 1:
            print("计算失败，请增大T数表维度")
            break
        else:
            i += 1


rom_berg(0, 1, 4, 5e-5)
