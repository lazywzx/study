import math
import sympy as sp


def fx(x, index):
    """定义函数fx"""
    if index == 1:
        """定义函数fx = x * e^x - 1及其导函数"""
        val_fx = x * math.pow(math.e, x) - 1
    elif index == 2:
        """定义函数fx = x^3 - x - 1及其导函数"""
        val_fx = x ** 3 - x - 1
    elif index == 3:
        """定义函数fx = (x - 1)^2 * (2x - 1)"""
        val_fx = (x - 1) ** 2 * (2 * x - 1)
    else:
        raise ValueError("index必须是1、2或3")

    val_x = x

    # 求导
    x = sp.Symbol('x')
    if index == 1:
        fx = x * sp.exp(x) - 1
    elif index == 2:
        fx = x ** 3 - x - 1
    else:
        fx = (x - 1) ** 2 * (2 * x - 1)

    fx_diff = fx.diff(x)

    # 恢复可计算状态
    fx_d = sp.lambdify(x, fx_diff, 'numpy')

    return val_fx, fx_d(val_x)


def newton_iteration(x0, e1, e2, n, index, r):
    """牛顿迭代法求解近似值"""
    """
        x0: 初始值
        e1: f(x)小于这个值抛出奇异标志
        e2: |x1 - x0|小于这个值迭代成功
        n: 最大迭代次数
        index: 选择f(x)
        r: 根的重数
    """
    k = 1  # 迭代次数

    while True:
        if abs(fx(x0, index)[0]) < e1:
            return "奇异标志", x0, k

        x1 = x0 - r * fx(x0, index)[0] / fx(x0, index)[1]
        if abs(x1 - x0) < e2:
            return "迭代成功", x1, k

        if k == n:
            return "迭代失败", x1, k

        x0 = x1
        k += 1
        print(x1)


flag, x, k = newton_iteration(0.8, 1e-30, 5e-6, 200, 3, 2)
"""在二重根附近迭代，不进行修正，迭代仍具有线性收敛性，修正后迭代速度变快"""
"""在修正为二重根迭代公式后，初始值必须大于2/3，否则迭代不收敛，初始值越接近2/3，迭代越慢且前期值偏离非常大"""

print("迭代结果：" + flag + "\n" + "近似值：" + str(x) + "\n迭代次数：" + str(k))
