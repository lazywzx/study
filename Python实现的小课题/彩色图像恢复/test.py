import numpy as np
import cv2
import os.path


def image_recover(image_path):
    path = './rgb_image/' + image_path + '.png'
    # 读取图片
    frame = cv2.imread(path)
    print('image_read_successful!   1/7')

    # 指定model所在路径
    protoFile = './models/colorization_deploy_v2.prototxt'
    weightFile = './models/colorization_release_v2.caffemodel'

    print('pts_loading...')
    # 加载聚类中心
    pts_in_hull = np.load('./pts_in_hull.npy')
    print('pts_load_successful! 2/7')

    print('NetFrom_reading...')
    # 读取网络
    net = cv2.dnn.readNetFromCaffe(protoFile, weightFile)
    print('NetFrom_read_successful! 3/7')

    print('Layer_getting...')
    # 将聚类中心填充为1x1卷积核
    pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1)
    net.getLayer(net.getLayerId('class8_ab')).blobs = [pts_in_hull.astype(np.float32)]
    net.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]
    print('Layer_get_successful!    4/7')

    W_in = 224
    H_in = 224

    img_rgb = (frame[:, :, [2, 1, 0]] * 1.0 / 255).astype(np.float32)
    img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2Lab)
    img_l = img_lab[:, :, 0]  # 提取出L通道
    print('Convert_successful!  5/7')

    # 将L通道的图像重新设置大小为network的输出大小
    img_l_rs = cv2.resize(img_l, (W_in, H_in))
    img_l_rs -= 50 # 从mean-centering减去50
    net.setInput(cv2.dnn.blobFromImage(img_l_rs))
    ab_dec = net.forward()[0, :, :, :].transpose((1, 2, 0))  # 结果
    print('Reset_successful!    6/7')

    (H_orig, W_orig) = img_rgb.shape[:2]  # 原始的图片大小
    ab_dec_us = cv2.resize(ab_dec, (W_orig, H_orig))
    img_lab_out = np.concatenate((img_l[:, :, np.newaxis], ab_dec_us), axis=2)  # 与原始图片L连接
    img_bgr_out = np.clip(cv2.cvtColor(img_lab_out, cv2.COLOR_Lab2BGR), 0, 1)
    print('Link_successful! 7/7')

    outputFile = './recover_image/' + image_path + '_colorized.png'
    cv2.imwrite(outputFile, (img_bgr_out * 255).astype(np.uint8))
    print('Done!')
