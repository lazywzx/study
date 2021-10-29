import numpy as np
import sympy as sp


def fx(x, y, z, d):
    """定义函数组Fx及其导函数"""
    retMat = {
        "matF": None,
        "matF_d": None
    }

    matF = np.array([x * y - z ** 2 - 1,
                     x * y * z + y ** 2 - x ** 2 - 2,
                     np.exp(x) + z - np.exp(y) - 3])
    retMat["matF"] = matF.T

    if d:   # 是否需要计算导函数
        val_x = x
        val_y = y
        val_z = z

        # 求导
        x, y, z = sp.symbols('x y z')
        Fx = sp.Matrix([[x * y - z ** 2 - 1],
                        [x * y * z + y ** 2 - x ** 2 - 2],
                        [sp.exp(x) + z - sp.exp(y) - 3]])

        v = sp.Matrix([x, y, z])
        F_diff = Fx.diff(v)

        # 恢复可计算状态
        F_d = sp.lambdify((x, y, z), F_diff, 'numpy')
        val_list = F_d(val_x, val_y, val_z)

        # 转换成数值矩阵
        matF_d = np.array(np.zeros((3, 3)))
        for j in range(len(val_list)):
            for i in range(len(val_list[j][0])):
                matF_d[i][j] = val_list[j][0][i][0]

        retMat["matF_d"] = matF_d

    return retMat


def compute(x, y, z, H0, e1, e2, e3, k):
    """计算一次迭代"""
    xv = np.array([x, y, z]).T
    matF = fx(x, y, z, 0)["matF"]
    if sum((abs(matF) < np.array([e1, e2, e3]).T)) > 0:
        return "奇异标志", xv, k

    xv1 = xv - np.dot(H0, matF)
    r0 = xv1 -xv
    matF1 = fx(xv1[0], xv1[1], xv1[2], 0)["matF"]
    y0 = matF1 - matF
    H1 = H0 + np.dot((r0 - np.dot(H0, y0)), np.dot(r0.T, H0) / np.dot(np.dot(r0.T, H0), y0))

    return xv1, H1, r0


def inv_broyden(x0, y0, z0, ex, ey, ez, e1, e2, e3, n):
    """逆Broyden求解方程组近似解"""
    # 计算其他初始值
    F0_d = fx(x0, y0, z0, 1)["matF_d"]
    xv = np.array([x0, y0, z0]).T
    H0 = np.linalg.inv(F0_d)    # 矩阵求逆

    k = 1
    while True:
        xv, H0, r0 = compute(xv[0], xv[1], xv[2], H0, e1, e2, e3, k)

        if sum((abs(r0) < np.array([ex, ey, ez]).T)) == 3:
            return "迭代成功", xv, k
        elif k == n:
            return "迭代失败", xv, k
        else:
            k += 1
            print(xv)


flag, x, k = inv_broyden(1, 1, 1, 5e-6, 5e-6, 5e-6, 1e-10, 1e-10, 1e-10, 20)

print("迭代结果：" + flag + "\n" + "近似值：" + str(x) + "\n迭代次数：" + str(k))
