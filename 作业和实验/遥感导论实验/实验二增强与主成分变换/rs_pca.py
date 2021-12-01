import numpy as np
from osgeo import gdal
from matplotlib import pyplot as plt

# 解决plt显示中文问题
plt.rcParams['font.sans-serif'] = ['SimHei']
# 禁止科学计数法输出
np.set_printoptions(suppress=True)

"""==========================================1. 读入数据========================================"""
data = gdal.Open('./Exp2_TM.tif')
img = data.ReadAsArray()
# 降到二维
bands, height, width = img.shape
x = img.transpose(1, 2, 0).reshape((-1, bands))

"""==========================================2. 求特征向量特征值=================================="""
# 各波段均值
mean_x = np.array([np.mean(x[:, i]) for i in range(bands)], dtype=float)
# 协方差矩阵
x_m = x - mean_x
cov_mat_x = np.dot(x_m.T, x_m) / (x.shape[0] - 1)
# 相关矩阵
R_mat_x = np.zeros((bands, bands), dtype=float)
for i in range(bands):
    for j in range(bands):
        R_mat_x[i][j] = cov_mat_x[i][j] / (cov_mat_x[i][i] * cov_mat_x[j][j]) ** 0.5

# 特征值与特征向量
eigen_value, feature_vector = np.linalg.eig(cov_mat_x)
# 按特征值由大到小排序
eig_sort = np.sort(eigen_value)[::-1]
sort_index = eigen_value.argsort()[::-1]
fv_sort = feature_vector[:, sort_index]
# 各特征值占比
eig_weight = [str(np.around(i / sum(eig_sort) * 100, 2)) + '%' for i in eig_sort]

"""==========================================3. 主成分变换======================================="""
y = np.dot(fv_sort.T, x.T).T

"""==========================================4. 验证变换后分量相关性==============================="""
mean_y = np.array([np.mean(y[:, i]) for i in range(bands)], dtype=float)
# 协方差矩阵
y_m = y - mean_y
cov_mat_y = np.dot(y_m.T, y_m) / (y.shape[0] - 1)
# 相关矩阵
R_mat_y = np.zeros((bands, bands), dtype=float)
for i in range(bands):
    for j in range(bands):
        R_mat_y[i][j] = cov_mat_y[i][j] / (cov_mat_y[i][i] * cov_mat_y[j][j]) ** 0.5

"""==========================================5. 恢复数据========================================"""
# 第一分量、前两分量、前三分量恢复
rec_x = []
rec_img = []
dis_rec = []
rmse = []
for xi in range(3):
    rec_x.append(np.dot(fv_sort[:, 0:(xi+1)], y[:, 0:(xi+1)].T).T)
    rec_img.append(rec_x[xi].reshape((height, width, bands)).transpose(2, 0, 1))
    # rec_img平移消除负亮度值
    dis_rec.append((rec_img[xi] - rec_img[xi].min()).astype(np.uint8))
    # 分析误差RMSE
    rmse.append((sum(sum(sum((rec_img[xi] - img) ** 2))) / (bands * height * width)) ** 0.5)

"""==========================================6. 输出结果========================================"""
# 各分量恢复数据误差
msg = ['第一', '前两', '前三']
for r in range(3):
    print(msg[r] + '分量恢复数据RMSE: ', rmse[r])

# 变换前后各分量相关性
print('变换前协方差矩阵COVx: \n', np.around(cov_mat_x, 2))
print('变换前相关矩阵Rx: \n', np.around(R_mat_x, 2))
print('特征值及其占比: \n', np.around(eigen_value, 2), '\n', eig_weight)
print('特征向量: \n', np.around(fv_sort, 4))
print('变换后协方差矩阵COVy: \n', np.around(cov_mat_y, 2))
print('变换后相关矩阵Ry: \n', np.around(R_mat_y, 2))

"""==========================================7. 结果可视化======================================="""
# PCA平移缩放亮度以显示
pca = y.reshape((height, width, bands)).transpose(2, 0, 1)
pca = ((pca - pca.min()) / (pca.max() - pca.min()) * 255).astype(np.uint8)

