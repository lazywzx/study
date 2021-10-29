import numpy as np

"""
不能用
用minVarEst.m代替
"""


def awgn(signal, snr):
    """
    加入高斯白噪声
    :param signal: 原始信号
    :param snr: 信噪比
    :return: 加噪后的信号
    """
    np.random.seed(7)
    snr = 10 ** (snr / 10.0)
    spower = np.sum(signal ** 2) / len(signal)
    npower = spower / snr
    noise = np.random.randn(len(signal)) * np.sqrt(npower)
    return signal + noise


# 设定真值向量
tvar = np.array([50, 60, 70]).T

# 设定传递矩阵H
# H1 = np.array([[1, -1, 1], [0, 0, 1], [1, 1, 1]])
H1 = np.array([[1, 1, 1], [4, 2, 1], [9, 3, 1]])

# 二次模型
y = np.dot(H1, tvar)

# 观测模型
z = awgn(y, 5)

# 估计向量
evar = np.dot(np.dot(np.linalg.inv(np.dot(H1.T, H1)), H1.T), z)

print(tvar, evar)
