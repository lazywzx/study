import os, random, cv2
import numpy as np

"""funcs for drawing features/matches"""


def draw_features(img, x, y, scale, orien, destype='circle'):
    """
    draw features on image

    :param img:
    :param x:
    :param y:
    :param scale:
    :param orien: must be radius
    :param destype:
    :return:
    """
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    x = int(x)
    y = int(y)
    scale = int(scale)
    lx = int(scale * np.cos(orien) + x)
    ly = int(scale * np.sin(orien) + y)

    # drawing type
    if destype == 'arrowed':
        cv2.arrowedLine(img, (x, y), (lx, ly), color, 2, 8, 0, 0.3)
    else:
        cv2.circle(img, (x, y), scale, color, 5)
        cv2.line(img, (x, y), (lx, ly), color, 5)

    return img


def extract_imgname(npz_name):
    """
    extract image name from npz file

    :param npz_name:
    :return:
    """
    name, ext = os.path.splitext(npz_name)
    imgname, feaext = os.path.splitext(name)
    return imgname


def feature_vis(feature_path, img_path, output_path):
    """
    visualize features on images

    :param feature_path:
    :param img_path:
    :param output_path:
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    featlist = os.listdir(feature_path)
    for npzname in featlist:
        imgname = extract_imgname(npzname)
        # read image
        rawimg = cv2.imread(os.path.join(img_path, imgname))
        drawimg = rawimg.copy()
        height = drawimg.shape[0]
        weight = drawimg.shape[1]
        # read points
        feat_path = os.path.join(feature_path, npzname)
        points = (np.load(feat_path))['points']
        for p in points:
            x = (p[0] + 0.5) * weight
            y = (p[1] + float(height) / weight / 2) * weight
            scale = p[2] * weight
            orien = np.deg2rad(p[3])
            drawimg = draw_features(drawimg, x, y, scale, orien)
        # put text -points: num- on image
        cv2.putText(drawimg, "points: " + str(len(points)), (int(weight * 0.05), int(height * 0.05)),
                    cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 8)
        small_img = cv2.resize(drawimg, (int(weight / 4), int(height / 4)))
        cv2.imwrite(os.path.join(output_path, "draw_" + imgname), small_img)  # save to file


feature_vis("./features", "./images", "./drawed")