# 原始数据各个波段图
plt.figure('原始数据各波段图像')
for i in range(6):
    plt.subplot(231 + i)
    plt.imshow(img[i], cmap='gray')
    plt.title('Band' + str(1 + i))

# 显示各个主成分图
plt.figure('各主成分图')
for i in range(6):
    plt.subplot(231 + i)
    plt.imshow(pca[i], cmap='gray')
    plt.title('PC' + str(1 + i))

# 原始数据彩色合成与主成分合成图对比
tmp_img = np.zeros((height, width, 3), dtype=np.uint8)
plt.figure('原始数据彩色合成与主成分合成图对比')
plt.subplot(251)
tmp_img[:, :, 0] = img[2]; tmp_img[:, :, 1] = img[1]; tmp_img[:, :, 2] = img[0]; plt.imshow(tmp_img)
plt.title('原数据可见光波段321合成')

plt.subplot(256)
tmp_img[:, :, 0] = img[3]; tmp_img[:, :, 1] = img[2]; tmp_img[:, :, 2] = img[1]; plt.imshow(tmp_img)
plt.title('原数据标准假彩色波段432合成')

plt.subplot(252)
tmp_img[:, :, 0] = pca[2]; tmp_img[:, :, 1] = pca[1]; tmp_img[:, :, 2] = pca[0]; plt.imshow(tmp_img)
plt.title('主成分PC321合成')

plt.subplot(257)
tmp_img[:, :, 0] = pca[3]; tmp_img[:, :, 1] = pca[2]; tmp_img[:, :, 2] = pca[1]; plt.imshow(tmp_img)
plt.title('主成分PC432合成')

# 不同分量恢复结果各波段
dis_list = ['第一分量恢复后的各波段', '前两分量恢复后的各波段', '前三分量恢复后的各波段']
for i in range(3):
    plt.figure(dis_list[i])
    for j in range(6):
        plt.subplot(231 + j)
        plt.imshow(dis_rec[i][j], cmap='gray')
        plt.title('rec' + str(i + 1) + '_band' + str(1 + j))

# 分量恢复后合成图
plt.figure('原始数据彩色合成与主成分合成图对比')
plt.subplot(253)
tmp_img[:, :, 0] = dis_rec[0][2]; tmp_img[:, :, 1] = dis_rec[0][1]; tmp_img[:, :, 2] = dis_rec[0][0]; plt.imshow(tmp_img)
plt.title('第一分量恢复可见光波段321合成')

plt.subplot(258)
tmp_img[:, :, 0] = dis_rec[0][3]; tmp_img[:, :, 1] = dis_rec[0][2]; tmp_img[:, :, 2] = dis_rec[0][1]; plt.imshow(tmp_img)
plt.title('第一分量恢复标准假彩色432合成')

plt.subplot(254)
tmp_img[:, :, 0] = dis_rec[1][2]; tmp_img[:, :, 1] = dis_rec[1][1]; tmp_img[:, :, 2] = dis_rec[1][0]; plt.imshow(tmp_img)
plt.title('前两分量恢复可见光波段321合成')

plt.subplot(259)
tmp_img[:, :, 0] = dis_rec[1][3]; tmp_img[:, :, 1] = dis_rec[1][2]; tmp_img[:, :, 2] = dis_rec[1][1]; plt.imshow(tmp_img)
plt.title('前两分量恢复标准假彩色432合成')

plt.subplot(255)
tmp_img[:, :, 0] = dis_rec[2][2]; tmp_img[:, :, 1] = dis_rec[2][1]; tmp_img[:, :, 2] = dis_rec[2][0]; plt.imshow(tmp_img)
plt.title('前三分量恢复可见光波段321合成')

plt.subplot(2, 5, 10)
tmp_img[:, :, 0] = dis_rec[2][3]; tmp_img[:, :, 1] = dis_rec[2][2]; tmp_img[:, :, 2] = dis_rec[2][1]; plt.imshow(tmp_img)
plt.title('前三分量恢复标准假彩色432合成')

plt.show()
