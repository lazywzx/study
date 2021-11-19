import cv2
import time
import numpy as np


def rs_align(ref_path, reg_path, output_path, order, ratio_thresh):
    """
    输入参考图像和待配准图像路径, 将两幅图进行配准并输出中间结果到输出路径下, 同时返回配准误差
    :param ref_path: 参考图像
    :param reg_path: 待配准图像
    :param output_path: 输出目录
    :param order: 指定映射多项式阶数, 限制1到3阶
    :param ratio_thresh: 匹配阈值, 控制匹配对数(0~1)
    :return: 匹配点对数, X, Y方向上的配准误差均方根
    """
    if order < 1 or order > 3:
        raise ValueError("阶数必须为1或2或3！")

    """ ************************ 1. 读入图像, 保持原始格式 ************************ """
    ref_img = cv2.imread(ref_path, -1)
    reg_img = cv2.imread(reg_path, -1)

    """ ************************ 2. 提取特征点 ********************************** """
    detector = cv2.SIFT_create(nfeatures=2000)
    ref_kp, ref_des = detector.detectAndCompute(ref_img, None)
    reg_kp, reg_des = detector.detectAndCompute(reg_img, None)

    """ ************************ 3. 画出特征点并保存 ***************************** """
    ref_kp_img = cv2.drawKeypoints(ref_img, ref_kp, None)
    reg_kp_img = cv2.drawKeypoints(reg_img, reg_kp, None)
    # 调整大小以拼接
    if ref_kp_img.shape[0] < reg_kp_img.shape[0]:
        kps_img = np.hstack([ref_kp_img, cv2.resize(reg_kp_img, (ref_kp_img.shape[0], ref_kp_img.shape[1]))])
    elif ref_kp_img.shape[0] > reg_kp_img.shape[0]:
        kps_img = np.hstack([cv2.resize(ref_kp_img, (reg_kp_img.shape[0], reg_kp_img.shape[1])), reg_kp_img])
    else:
        kps_img = np.hstack([ref_kp_img, reg_kp_img])
    cv2.imwrite(output_path + 'kps.png', kps_img)

    """ ************************ 4. 匹配特征点 ********************************** """
    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
    knn_matches = matcher.knnMatch(ref_des, reg_des, k=2)

    """ ************************ 5. 寻找good matches *************************** """
    good_matches = []
    for m, n in knn_matches:
        if m.distance < ratio_thresh * n.distance:
            good_matches.append(m)

    """ ************************ 6. 画出匹配结果并保存 **************************** """
    match_img = cv2.drawMatches(ref_img, ref_kp, reg_img, reg_kp, good_matches, None, flags=2)
    cv2.imwrite(output_path + 'matches.png', match_img)

    """ ************************ 7. 建立映射多项式并表示成矩阵形式 ****************** """
    """
    # 一阶多项式
    # u = a0 + a1 * x + a2 * y
    # v = b0 + b1 * x + b2 * y
    # 二阶多项式
    # u = a0 + a1 * x + a2 * y + a3 * xy + a4 * x^2 + a5 * y^2
    # v = b0 + b1 * x + b2 * y + b3 * xy + b4 * x^2 + b5 * y^2
    # 三阶多项式
    # u = a0 + a1 * x + a2 * y + a3 * xy + a4 * x^2 + a5 * y^2 + a6 * x^2y + a7 * y^2x + a8 * x^3 + a9 * y^3
    # v = b0 + b1 * x + b2 * y + b3 * xy + b4 * x^2 + b5 * y^2 + b6 * x^2y + b7 * y^2x + b8 * x^3 + b9 * y^3
    """
    len_gm = len(good_matches)
    matrix_xy = np.ones((len_gm, (3, 6, 10)[order - 1]), dtype=float)
    vector_u = np.zeros(len_gm, dtype=float)
    vector_v = np.zeros(len_gm, dtype=float)
    for i in range(0, len_gm):
        # 提取匹配点坐标
        x, y = ref_kp[good_matches[i].queryIdx].pt
        u, v = reg_kp[good_matches[i].trainIdx].pt
        # 计算matrix_xy矩阵元素
        # 一阶
        matrix_xy[i][1] = x
        matrix_xy[i][2] = y
        # 二阶
        if order >= 2:
            matrix_xy[i][3] = x * y
            matrix_xy[i][4] = x ** 2
            matrix_xy[i][5] = y ** 2
        # 三阶
        if order >= 3:
            matrix_xy[i][6] = x ** 2 * y
            matrix_xy[i][7] = y ** 2 * x
            matrix_xy[i][8] = x ** 3
            matrix_xy[i][9] = y ** 3

        # 计算u, v向量元素
        vector_u[i] = u
        vector_v[i] = v

    """ ************************ 8. 求解多项式系数向量(解超定方程组) **************** """
    a = np.linalg.lstsq(matrix_xy, vector_u, rcond=None)[0]
    b = np.linalg.lstsq(matrix_xy, vector_v, rcond=None)[0]

    """ ************************ 9. 重采样 ************************************* """
    # 根据目标图像像素坐标, 计算要采样亮度的图像坐标
    # 采用三次卷积差值得到目标图像像素亮度
    dst_height = ref_img.shape[0]
    dst_width = ref_img.shape[1]
    dst_img = np.zeros((dst_height, dst_width), dtype=np.uint8)

    reg_height = reg_img.shape[0]
    reg_width = reg_img.shape[1]
    tmp_img = np.array(reg_img, dtype=float)

    # 这里有个超级大坑：x, u是横坐标, 代表列; y, v是纵坐标, 代表行!
    for y in range(0, dst_height):
        for x in range(0, dst_width):
            # 映射多项式
            # 一阶
            u = a[0] + a[1] * x + a[2] * y
            v = b[0] + b[1] * x + b[2] * y
            # 二阶
            if order >= 2:
                u += a[3] * x * y + a[4] * x ** 2 + a[5] * y ** 2
                v += b[3] * x * y + b[4] * x ** 2 + b[5] * y ** 2
            # 三阶
            if order >= 3:
                u += a[6] * x ** 2 * y + a[7] * y ** 2 * x + a[8] * x ** 3 + a[9] * y ** 3
                v += b[6] * x ** 2 * y + b[7] * y ** 2 * x + b[8] * x ** 3 + b[9] * y ** 3

            # 判断边界条件, 防止越界
            u_norm = int(u)
            v_norm = int(v)
            if u_norm < 1 or u_norm > reg_width - 3 or v_norm < 1 or v_norm > reg_height - 3:
                continue

            # 三次卷积插值
            # 水平插值
            u_dist = u - u_norm
            horizontal_value = np.zeros(4, dtype=float)
            for k in range(0, 4):
                horizontal_value[k] = u_dist * \
                                      (u_dist *
                                       (u_dist *
                                        (tmp_img[v_norm - 1 + k][u_norm + 2] - tmp_img[v_norm - 1 + k][u_norm + 1]
                                         + tmp_img[v_norm - 1 + k][u_norm] - tmp_img[v_norm - 1 + k][u_norm - 1])
                                        + tmp_img[v_norm - 1 + k][u_norm + 1] - tmp_img[v_norm - 1 + k][u_norm + 2]
                                        + 2 * (tmp_img[v_norm - 1 + k][u_norm - 1] - tmp_img[v_norm - 1 + k][u_norm]))
                                       + tmp_img[v_norm - 1 + k][u_norm + 1] - tmp_img[v_norm - 1 + k][u_norm - 1]) \
                                      + tmp_img[v_norm - 1 + k][u_norm]

            # 垂直插值
            v_dist = v - v_norm
            vertical_value = v_dist * \
                             (v_dist *
                              (v_dist *
                               (horizontal_value[3] - horizontal_value[2] + horizontal_value[1] - horizontal_value[0])
                               + horizontal_value[2] - horizontal_value[3]
                               + 2 * (horizontal_value[0] - horizontal_value[1]))
                              + horizontal_value[2] - horizontal_value[0]) + horizontal_value[1]

            # 图像赋值
            if vertical_value < 0:
                brightness = 0
            elif vertical_value > 255:
                brightness = 255
            else:
                brightness = round(vertical_value)
            dst_img[y][x] = brightness

    cv2.imwrite(output_path + 'alignment.png', dst_img)

    """ ************************ 10. 伪彩色显示, 直观对比匹配效果 ******************* """
    merge_img = np.zeros((dst_height, dst_width, 3), dtype=np.uint8)
    merge_img[:, :, 2] = ref_img  # 参考图像为红色
    merge_img[:, :, 1] = dst_img  # 配准图像为绿色
    cv2.imwrite(output_path + 'merge.png', merge_img)

    """ ************************ 11. 计算匹配误差(由控制点引起的坐标误差) ************ """
    error_x = np.zeros(len_gm, dtype=float)
    error_y = np.zeros(len_gm, dtype=float)
    for i in range(0, len_gm):
        # X, Y方向上的单点误差
        x, y = ref_kp[good_matches[i].queryIdx].pt
        # 一阶
        error_x[i] = a[0] + a[1] * x + a[2] * y - reg_kp[good_matches[i].trainIdx].pt[0]
        error_y[i] = b[0] + b[1] * x + b[2] * y - reg_kp[good_matches[i].trainIdx].pt[1]
        # 二阶
        if order >= 2:
            error_x[i] += a[3] * x * y + a[4] * x ** 2 + a[5] * y ** 2
            error_y[i] += b[3] * x * y + b[4] * x ** 2 + b[5] * y ** 2
        # 三阶
        if order >= 3:
            error_x[i] += a[6] * x ** 2 * y + a[7] * y ** 2 * x + a[8] * x ** 3 + a[9] * y ** 3
            error_y[i] += b[6] * x ** 2 * y + b[7] * y ** 2 * x + b[8] * x ** 3 + b[9] * y ** 3

    # 计算均方根
    r_x = (sum(error_x ** 2) / len_gm) ** 0.5
    r_y = (sum(error_y ** 2) / len_gm) ** 0.5

    return len_gm, r_x, r_y


# 调用配准程序并计时
st_time = time.time()
gcp_num, rms_x, rms_y = rs_align('./images/test1.tif', './images/test2.tif', './output/', 3, 0.5)
cost_time = time.time() - st_time
print('配准完成, 匹配点个数:', gcp_num, '\n共耗时', time.time() - st_time, '秒。')
