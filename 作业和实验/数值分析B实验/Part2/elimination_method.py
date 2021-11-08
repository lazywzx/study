import numpy as np


def gauss_elimination(A, b):
    """高斯消元法"""

    # 合并增广矩阵
    Ab = np.concatenate((A, b), axis=1)

    # 消元过程
    n = Ab.shape[0]
    for k in range(0, n-1):
        for i in range(k+1, n):
            m = Ab[i][k] / Ab[k][k]
            Ab[i] = Ab[i] - Ab[k] * m

    # 回代过程
    x = np.zeros(n).T
    x[n-1] = Ab[n-1][n] / Ab[n-1][n-1]
    for i in range(n-2, -1, -1):
        ax_sum = 0
        for j in range(i+1, n):
            ax_sum += Ab[i][j] * x[j]
        x[i] = (Ab[i][n] - ax_sum) / Ab[i][i]

    # 返回解向量
    return x


def gauss_column_principal_elimination(A, b):
    """高斯列主元消去法"""

    # 合并增广矩阵
    Ab = np.concatenate((A, b), axis=1)

    # 消元过程
    n = Ab.shape[0]
    for k in range(0, n-1):
        index_maxnum = np.argmax(abs(Ab[:, k]))  # 获取最大列元素绝对值的索引
        # 交换行
        tmp = Ab[k, :].copy()
        Ab[k, :] = Ab[index_maxnum, :].copy()
        Ab[index_maxnum, :] = tmp

        for i in range(k+1, n):
            m = Ab[i][k] / Ab[k][k]
            Ab[i] = Ab[i] - Ab[k] * m

    # 回代过程
    x = np.zeros(n).T
    x[n - 1] = Ab[n - 1][n] / Ab[n - 1][n - 1]
    for i in range(n - 2, -1, -1):
        ax_sum = 0
        for j in range(i + 1, n):
            ax_sum += Ab[i][j] * x[j]
        x[i] = (Ab[i][n] - ax_sum) / Ab[i][i]

    # 返回解向量
    return x


# 线性方程组系数矩阵
A1 = np.array([[1e-8, 2, 3], [-1, 3.712, 4.623], [-2, 1.072, 5.643]])
b1 = np.array([[1], [2], [3]])

A2 = np.array([[4, -2, 4], [-2, 17, 10], [-4, 10, 9]])
b2 = np.array([[10], [3], [7]])

# 求解
x1_gauss = gauss_elimination(A1, b1)
x1_gauss_col = gauss_column_principal_elimination(A1, b1)

x2_gauss = gauss_elimination(A2, b2)
x2_gauss_col = gauss_column_principal_elimination(A2, b2)

# 输出
print("方程组1：\nA=", A1, "\nb=", b1, "\n高斯消去法结果: x1=", x1_gauss, "\n高斯列主元消去法结果: x1=", x1_gauss_col)
print("\n方程组2：\nA=", A2, "\nb=", b2, "\n高斯消去法结果: x2=", x2_gauss, "\n高斯列主元消去法结果: x2=", x2_gauss_col)
