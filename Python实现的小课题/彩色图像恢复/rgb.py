import cv2
import numpy as np
import sys


def read_img(img_name):
    img_name = img_name[1]
    img_path = './src_image/' + img_name + '.png'
    src_img = cv2.imread(img_path)

    b_com = src_img[:, :, 0]
    g_com = src_img[:, :, 1]
    r_com = src_img[:, :, 2]

    if img_name == 'xxs':
        img_size = 390
    elif img_name == 'jst':
        img_size = 203
    elif img_name == 'yfl':
        img_size = 240
    elif img_name == 'ng':
        img_size = 192
    else:
        img_size = 500
        print("Error Argv!")
    return b_com, g_com, r_com, img_size, img_name


def rgb_get(component, x_position, y_position):
    tmp_img = np.zeros((y_size, 320, 3), np.uint8)
    tmp_img.fill(0)
    if component == 'Red':
        tmp_img[:, :, 0] = 0
        tmp_img[:, :, 1] = 0
        tmp_img[:, :, 2] = r
    elif component == 'Green':
        tmp_img[:, :, 0] = 0
        tmp_img[:, :, 1] = g
        tmp_img[:, :, 2] = 0
    elif component == 'Blue':
        tmp_img[:, :, 0] = b
        tmp_img[:, :, 1] = 0
        tmp_img[:, :, 2] = 0
    elif component == 'Original':
        tmp_img[:, :, 0] = b
        tmp_img[:, :, 1] = g
        tmp_img[:, :, 2] = r
    elif component == 'Delete_Green':
        tmp_img[:, :, 0] = b
        tmp_img[:, :, 1] = 0
        tmp_img[:, :, 2] = r
    elif component == 'DG_recover':
        if b.all() > r.all():
            rec_g = r
        else:
            rec_g = b
        tmp_img[:, :, 0] = b
        tmp_img[:, :, 1] = rec_g
        tmp_img[:, :, 2] = r
    elif component == 'Gray_REC_DG':
        if b.all() > r.all():
            rec_g = r
        else:
            rec_g = b
        tmp_img[:, :, 0] = b
        tmp_img[:, :, 1] = rec_g
        tmp_img[:, :, 2] = r
        tmp_img = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)
        save_path = './rgb_image/Gray_DG_' + name + '.png'
        cv2.imwrite(save_path, tmp_img)
    else:
        print("Error Argv!")
        return None

    cv2.namedWindow(component, 0)
    cv2.resizeWindow(component, 320, y_size)
    cv2.moveWindow(component, x_position, y_position)
    cv2.imshow(component, tmp_img)


def image_recover():
    path = './rgb_image/Gray_REC_DG_' + name + '.png'
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

    outputFile = './recover_image/' + name + '_colorized.png'
    cv2.imwrite(outputFile, (img_bgr_out * 255).astype(np.uint8))

    rec_img = cv2.imread(outputFile)
    cv2.namedWindow('Recover_image', 0)
    cv2.resizeWindow('Recover_image', 320, y_size)
    cv2.moveWindow('Recover_image', 1080, y_size + 50)
    cv2.imshow('Recover_image', rec_img)

    print('Done!')


if __name__ == "__main__":
    b, g, r, y_size, name = read_img(sys.argv)
    rgb_get('Original', 30, 10)
    rgb_get('Red', 380, 10)
    rgb_get('Green', 730, 10)
    rgb_get('Blue', 1080, 10)
    rgb_get('Delete_Green', 40, y_size + 50)
    rgb_get('DG_recover', 380, y_size + 50)
    rgb_get('Gray_REC_DG', 730, y_size + 50)
    image_recover()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
